from processor.action.BasicAction import BasicAction


class FlattenColAction(BasicAction):

    def process(self, df):

        """指定某一列， 为离散变量， 把列变成 one-hot 编码，
            并作为多列的形式呈现
        """
        labels = list(set(df[self.targetCol]))
        labels.sort()
        labels = set(labels)
        for label in labels:
            df[f'{self.targetCol}_{label}'] = df[self.targetCol].apply(lambda x: x == label)

        return df

    def check_input(self):
        assert self.newCols.__len__() == 0