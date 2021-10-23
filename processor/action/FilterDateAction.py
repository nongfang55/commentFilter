import time

from processor.action.BasicAction import BasicAction
from utils.StringKeyUtils import StringKeyUtils


class FilterDateAction(BasicAction):
    """用于去除不在时间范围外面的数据
        默认是字符串类型
    """

    def __init__(self, targetCol, *newCols, **kwargs):

        super().__init__(targetCol, *newCols, **kwargs)
        """ 这里只加载一个变量， 是一个四元组的字符串
            如：  (start_year, start_month, end_year, end_month)
            实例： (2016, 1, 2020, 6)
        """
        self.dateRange = self.kwargs.get(StringKeyUtils.STR_KEY_DATE_RANGE, None)
        self.startYear = None
        self.startMonth = None
        self.endYear = None
        self.endMonth = None
        if len(self.dateRange) == 4:
            self.startYear, self.startMonth, self.endYear, self.endMonth = self.dateRange

    def judgeInRange(self, item):
        item_date = time.strptime(item, "%Y-%m-%d %H:%M:%S")
        """这里比较的时候， 是已经默认字段有效了"""
        if self.startYear * 12 + self.startMonth <= item_date.tm_year * 12 + item_date.tm_mon  \
                <= self.endYear * 12 + self.endMonth:
            return True
        else:
            return False

    def process(self, df):

        """  如果没有设置， 那么就直接返回
        """
        self.check_input()
        if self.startMonth is None:
            return df

        # 去除没有时间的数据
        df.dropna(subset=[self.targetCol], inplace=True)

        # 去除不在目标时间段的时间
        tempCol = StringKeyUtils.STR_KEY_INDICATE
        df[tempCol] = df[self.targetCol].apply(lambda x: self.judgeInRange(x))
        df = df.loc[df[tempCol] == True].copy(deep=True)
        df.drop(columns=[tempCol], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def check_input(self):
        assert self.newCols.__len__() == 0