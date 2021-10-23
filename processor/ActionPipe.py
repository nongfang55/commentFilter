from processor.action.BasicAction import BasicAction
from pandas import DataFrame


class ActionPipe:
    """接受各种action操作用于处理dataframe"""

    def __init__(self):
        self.pipe = []

    def add_action(self, action):
        if isinstance(action, BasicAction):
            self.pipe.append(action)
        return self

    def execute(self, df):
        """执行所有的 action"""
        if not isinstance(df, DataFrame):
            return df
        for action in self.pipe:
            df = action.process(df)
            print("action:", type(action), " shape:", df.shape)
        return df
