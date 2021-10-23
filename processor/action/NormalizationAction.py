from processor.action.BasicAction import BasicAction
import numpy


class NormalizationAction(BasicAction):
    """指定数据的某一列，
        对这一列的数据做标准归一化

        targetCol : 需要归一化的 col
        newCols : 不填
        kwargs: 不填
    """

    def process(self, df):
        mean = numpy.mean(df[self.targetCol])
        std = numpy.std(df[self.targetCol])
        df[self.targetCol] = df[self.targetCol].apply(
            lambda x: (x - mean) / std)
        return df

    def check_input(self):
        assert self.newCols.__len__() == 0
