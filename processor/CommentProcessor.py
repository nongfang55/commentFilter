import pandas
from stanfordcorenlp import StanfordCoreNLP

from config.projectConfig import projectConfig
from processor.action.CalDistributionAction import CalDistributionAction
from processor.action.DropColAction import DropColAction
from processor.action.KeyWordCountAction import KeyWordCountAction
from processor.action.DropNanAction import DropNanAction
from processor.action.FilterInvalidUserAction import FilterInvalidUserAction
from processor.action.KeyWordReplaceAction import KeyWordReplaceAction
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

    processor.add_action(CalDistributionAction(targetCol='count_token',
                                               key_group_by='repo_full_name',
                                               value_type='type_discrete'))

    """执行所有的action"""
    data = processor.execute(rawData)

    print(data)
