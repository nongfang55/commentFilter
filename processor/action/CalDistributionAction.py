from processor.action.BasicAction import BasicAction
from utils.SingleDataAnalyzer import SingleDataAnalyzer
from utils.StringKeyUtils import StringKeyUtils
import pandas as pd

from utils.ExcelHelper import ExcelHelper


class CalDistributionAction(BasicAction):
    """用于统计某一行的数据的分布， 统计的结果保存在一个excel中，
        其中sheet的名字就是col的名字， 并且可以指定某一列作为主键"""

    """对于连续的值， 会就近变成整数"""

    """这个操作主要是用于统计， 不会影响到当前的df"""

    def __init__(self, targetCol, *newCols, **kwargs):

        super().__init__(targetCol, *newCols, **kwargs)
        """这里加载参数中是否有指定key, 是否有excel的名称"""
        """默认认为处理的方式为连续值变量"""
        self.valueType = self.kwargs.get(StringKeyUtils.STR_KEY_VALUE_TYPE, StringKeyUtils.STR_VALUE_TYPE_CONTINUOUS)
        self.groupKey = self.kwargs.get(StringKeyUtils.STR_KEY_GROUP_BY, None)
        self.excelName = self.kwargs.get(StringKeyUtils.STR_KEY_EXCEL_NAME, StringKeyUtils.STR_KEY_DEFAULT_EXCEL_NAME)
        self.sheetName = self.kwargs.get(StringKeyUtils.STR_KEY_SHEET_NAME, targetCol)

    def process(self, df):
        """对指定的 dataframe 中的列进行数据的统计"""
        disList = []
        if self.groupKey is not None:
            """处理有主键的值"""
            disList = self.processGroupData(df)
        else:
            disList = self.processSingleData(df)

        """对收集到的数据处理"""
        disDict = self.processDistribution(disList)
        """输出一个DataFrame到一个excel"""
        self.writeResult(disDict)

        """对这个数据做更加详尽的分析"""
        """如果是连续的变量， 那么可以做进一步的分析"""
        if self.valueType == StringKeyUtils.STR_VALUE_TYPE_CONTINUOUS:
            self.analyzeResult(disDict)

        return df

    def analyzeResult(self, df):
        """对于之前的 dataframe 做更加进一步的分析"""
        weights = list(df.columns[1:])
        labels = list(df[self.groupKey])
        datas = []
        for index, label in enumerate(labels):
            data = list(df.iloc[index])[1:]
            datas.append(data)

        SingleDataAnalyzer().process(weights=weights, nums=datas, labels=labels,
                                     excelName=self.excelName, sheetName=f'f_{self.targetCol}')

    def processDistribution(self, disList):
        """收集到统计的分布，做统一, 生成一个DataFrame"""
        valueDict = {}
        cols = []
        if self.valueType == StringKeyUtils.STR_VALUE_TYPE_CONTINUOUS:
            """连续值的处理方式为，先统一最大的数据和最小的数据，然后一排划开"""
            upper = None
            lower = None
            for key, disDict in disList:
                if isinstance(disDict, dict):
                    if upper is None or upper < max(disDict.keys()):
                        upper = max(disDict.keys())
                    if lower is None or lower > min(disDict.keys()):
                        lower = min(disDict.keys())
            cols.extend([int(x) for x in range(lower, upper + 1)])
        else:
            for key, disDict in disList:
                if isinstance(disDict, dict):
                    cols.extend(disDict.keys())

            """所有的离散值按照字典序排序"""
            cols = list(set(cols))
            cols.sort()

        valueDict[self.groupKey] = []
        for col in cols:
            valueDict[col] = []
        for key, disDict in disList:
            valueDict[self.groupKey].append(key)
            for col in cols:
                valueDict[col].append(disDict.get(col, 0))
        disDict = pd.DataFrame(valueDict)
        return disDict

    def check_input(self):
        assert self.targetCol is not None

    def processGroupData(self, df):
        """处理有主键的数据"""
        disList = []
        for key, tempDf in dict(list(df.groupby(self.groupKey))).items():
            disDict = {}  # 用于保存值的字典
            values = [x for x in tempDf[self.targetCol]]
            if self.valueType == StringKeyUtils.STR_VALUE_TYPE_CONTINUOUS:
                """连续值特征转化为整数"""
                values = [int(x) for x in values]
            else:
                """离散值转化为字符串"""
                values = [str(x) for x in values]

            for value in values:
                disDict[value] = disDict.get(value, 0) + 1
            disList.append((key, disDict))
        return disList

    def processSingleData(self, df):
        """处理没有主键的数据"""
        disList = []
        disDict = {}  # 用于保存值的字典
        values = [x for x in df[self.targetCol]]
        if self.valueType == StringKeyUtils.STR_VALUE_TYPE_CONTINUOUS:
            """连续值特征转化为整数"""
            values = [int(x) for x in values]
        else:
            """离散值转化为字符串"""
            values = [str(x) for x in values]

        for value in values:
            disDict[value] = disDict.get(value, 0) + 1
        disList.append((None, disDict))
        return disList

    def writeResult(self, result):
        """把dataFrame写excel中"""
        result = pd.DataFrame(result.values.T, index=result.columns, columns=result.index)  # 转置
        result[StringKeyUtils.STR_KEY_INDEX] = result.index
        sortCol = [x for x in result.columns.copy()]
        sortCol.remove(StringKeyUtils.STR_KEY_INDEX)
        sortCol.insert(0, StringKeyUtils.STR_KEY_INDEX)
        result = result[sortCol]
        helper = ExcelHelper()
        helper.writeDataFrameToExcel(fileName=self.excelName, sheetName=self.sheetName,
                                     dataframe=result)
