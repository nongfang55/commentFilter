import os

import pandas
from stanfordcorenlp import StanfordCoreNLP

from config.projectConfig import projectConfig
from processor.action.CalDistributionAction import CalDistributionAction
from processor.action.DropColAction import DropColAction
from processor.action.KeyWordCountAction import KeyWordCountAction
from processor.action.DropNanAction import DropNanAction
from processor.action.FilterInvalidUserAction import FilterInvalidUserAction
from processor.action.KeyWordReplaceAction import KeyWordReplaceAction
from processor.action.NormalizationAction import NormalizationAction
from processor.action.TokenizeAction import TokenizeAction
from processor.ActionPipe import ActionPipe

if __name__ == "__main__":
    data_path = projectConfig.getSampleIssueCommentDataPath()
    rawData = pandas.read_csv(data_path, encoding='gbk')
    print(rawData)

    textCol = 'bodyText'
    userCol = 'login'

    processor = ActionPipe()
    processor.add_action(DropNanAction(targetCol=textCol)). \
        add_action(FilterInvalidUserAction(targetCol=userCol)). \
        add_action(KeyWordReplaceAction(targetCol=textCol)). \
        add_action(KeyWordCountAction(targetCol=textCol)). \
        add_action(TokenizeAction(targetCol=textCol))

    dropCols = ['pr', 'node_id', 'pr_author', 'login', 'bodyText']
    for col in dropCols:
        processor.add_action(DropColAction(targetCol=col))

    """ 统计以下字段的分布 """
    cols = ['count_talk', 'count_pic', 'count_link', 'count_block',
            'count_element', 'count_at', 'count_sentence', 'count_token']
    #
    # for col in cols:
    #     processor.add_action(CalDistributionAction(targetCol=col,
    #                                                key_group_by='repo_full_name'))

    """尝试做数据归一化"""
    for col in cols:
        processor.add_action(NormalizationAction(targetCol=col))

    """执行所有的action"""
    data = processor.execute(rawData)

    print(data)
