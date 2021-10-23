import json
import os

import pandas
from kmodes.kprototypes import KPrototypes

from config.projectConfig import projectConfig
from processor.ActionPipe import ActionPipe
from processor.action.CalDistributionAction import CalDistributionAction
from processor.action.CalEntropyAction import CalEntropyAction
from processor.action.CommonFilterAction import CommonFilterAction
from processor.action.DropColAction import DropColAction
from processor.action.DropNanAction import DropNanAction
from processor.action.FilterDateAction import FilterDateAction
from processor.action.FilterInvalidUserAction import FilterInvalidUserAction
from processor.action.FlattenColAction import FlattenColAction
from processor.action.KeyWordCountAction import KeyWordCountAction
from processor.action.KeyWordReplaceAction import KeyWordReplaceAction
from processor.action.LabelEncoderAction import LabelEncoderAction
from processor.action.NormalizationAction import NormalizationAction
from processor.action.TokenizeAction import TokenizeAction
from processor.bean.PRTimeLineRelation import PRTimeLineRelation
from utils.ExcelHelper import ExcelHelper
from utils.pandasHelper import pandasHelper
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy

"""尝试提取一些comment的特征，然后用不同算法做据类的尝试"""


def loadIssueCommentData(projects):
    issueDataPath = projectConfig.getIssueCommentPath(isLocal=False)
    timelineDataPath = projectConfig.getPRTimeLineDataPath(isLocal=False)
    pullRequestDataPath = projectConfig.getPullRequestPath(isLocal=False)

    data = None
    for project in projects:
        issue_filename = os.path.join(issueDataPath, f'ALL_{project}_data_issuecomment.tsv')
        timeline_filename = os.path.join(timelineDataPath, f'ALL_{project}_data_prtimeline.tsv')
        pullrequest_filename = os.path.join(pullRequestDataPath, f'ALL_{project}_data_pullrequest.tsv')

        issueCommentData = pandasHelper().readTSVFile(fileName=issue_filename,
                                                      sep='\t', header=pandasHelper.INT_READ_FILE_WITH_HEAD)

        pullRequestData = pandasHelper().readTSVFile(fileName=pullrequest_filename,
                                                     sep='\t', header=pandasHelper.INT_READ_FILE_WITH_HEAD)

        pullRequestData = pullRequestData[['number', 'user_login']]
        pullRequestData.columns= ['pull_number', 'author']
        issueCommentData = pandas.merge(issueCommentData, pullRequestData, on='pull_number')

        timelineData = pandasHelper().readTSVFile(fileName=timeline_filename,
                                                  sep='\t', header=pandasHelper.INT_READ_FILE_WITH_HEAD)
        timelineData['login'] = timelineData['origin'].apply(lambda x: PRTimeLineRelation.parser(x).user_login)

        """计算每一个PR的事件线的长度, 以及issuecomment所在的位置的比例， 
            也顺带记录每个PR的 closed 的人的名字"""
        pr_len_dict = {}
        pr_close_login_dict = {}
        for pr_node, tempDf in dict(list(timelineData.groupby('pullrequest_node'))).items():
            pr_len_dict[pr_node] = max(tempDf['position'])
            df_t = tempDf.loc[tempDf['typename'] == 'ClosedEvent']
            if df_t.shape[0] > 0:
                """存在关闭的事件"""
                pr_close_login_dict[pr_node] = getattr(df_t.iloc[0], "login")

        """加载 timeline 的数据后， 把两个数据做join"""
        timelineData['timeline_length'] = timelineData.apply(
            lambda x: pr_len_dict.get(x['pullrequest_node'], numpy.NAN), axis=1)
        timelineData['close_login'] = timelineData.apply(
            lambda x: pr_close_login_dict.get(x['pullrequest_node'], numpy.NAN), axis=1)
        timelineData = timelineData.loc[timelineData['typename'] == 'IssueComment'].copy(deep=True)
        timelineData = timelineData[['timelineitem_node', 'position', 'timeline_length', 'close_login']]
        issueCommentData = pandas.merge(issueCommentData, timelineData, how='inner',
                                        left_on='node_id', right_on='timelineitem_node')
        issueCommentData['position_ratio'] = issueCommentData.apply(lambda x: x['position'] / x['timeline_length'],
                                                                    axis=1)
        issueCommentData['close_login'] = issueCommentData.apply(lambda x: x['close_login'] == x['user_login'], axis=1)
        if data is None:
            data = issueCommentData
        else:
            data = pandas.concat([data, issueCommentData])

    return data


