import re

from processor.action.BasicAction import BasicAction
from processor.action.StringKeyUtils import StringKeyUtils


class KeyWordCountAction(BasicAction):
    """用于统计句子中的 谈话引用， 关键字， 代码,  @用户， url等"""

    def __init__(self, targetCol, *newCols, **kwargs):
        super().__init__(targetCol, *newCols, **kwargs)
        """
            newCols: 需要传入处理元素的col名称列表， 输入顺序参考处理顺序
            kwargs:  需要传入处理元素的指示信号， 
                    默认全部处理，否则依次取建判断处理
        """

        """
            处理顺序： 谈话引用， 照片， 链接，大代码块， 代码元素， @用户
        """

        self.processList = [StringKeyUtils.STR_INDICATE_TALK, StringKeyUtils.STR_INDICATE_PIC,
                            StringKeyUtils.STR_INDICATE_LINK, StringKeyUtils.STR_INDICATE_BLOCK,
                            StringKeyUtils.STR_INDICATE_ELEMENT, StringKeyUtils.STR_INDICATE_AT]

        if self.kwargs.__len__() == 0:
            for item in self.processList:
                self.kwargs[item] = True

        if self.newCols.__len__() == 0:
            """col的顺序需要和处理顺序相同"""
            self.newCols = []
            self.newCols.append(StringKeyUtils.STR_COUNT_TALK)
            self.newCols.append(StringKeyUtils.STR_COUNT_PIC)
            self.newCols.append(StringKeyUtils.STR_COUNT_LINK)
            self.newCols.append(StringKeyUtils.STR_COUNT_BLOCK)
            self.newCols.append(StringKeyUtils.STR_COUNT_ELEMENT)
            self.newCols.append(StringKeyUtils.STR_COUNT_AT)

        self.check_input()

        """用于获取目标词的字典"""
        self.wordDict = {StringKeyUtils.STR_INDICATE_TALK: StringKeyUtils.STR_REPLACE_KEY_TALK,
                         StringKeyUtils.STR_INDICATE_PIC: StringKeyUtils.STR_REPLACE_KEY_PIC,
                         StringKeyUtils.STR_INDICATE_LINK: StringKeyUtils.STR_REPLACE_KEY_LINK,
                         StringKeyUtils.STR_INDICATE_BLOCK: StringKeyUtils.STR_REPLACE_KEY_BLOCK,
                         StringKeyUtils.STR_INDICATE_ELEMENT: StringKeyUtils.STR_REPLACE_KEY_ELEMENT,
                         StringKeyUtils.STR_INDICATE_AT: StringKeyUtils.STR_REPLACE_KEY_AT}

        """用于获取新增行名称的字典"""
        self.colNameDict = {StringKeyUtils.STR_INDICATE_TALK: StringKeyUtils.STR_COUNT_TALK,
                            StringKeyUtils.STR_INDICATE_PIC: StringKeyUtils.STR_COUNT_PIC,
                            StringKeyUtils.STR_INDICATE_LINK: StringKeyUtils.STR_COUNT_LINK,
                            StringKeyUtils.STR_INDICATE_BLOCK: StringKeyUtils.STR_COUNT_BLOCK,
                            StringKeyUtils.STR_INDICATE_ELEMENT: StringKeyUtils.STR_COUNT_ELEMENT,
                            StringKeyUtils.STR_INDICATE_AT: StringKeyUtils.STR_COUNT_AT}

        """关联新增的col名称"""
        index = 0
        for item in self.processList:
            if self.kwargs[item]:
                self.colNameDict[item] = self.newCols[index]
                index += 1

    def process(self, df):

        for item in self.processList:
            if self.kwargs.get(item, False):
                """依次处理每个目标词"""
                self.process_col(df, self.targetCol, self.colNameDict[item], self.wordDict[item])

        return df

    def process_col(self, df, targetCol, outputCol, targetWord):
        """匹配全文中有这些词的次数"""
        word_pattern = re.compile(targetWord)
        df[outputCol] = df[targetCol].apply(lambda x: word_pattern.findall(x).__len__())

    def check_input(self):
        assert self.newCols.__len__() == self.kwargs.keys().__len__()
