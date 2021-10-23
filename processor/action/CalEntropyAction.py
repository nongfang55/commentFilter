import math
import re

import nltk

from processor.action.BasicAction import BasicAction
from utils.StringKeyUtils import StringKeyUtils
from nltk.stem import PorterStemmer


class CalEntropyAction(BasicAction):

    """给定某一列的文本， 计算该文本中的信息熵"""

    def __init__(self, targetCol, *newCols, **kwargs):
        super().__init__(targetCol, *newCols, **kwargs)
        """
            targetCols: 目标处理列
            newCols: 输出的列名
            kwargs:  
                    filter_word_count :计算信息熵时候对低频词的过滤数量
                    cal_element : 是否计算文本中的元素
                    cal_outer : 是否计算低频词
                    key_col : 是否计算一个范围内的数值
            
        """

        self.invalidLine = [StringKeyUtils.STR_REPLACE_KEY_LINK,
                            StringKeyUtils.STR_REPLACE_KEY_BLOCK,
                            StringKeyUtils.STR_REPLACE_KEY_AT,
                            StringKeyUtils.STR_REPLACE_KEY_PIC,
                            StringKeyUtils.STR_REPLACE_KEY_TALK,
                            StringKeyUtils.STR_REPLACE_KEY_ELEMENT]

        self.word_count_map = {}  # 用于存放每个单词出现的频率

        self.total_count = 0  # 所有出现的有效 token的数量和

        self.tempCol = "_token_text"

        self.filter_word_count = self.kwargs.get(StringKeyUtils.STR_KEY_FILTER_WORD_COUNT, 3)  # 默认过滤低频单词数
        self.cal_element = self.kwargs.get(StringKeyUtils.STR_KEY_CAL_ELEMENT, True)    # 是否考虑元素
        self.cal_unknown = self.kwargs.get(StringKeyUtils.STR_KEY_CAL_UNKNOWN, False)   # 是否计算未知词
        self.groupKey = self.kwargs.get(StringKeyUtils.STR_KEY_GROUP_BY, None)  # groupby 的主键
        self.group_unknown = self.kwargs.get(StringKeyUtils.STR_KEY_GROUP_UNKNOWN, False)  # 配合cal_outer

        self.check_input()

        """初始化punkt分割器"""
        self.sen_tokenizer = nltk.data.load(StringKeyUtils.STR_PATH_PUNTK)

        """基于SNOWball 的词干提取"""
        self.stemmer = PorterStemmer()

    def token(self, text):
        """分词"""
        word_re = re.compile(r'[A-Za-z\-0-9\'_]+')
        words = word_re.findall(text)

        """单词转小写， 词干还原"""
        words = [self.stemmer.stem(x.lower()) for x in words]

        return words

    def cal(self, text):
        entropy = 0  # 这里直接指数相加， 防止浮点数计算带来的问题
        for word in text:
            count = self.word_count_map.get(word, -1)
            if count == -1:
                if self.cal_unknown:
                    """如果计算低频词"""
                    if self.group_unknown:
                        """如果未知词算总体的分布"""
                        entropy += math.log2(self.total_count * 1.0 / self.word_count_map.get(
                            StringKeyUtils.STR_KEY_TOKEN_UNKNOWN))
                    else:
                        """如果只计算单次出现"""
                        entropy += math.log2(self.total_count / 1)
            else:
                entropy += math.log2(self.total_count * 1.0 / count)

        return entropy

    def processText(self, texts):
        """用于处理text 列表， 返回每个text的信息熵"""

        """计算需要清空"""
        self.word_count_map.clear()
        self.total_count = 0

        """如果不计算元素， 那么现在就滤掉"""
        if not self.cal_element:
            texts = [[x for x in text if x not in self.invalidLine] for text in texts]

        for text in texts:
            for token in text:
                self.word_count_map[token] = self.word_count_map.get(token, 0) + 1

        """过滤频次过低的单词, 计算每个单词出现的概率"""
        del_words = []
        del_word_num = 0  # 统计所有未知词的总数

        for k, v in self.word_count_map.items():
            if v < self.filter_word_count:
                del_words.append(k)
                del_word_num += v

        """删除低频词, 添加未知词"""
        for k in del_words:
            self.word_count_map.pop(k)

        self.total_count = sum(self.word_count_map.values())

        self.word_count_map[StringKeyUtils.STR_KEY_TOKEN_UNKNOWN] = del_word_num

        """根据计算每个文本的信息熵"""
        entropys = [self.cal(text) for text in texts]

        return entropys

    def processSingleData(self, df):
        """计算每个文本的信息熵"""
        texts = [x.split(' ') for x in list(df[self.tempCol])]
        entropys = self.processText(texts)
        df[self.newCols[0]] = entropys
        return df

    def processGroupData(self, df):
        resultsMap = {}  # 用于存放每个group的值， 最后再统一的加上去
        keys = []

        for key, tempDf in dict(list(df.groupby(self.groupKey))).items():

            """计算每个文本的信息熵"""
            texts = [x.split(' ') for x in list(tempDf[self.tempCol])]
            entropys = self.processText(texts)

            """记录中间结果"""
            resultsMap[key] = entropys
            keys.append(key)

        resultList = []
        for key in keys:
            resultList.extend(resultsMap[key])
        df[self.newCols[0]] = resultList

        return df

    def process(self, df):

        """先对目标的列进行分词, 词干还原"""
        df[self.tempCol] = df[self.targetCol].apply(lambda x: ' '.join(self.token(x)))

        if self.groupKey is not None:
            """处理有主键的值"""
            df = self.processGroupData(df)
        else:
            df = self.processSingleData(df)

        """删除临时col"""
        df.drop(self.tempCol, axis=1, inplace=True)
        return df

    def check_input(self):
        assert self.newCols.__len__() == 1
