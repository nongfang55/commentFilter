
import os

import pandas

from config.projectConfig import projectConfig
from processor.ActionPipe import ActionPipe
from processor.action.CalDistributionAction import CalDistributionAction
from processor.action.CommonFilterAction import CommonFilterAction
from processor.action.DropColAction import DropColAction
from processor.action.DropNanAction import DropNanAction
from processor.action.FilterDateAction import FilterDateAction
from processor.action.FilterInvalidUserAction import FilterInvalidUserAction
from processor.action.KeyWordCountAction import KeyWordCountAction
from processor.action.KeyWordReplaceAction import KeyWordReplaceAction
from processor.action.LabelEncoderAction import LabelEncoderAction
from processor.action.NormalizationAction import NormalizationAction
from processor.action.TokenizeAction import TokenizeAction
from utils.pandasHelper import pandasHelper
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt


"""尝试提取一些comment的特征，然后用不同算法做据类的尝试"""

def loadIssueCommentData(projects):
    issueDataPath = projectConfig.getIssueCommentPath(isLocal=False)

    data = None
    for project in projects:
        filename = os.path.join(issueDataPath, f'ALL_{project}_data_issuecomment.tsv')
        df = pandasHelper().readTSVFile(fileName=filename, sep='\t', header=pandasHelper.INT_READ_FILE_WITH_HEAD)
        if data is None:
            data = df
        else:
            data = pandas.concat([data, df])
    return data

def try_kmeans(X, label):
    """尝试使用 kmeans 算法"""
    scores = []
    for n_cluster in range(2, 10):
        y_pred = KMeans(n_clusters=n_cluster, random_state=9, n_jobs=4).fit_predict(X)
        # score = metrics.calinski_harabasz_score(X, y_pred) # ch-index
        score = metrics.silhouette_score(X, y_pred,metric='euclidean')  # 样本平均轮廓系数
        scores.append(score)

    plt.plot(range(2, 10), scores, label=label)

def analyze_keams(X, label):
    n_clusters = 4
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


if __name__ == "__main__":
    projects = ['akka', 'cakephp', 'scikit-learn', 'symfony', 'xbmc']
    projects = ['symfony']
    for project in projects:
        print("==" * 50)
        print(f"project:{project}")
        issueCommentData = loadIssueCommentData([project])

        """对issue comment的一些特征做预处理"""
        textCol = 'body'
        userCol = 'user_login'
        dateCol = 'created_at'

        association_label_map = {}

        processor = ActionPipe()
        processor.add_action(FilterDateAction(targetCol=dateCol, dateRange=(2017, 1, 2020, 6))).\
            add_action(DropNanAction(targetCol=textCol)). \
            add_action(CommonFilterAction(targetCol='author_association',
                                          filter_func=lambda x: x != 'CONTRIBUTOR' and x != 'COLLABORATOR')). \
            add_action(LabelEncoderAction(targetCol='author_association', label_map=association_label_map)). \
            add_action(FilterInvalidUserAction(targetCol=userCol)). \
            add_action(KeyWordReplaceAction(targetCol=textCol)). \
            add_action(KeyWordCountAction(targetCol=textCol)). \
            add_action(TokenizeAction(targetCol=textCol))

        """删除一些不需要的字段"""
        drop_cols = ["repo_full_name", "pull_number", "id", "node_id", "user_login",
                     "created_at", "updated_at", "body", "author_association"]

        for col in drop_cols:
            processor.add_action(DropColAction(targetCol=col))

        """对剩下的行数做归一化"""
        cols = ['count_talk', 'count_pic', 'count_link', 'count_block',
                'count_element', 'count_at', 'count_sentence', 'count_token']

        for col in cols:
            processor.add_action(NormalizationAction(col))

        """执行所有的action"""
        data = processor.execute(issueCommentData)
        print(data)
        """尝试用不同的据类算法做据类"""

        """先使用 k-means 聚类试试"""
        # try_kmeans(data, project)
        analyze_keams(data, project)

    # plt.legend(loc=2)
    # plt.show()