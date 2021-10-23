from processor.action.BasicAction import BasicAction


class FilterInvalidUserAction(BasicAction):
    """用于去除 一些无效的用户，包括被删除的用户，
        以及项目的社区机器人"""

    """手动维护的列表"""
    BOT_TABLE = ['stickler-ci', 'codecov-io', 'rails-bot', 'mention-bot',
             'babel-bot', 'symfony-skeleton-bot', 'akka-ci', 'buildsize',
             'stale', 'netty-bot', 'codecov', 'label-actions', 'salt-jenkins',
             'facebook-github-bot', 'reactjs-bot', 'pull-bot', 'googlebot',
             'mary-poppins', 'ngbot[bot]', 'ngbot', 'sklearn-lgtm', 'pep8speaks',
             'fastlane-bot-helper', 'netkins', 'GordonTheTurtle', 'lightbend-cla-validator',
             'sizebot', 'angular-automatic-lock-bot', 'codesandbox', 'jenkins4kodi', 'github-actions',
             'houndci-bot', 'joomla-cms-bot', 'CLAassistant', 'claassistantio']

    def process(self, df):

        """如果是社区机器人，那么用于名字在列表当中，
            如果是无效的用户，那么名字为na
        """
        self.check_input()

        # 去除已经删除的用户
        df.dropna(subset=[self.targetCol], inplace=True)

        # 去除社区机器人
        df['isBot'] = df[self.targetCol].apply(lambda x: x in self.BOT_TABLE)
        df = df.loc[df['isBot'] == False].copy(deep=True)
        df.drop(columns=['isBot'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def check_input(self):
        assert self.newCols.__len__() == 0