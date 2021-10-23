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
        pullRequestData.columns = ['pull_number', 'author']
        issueCommentData = pandas.merge(issueCommentData, pullRequestData, on='pull_number')

        # timelineData = pandasHelper().readTSVFile(fileName=timeline_filename,
        #                                           sep='\t', header=pandasHelper.INT_READ_FILE_WITH_HEAD)
        # timelineData['login'] = timelineData['origin'].apply(lambda x: PRTimeLineRelation.parser(x).user_login)
        #
        # """计算每一个PR的事件线的长度, 以及issuecomment所在的位置的比例，
        #     也顺带记录每个PR的 closed 的人的名字"""
        # pr_len_dict = {}
        # pr_close_login_dict = {}
        # for pr_node, tempDf in dict(list(timelineData.groupby('pullrequest_node'))).items():
        #     pr_len_dict[pr_node] = max(tempDf['position'])
        #     df_t = tempDf.loc[tempDf['typename'] == 'ClosedEvent']
        #     if df_t.shape[0] > 0:
        #         """存在关闭的事件"""
        #         pr_close_login_dict[pr_node] = getattr(df_t.iloc[0], "login")
        #
        # """加载 timeline 的数据后， 把两个数据做join"""
        # timelineData['timeline_length'] = timelineData.apply(
        #     lambda x: pr_len_dict.get(x['pullrequest_node'], numpy.NAN), axis=1)
        # timelineData['close_login'] = timelineData.apply(
        #     lambda x: pr_close_login_dict.get(x['pullrequest_node'], numpy.NAN), axis=1)
        # timelineData = timelineData.loc[timelineData['typename'] == 'IssueComment'].copy(deep=True)
        # timelineData = timelineData[['timelineitem_node', 'position', 'timeline_length', 'close_login']]
        # issueCommentData = pandas.merge(issueCommentData, timelineData, how='inner',
        #                                 left_on='node_id', right_on='timelineitem_node')
        # issueCommentData['position_ratio'] = issueCommentData.apply(lambda x: x['position'] / x['timeline_length'],
        #                                                             axis=1)
        # issueCommentData['close_login'] = issueCommentData.apply(lambda x: x['close_login'] == x['user_login'], axis=1)


        if data is None:
            data = issueCommentData
        else:
            data = pandas.concat([data, issueCommentData])

    return data


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
    # projects = ['akka', 'cakephp', 'scikit-learn', 'symfony', 'xbmc']
    projects = ['opencv', 'cakephp', 'akka', 'xbmc', 'babel', 'symfony', 'brew',
                'django', 'netty', 'scikit-learn', 'next.js', 'angular', 'moby',
                'metasploit-framework', 'Baystation12', 'react', 'pandas',
                'grafana', 'salt', 'joomla-cms']

    # projects = ['akka', 'cakephp']

    issueCommentData = loadIssueCommentData(projects)

    """对issue comment的一些特征做预处理"""
    textCol = 'body'
    userCol = 'user_login'
    dateCol = 'created_at'

    """开发者身份映射表"""
    association_label_map = {}
    """是否为合入者映射表"""
    close_login_map = {}

    """初始化处理流水线"""
    processor = ActionPipe()

    """处理2017年1月到2020年6月的数据"""
    processor.add_action(FilterDateAction(targetCol=dateCol, dateRange=(2017, 1, 2020, 6)))

    """处理内容为NaN的文本"""
    processor.add_action(DropNanAction(targetCol=textCol))

    """处理为COLLABORATOR的用户, 为作者的用户, 社区机器人，删除账号的用户"""
    processor.add_action(CommonFilterAction(targetCol='author_association',
                                            filter_func=lambda x: x != 'COLLABORATOR')). \
        add_action(FilterInvalidUserAction(targetCol=userCol)) .\
        add_action(CommonFilterAction(targetCol=None, filter_func=lambda x: x['author'] != x['user_login']))

    """离散值映射"""
    processor.add_action(LabelEncoderAction(targetCol='author_association', label_map=association_label_map))
    # . \
    #     add_action(LabelEncoderAction(targetCol='close_login', label_map=close_login_map))

    """抽取评论中的关键词"""
    processor.add_action(KeyWordReplaceAction(targetCol=textCol))

    # . \
    # add_action(KeyWordCountAction(targetCol=textCol)). \
    # add_action(TokenizeAction(targetCol=textCol))

    for cal_element in [True]:
        for cal_unknown in [True]:
            for group_unknown in [True]:
                processor.add_action(CalEntropyAction(textCol, f'entropy_{cal_element}_{cal_unknown}_{group_unknown}',
                                                      key_group_by='repo_full_name', cal_element=cal_element,
                                                      cal_unknown=cal_unknown, group_unknown=group_unknown))

    """统计一些字段的分布"""
    cal_dis_col = []
    for cal_element in [True]:
        for cal_unknown in [True]:
            for group_unknown in [True]:
                cal_dis_col.append(f'entropy_{cal_element}_{cal_unknown}_{group_unknown}')

    # for col in cal_dis_col:
    #     processor.add_action(CalDistributionAction(targetCol=col, key_group_by='repo_full_name'))

    """执行所有的action"""
    data = processor.execute(issueCommentData)
    print(data)