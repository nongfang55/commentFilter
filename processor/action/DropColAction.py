from processor.action.BasicAction import BasicAction


class DropColAction(BasicAction):
    """用于去除 某一行"""

    def process(self, df):
        df.drop(self.targetCol, axis=1, inplace=True)
        return df

    def check_input(self):
        assert self.targetCol is not None
