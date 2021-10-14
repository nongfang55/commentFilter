from processor.action.BasicAction import BasicAction


class DropNanAction(BasicAction):
    """用于去除 若干行的nan"""

    def process(self, df):
        df.dropna(subset=[self.targetCol], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def check_input(self):
        assert self.targetCol is not None
