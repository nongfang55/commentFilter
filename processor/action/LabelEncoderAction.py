import time

from processor.action.BasicAction import BasicAction
from utils.StringKeyUtils import StringKeyUtils


class LabelEncoderAction(BasicAction):
    """用于给离散值做编码， 编码的结果不包含大小顺序信息，只有单独的类别
    """

    def __init__(self, targetCol, *newCols, **kwargs):

        super().__init__(targetCol, *newCols, **kwargs)
        """  targetCol 输入需要处理的列 
             newCols 默认为空
             kwargs 输入参数 label_map 为一个字典变量，用于保存映射的关系
        """
        self.label_map = self.kwargs.get(StringKeyUtils.STR_KEY_LABEL_MAP, {})

    def process(self, df):
        labels = list(set(df[self.targetCol]))
        """按照字典序排序"""
        labels.sort()
        labels = set(labels)
        for index, label in enumerate(labels):
            self.label_map[label] = index

        """对目标的列做映射"""
        df[self.targetCol] = df[self.targetCol].apply(lambda x: self.label_map[x])
        return df

    def check_input(self):
        assert self.newCols.__len__() == 0