def try_kmeans(X, label):
    """尝试使用 kmeans 算法"""
    scores = []
    for n_cluster in range(2, 10):
        y_pred = KMeans(n_clusters=n_cluster, random_state=9, n_jobs=4).fit_predict(X)
        # score = metrics.calinski_harabasz_score(X, y_pred) # ch-index
        score = metrics.silhouette_score(X, y_pred, metric='euclidean')  # 样本平均轮廓系数
        scores.append(score)

    plt.plot(range(2, 10), scores, label=label)


def try_kprototypes(X, label):
    """尝试使用 k-prototypes 算法"""
    scores_ch = []
    score_si = []
    for n_cluster in range(2, 10):
        # y_pred = KMeans(n_clusters=n_cluster, random_state=9, n_jobs=4).fit_predict(X)
        # # score = metrics.calinski_harabasz_score(X, y_pred) # ch-index
        # score = metrics.silhouette_score(X, y_pred,metric='euclidean')  # 样本平均轮廓系数
        # scores.append(score)
        km = KPrototypes(n_clusters=n_cluster, n_jobs=4, random_state=9, init='Huang')
        y_pred = km.fit_predict(X, categorical=[0, 2])
        score = metrics.calinski_harabasz_score(X, y_pred)  # ch-index
        scores_ch.append(score)

        score = metrics.silhouette_score(X, y_pred, metric='euclidean')  # 样本平均轮廓系数
        score_si.append(score)

    plt.plot(range(2, 10), scores_ch, label=label)
    # plt.plot(range(2, 10), score_si, label=label)


def analyze_kneams(X, label):
    n_clusters = 3
    y_pred = KMeans(n_clusters=n_clusters, random_state=9, n_jobs=4).fit_predict(X)
    nums = []
    for i in range(0, n_clusters):
        num = [x for x in y_pred if x == i].__len__()
        nums.append(num)

    print("nums for each class:")
    for i in range(0, n_clusters):
        print(f"class {i}: {nums[i]}")

    print("==" * 20)
    print("avg center of each class:")
    for i in range(0, n_clusters):
        sum_v = [0 for _ in range(0, X.shape[1])]
        for index, y in enumerate(y_pred):
            if y == i:
                sum_v = [a + b for a, b in zip(sum_v, list(X.iloc[index]))]

        sum_v = [x / nums[i] for x in sum_v]
        print(f"feature for class {i}", sum_v)


def analyze_kprototypes(X, label, n_clusters):
    # n_clusters = 3
    print("==" * 50)
    km = KPrototypes(n_clusters=n_clusters, n_jobs=4, random_state=9, init='Huang')
    y_pred = km.fit_predict(X, categorical=[0, 2])

    nums = []
    for i in range(0, n_clusters):
        num = [x for x in y_pred if x == i].__len__()
        nums.append(num)

    print("nums for each class:")
    for i in range(0, n_clusters):
        print(f"class {i}: {nums[i]}")

    print("==" * 20)
    print("avg center of each class:")
    for i in range(0, n_clusters):
        sum_v = [0 for _ in range(0, X.shape[1])]
        for index, y in enumerate(y_pred):
            if y == i:
                sum_v = [a + b for a, b in zip(sum_v, list(X.iloc[index]))]

        sum_v = [x / nums[i] for x in sum_v]
        print(f"feature for class {i}", sum_v)

def sample_low_data(data, project, targetCol):
    print(data)
    """根据目标的col做数值的排序"""
    data.sort_values(by=targetCol, inplace=True)
    data.reset_index(drop=True, inplace=True)

    for index, row in data.iterrows():
        if index == 500:
            break
        if index % 25 == 0:
            number = getattr(row, 'pull_number')
            text = getattr(row, 'body')
            entropy = getattr(row, 'entropy')
            print('project:', project, "  pull:", number, 'entropy:', entropy, ' text:', text)



