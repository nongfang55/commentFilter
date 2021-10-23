import re

import nltk

from processor.action.BasicAction import BasicAction
from utils.StringKeyUtils import StringKeyUtils


class TokenizeAction(BasicAction):
    """用于统计文本中的句子数量， token数量"""

    def __init__(self, targetCol, *newCols, **kwargs):
        super().__init__(targetCol, *newCols, **kwargs)
        """
            newCols: 需要传入处理元素的col名称列表， 输入顺序参考处理顺序
            kwargs:  需要传入处理元素的指示信号， 
                    默认全部处理，否则依次取建判断处理
        """

        """
            处理顺序： 句子， token
        """

        self.processList = [StringKeyUtils.STR_INDICATE_SENTENCE,
                            StringKeyUtils.STR_INDICATE_TOKEN]

        self.invalidLine = ["", StringKeyUtils.STR_REPLACE_KEY_LINK,
                            StringKeyUtils.STR_REPLACE_KEY_BLOCK,
                            StringKeyUtils.STR_REPLACE_KEY_AT,
                            StringKeyUtils.STR_REPLACE_KEY_PIC,
                            StringKeyUtils.STR_REPLACE_KEY_TALK,
                            StringKeyUtils.STR_REPLACE_KEY_ELEMENT]

        if self.kwargs.__len__() == 0:
            for item in self.processList:
                self.kwargs[item] = True

        if self.newCols.__len__() == 0:
            """col的顺序需要和处理顺序相同"""
            self.newCols = []
            self.newCols.append(StringKeyUtils.STR_COUNT_SENTENCE)
            self.newCols.append(StringKeyUtils.STR_COUNT_TOKEN)

        self.check_input()

        """用于获取新增行名称的字典"""
        self.colNameDict = {StringKeyUtils.STR_INDICATE_SENTENCE: StringKeyUtils.STR_COUNT_SENTENCE,
                            StringKeyUtils.STR_INDICATE_TOKEN: StringKeyUtils.STR_COUNT_TOKEN}

        """用于获取处理的函数"""
        self.funcDict = {StringKeyUtils.STR_INDICATE_SENTENCE: self.count_sentence,
                         StringKeyUtils.STR_INDICATE_TOKEN: self.count_token}

        """关联新增的col名称"""
        index = 0
        for item in self.processList:
            if self.kwargs[item]:
                self.colNameDict[item] = self.newCols[index]
                index += 1

        """初始化punkt分割器"""
        self.sen_tokenizer = nltk.data.load(StringKeyUtils.STR_PATH_PUNTK)

    def process(self, df):

        for item in self.processList:
            if self.kwargs.get(item, False):
                """依次处理每个目标词"""
                df[self.colNameDict[item]] = df[self.targetCol].apply(lambda x: self.funcDict[item](x))

        return df

    def count_sentence(self, text):
        """计算句子的个数"""
        sentence_count = 0
        """先对text做分行"""
        lines = text.split('\n')
        for line in lines:
            line = line.strip(' \n\f\t\r')
            """如果只是落单的元素， 或者空行，直接忽略"""
            if line not in self.invalidLine:
                sentence_count += self.sen_tokenizer.tokenize(line).__len__()

        return sentence_count

    def count_token(self, text):
        """计算token个数, 不包括 comment 中的元素"""
        tokens_count = 0
        word_re = re.compile(r'[A-Za-z\-0-9\'_]+')
        words = word_re.findall(text)
        words = [word for word in words if word not in self.invalidLine]
        return words.__len__()

    def check_input(self):
        assert self.newCols.__len__() == self.kwargs.keys().__len__()
