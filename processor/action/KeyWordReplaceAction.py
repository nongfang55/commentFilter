import re

from processor.action.BasicAction import BasicAction
from utils.StringKeyUtils import StringKeyUtils


class KeyWordReplaceAction(BasicAction):

    """用于替换句子中的 谈话引用， 关键字， 代码,  @用户， url等"""

    def __init__(self, targetCol, *newCols, **kwargs):

        super().__init__(targetCol, *newCols, **kwargs)

        """
            处理顺序： 谈话引用， 照片， 链接，大代码块， 代码元素， @用户
        """

        self.processList = [StringKeyUtils.STR_INDICATE_TALK, StringKeyUtils.STR_INDICATE_PIC,
                            StringKeyUtils.STR_INDICATE_LINK, StringKeyUtils.STR_INDICATE_BLOCK,
                            StringKeyUtils.STR_INDICATE_ELEMENT, StringKeyUtils.STR_INDICATE_AT]

        """
            kwargs: 输入需要处理的元素的指示变量， 默认全部处理，否则依次取建判断处理
        """
        if self.kwargs.__len__() == 0:
            for item in self.processList:
                self.kwargs[item] = True

        """用于存储正则的pattern"""
        self.patternDict = {StringKeyUtils.STR_INDICATE_TALK: r'(^>[^\n]*\n)+',
                            StringKeyUtils.STR_INDICATE_PIC: r'^!\[.*\]\(.*\)',
                            StringKeyUtils.STR_INDICATE_LINK: r'http[s]?://(?:[a-zA-Z]|[0-9]|[#$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                            StringKeyUtils.STR_INDICATE_BLOCK: r'```.*?```',
                            StringKeyUtils.STR_INDICATE_ELEMENT: r'`[^`]+`',
                            StringKeyUtils.STR_INDICATE_AT: r'@[a-z0-9\-/]+'}

        """用于存储正则的flag"""
        self.flagDict = {StringKeyUtils.STR_INDICATE_TALK: re.I | re.S | re.M,
                         StringKeyUtils.STR_INDICATE_PIC: re.I | re.M,
                         StringKeyUtils.STR_INDICATE_LINK: re.I | re.M,
                         StringKeyUtils.STR_INDICATE_BLOCK: re.I | re.S,
                         StringKeyUtils.STR_INDICATE_ELEMENT: re.I,
                         StringKeyUtils.STR_INDICATE_AT: re.I}

        """用于替换正则的单词"""
        """加空格是便于分开"""
        self.wordDict = {StringKeyUtils.STR_INDICATE_TALK: " " + StringKeyUtils.STR_REPLACE_KEY_TALK + " ",
                         StringKeyUtils.STR_INDICATE_PIC: " " + StringKeyUtils.STR_REPLACE_KEY_PIC + " ",
                         StringKeyUtils.STR_INDICATE_LINK: " " + StringKeyUtils.STR_REPLACE_KEY_LINK + " ",
                         StringKeyUtils.STR_INDICATE_BLOCK: " " + StringKeyUtils.STR_REPLACE_KEY_BLOCK + " ",
                         StringKeyUtils.STR_INDICATE_ELEMENT: " " + StringKeyUtils.STR_REPLACE_KEY_ELEMENT + " ",
                         StringKeyUtils.STR_INDICATE_AT: " " + StringKeyUtils.STR_REPLACE_KEY_AT + " "}

    def process(self, df):

        self.check_input()
        for item in self.processList:
            if self.kwargs.get(item, False):
                self.replace(df, self.targetCol, self.patternDict[item], self.wordDict[item], self.flagDict[item])

        return df

    def replace(self, df, targetCol, pattern, word, flag):
        """根据提供的pattern 和 flag 在目标的col 上进行正则的替换"""
        df[targetCol] = df[targetCol].apply(lambda x: re.sub(pattern, word, x, flags=flag))

    def check_input(self):
        assert self.newCols.__len__() == 0
