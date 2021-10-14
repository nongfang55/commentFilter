
class BasicAction:

    """构建处理的算子，用于比较方便的出路特征或者增加特征，
        这样便于后面算法的特征的迭代"""

    def __init__(self, targetCol, *newCols, **kwargs):
        self.targetCol = targetCol
        self.newCols = newCols
        self.kwargs = kwargs

    def process(self, df):
        """处理的内容都是DataFrame
           df 需要处理的DF
           targetCol 目标处理的列
           newCols 预计添加的新列
        """
        pass

    def check_input(self):
        """用于判断输入参数是否正确"""
        raise Exception('stub!')
