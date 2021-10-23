import os

import pandas
from stanfordcorenlp import StanfordCoreNLP

from config.projectConfig import projectConfig
from processor.action.CalDistributionAction import CalDistributionAction
from processor.action.DropColAction import DropColAction
from processor.action.FilterDateAction import FilterDateAction
from processor.action.KeyWordCountAction import KeyWordCountAction
from processor.action.DropNanAction import DropNanAction
from processor.action.FilterInvalidUserAction import FilterInvalidUserAction
from processor.action.KeyWordReplaceAction import KeyWordReplaceAction
from processor.action.TokenizeAction import TokenizeAction
from processor.ActionPipe import ActionPipe
from utils.pandasHelper import pandasHelper


def loadIssueCommentData():
    projects = ['akka', 'cakephp', 'scikit-learn', 'symfony', 'xbmc']
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

if __name__ == "__main__":

    issueCommentData = loadIssueCommentData()
    textCol = 'body'
    userCol = 'user_login'
    dateCol = 'created_at'

    processor = ActionPipe()
    processor.add_action(FilterDateAction(targetCol=dateCol, dateRange=(2017, 1, 2020, 6))).\
        add_action(DropNanAction(targetCol=textCol)). \
        add_action(FilterInvalidUserAction(targetCol=userCol)). \
        add_action(KeyWordReplaceAction(targetCol=textCol)). \
        add_action(KeyWordCountAction(targetCol=textCol)). \
        add_action(TokenizeAction(targetCol=textCol))

    cols = ['count_talk', 'count_pic', 'count_link', 'count_block',
            'count_element', 'count_at', 'count_sentence', 'count_token']

    for col in cols:
        processor.add_action(CalDistributionAction(targetCol=col,
                                                   key_group_by='repo_full_name'))

    """执行所有的action"""
    data = processor.execute(issueCommentData)
    print(data)