def analyze_dis_by_col(data, project, targetCol):
    print(data)
    """根据目标的col做数值的排序"""
    data.sort_values(by=targetCol, inplace=True)
    data.reset_index(drop=True, inplace=True)

    """对数值做分桶，分20份"""
    loop = 20
    step = data.shape[0] // loop
    results = []
    cols = data.columns
    results.append(cols)
    for i in range(0, loop):
        result = []
        for col in cols:
            result.append(numpy.mean(data[col][i * step: i * step + step]))
        results.append(result)
    print(results)

    excelName = 'bin_analyze.xls'
    sheetName = f"{project}_{targetCol}"
    if os.path.exists(excelName):
        ExcelHelper().addSheet(filename=excelName, sheetName=sheetName)
    else:
        ExcelHelper().initExcelFile(fileName=excelName, sheetName=sheetName)
    ExcelHelper().appendExcelRowWithDataLists(fileName=excelName, sheetName=sheetName,
                                              dataLists=results, style=ExcelHelper.getNormalStyle())

if __name__ == "__main__":
    projects = ['akka', 'cakephp', 'scikit-learn', 'symfony', 'xbmc', '']
    # projects = ['cakephp']
    for project in projects:
        print("==" * 50)
        print(f"project:{project}")
        issueCommentData = loadIssueCommentData(projects)

        """对issue comment的一些特征做预处理"""
        textCol = 'body'
        userCol = 'user_login'
        dateCol = 'created_at'

        """开发者身份映射表"""
        association_label_map = {}
        """是否为合入者映射表"""
        close_login_map = {}

        processor = ActionPipe()
        processor.add_action(FilterDateAction(targetCol=dateCol, dateRange=(2017, 1, 2020, 6))). \
            add_action(DropNanAction(targetCol=textCol)). \
            add_action(CommonFilterAction(targetCol='author_association',
                                          filter_func=lambda x: x != 'COLLABORATOR')). \
            add_action(CommonFilterAction(targetCol= None,
                                          filter_func=lambda x: x['author'] != x['user_login'])). \
            add_action(LabelEncoderAction(targetCol='author_association', label_map=association_label_map)). \
            add_action(LabelEncoderAction(targetCol='close_login', label_map=close_login_map)). \
            add_action(FilterInvalidUserAction(targetCol=userCol)). \
            add_action(KeyWordReplaceAction(targetCol=textCol)). \
            add_action(KeyWordCountAction(targetCol=textCol)). \
            add_action(TokenizeAction(targetCol=textCol)). \
            add_action(CalEntropyAction(textCol, 'entropy', key_group_by='repo_full_name', cal_element=True))
        # add_action(CalEntropyAction(textCol, 'entropy_all', cal_outer=True, key_group_by='repo_full_name'))
        #
    # add_action(FlattenColAction(targetCol='author_association')). \

        """统计一些字段的分布"""

        # cols2 = ['count_talk', 'count_pic', 'count_link', 'count_block',
        #          'count_element', 'count_at', 'count_sentence', 'count_token',
        #          'entropy', 'author_association', 'close_login',
        #          'position']
        #
        # for col in cols2:
        #     processor.add_action(CalDistributionAction(targetCol=col,
        #                                                key_group_by='repo_full_name'))

        """删除一些不需要的字段"""
        drop_cols = ["repo_full_name", "id", "node_id", "user_login",
                     "created_at", "updated_at", "timelineitem_node", 'position', 'author',
                     'author_association']

        for col in drop_cols:
            processor.add_action(DropColAction(targetCol=col))

        # """对剩下的行数做归一化"""
        # cols = ['count_talk', 'count_pic', 'count_link', 'count_block',
        #         'count_element', 'count_at', 'count_sentence', 'count_token',
        #         'timeline_length', 'position_ratio', 'entropy']
        #
        # for col in cols:
        #     processor.add_action(NormalizationAction(col))

        """执行所有的action"""
        data = processor.execute(issueCommentData)
        print(data)
        """尝试用不同的据类算法做据类"""

        break

        # """先使用 k-means 聚类试试"""
        # try_kmeans(data, project)
        # analyze_kneams(data, project)

        """ 增加部分特征， 使用聚类k-prototypes试试 """
        # try_kprototypes(data, project)
        # analyze_kprototypes(data, project, 2)
        # analyze_kprototypes(data, project, 3)

        """尝试以信息熵为轴，计算每个特征的分桶情况"""
        # analyze_dis_by_col(data, project, 'entropy')
        # sample_low_data(data, project, 'entropy')
    #
    # plt.legend(loc=2)
    # plt.show()
