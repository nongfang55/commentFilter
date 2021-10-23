from processor.action.BasicAction import BasicAction
from utils.StringKeyUtils import StringKeyUtils


class CommonFilterAction(BasicAction):
    """通用的过滤的算子
        过滤的算子自己提供
        targetCol: 需要过滤的目标行数
        newCols : 为空
        kwargs: 需要提供过滤函数
                key_fun_filter  这个函数需要在保留的字段上面返回为True, 在不需要的字段上面范围为False
    """

    def __init__(self, targetCol, *newCols, **kwargs):

        super().__init__(targetCol, *newCols, **kwargs)
        """获取判断的函数"""
        self.func = kwargs.get(StringKeyUtils.STR_KEY_FUN_FILTER, None)

    def process(self, df):
        """如果没有提供函数， 直接返回"""
        if self.func is None:
            return df

        if self.targetCol is not None:
            # 去除返回值不为True的字段
            tempCol = StringKeyUtils.STR_KEY_INDICATE
            df[tempCol] = df[self.targetCol].apply(lambda x: self.func(x))
            df = df.loc[df[tempCol] == True].copy(deep=True)
            df.drop(columns=[tempCol], inplace=True)
            df.reset_index(drop=True, inplace=True)
        else:
            """在全局做"""
            tempCol = StringKeyUtils.STR_KEY_INDICATE
            df[tempCol] = df.apply(lambda x: self.func(x), axis=1)
            df = df.loc[df[tempCol] == True].copy(deep=True)
            df.drop(columns=[tempCol], inplace=True)
            df.reset_index(drop=True, inplace=True)

        return df

    def check_input(self):
        assert self.targetCol is not None
