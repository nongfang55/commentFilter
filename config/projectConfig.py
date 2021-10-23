import os


class projectConfig:

    projectName = 'commentFilter'

    PATH_CHROME_DATA = 'data' + os.sep + 'chrome' + os.sep + 'chromium_conversations_annotations.csv'
    PATH_SAMPLE_ISSUE_COMMENT = 'data' + os.sep + 'comment' + os.sep + 'sampleIssueComment_2.csv'

    PATH_ISSUE_COMMENT_PATH = 'data' + os.sep + 'train' + os.sep + 'issueCommentData'
    PATH_DATA_TRAIN = 'data' + os.sep + 'train'
    PATH_COMMIT_FILE = 'data' + os.sep + 'train' + os.sep + 'commitFileData'
    PATH_SEAA = 'data' + os.sep + 'SEAA'
    PATH_PULL_REQUEST = 'data' + os.sep + 'train' + os.sep + 'pullRequestData'
    PATH_PR_CHANGE_FILE = 'data' + os.sep + 'train' + os.sep + 'prChangeFile'
    PATH_REVIEW = 'data' + os.sep + 'train' + os.sep + 'reviewData'
    PATH_TIMELINE = 'data' + os.sep + 'train' + os.sep + 'prTimeLineData'
    PATH_REVIEW_COMMENT = 'data' + os.sep + 'train' + os.sep + 'reviewCommentData'
    PATH_REVIEW_CHANGE = 'data' + os.sep + 'train' + os.sep + 'reviewChangeData'
    PATH_PULL_REQUEST_DISTANCE = 'data' + os.sep + 'train' + os.sep + 'prDistance'
    PATH_USER_FOLLOW_RELATION = 'data' + os.sep + 'train' + os.sep + 'userFollowRelation'
    PATH_USER_ORGANIZATION_RELATION = 'data' + os.sep + 'train' + os.sep + 'userOrganizationRelation'
    PATH_USER_CONTRIBUTION_RELATION = 'data' + os.sep + 'train' + os.sep + 'userContributionRelation'
    PATH_USER_WATCH_REPO_RELATION = 'data' + os.sep + 'train' + os.sep + 'userWatchRepoRelation'
    PATH_STOP_WORD_STEM = 'data' + os.sep + 'stemStopWord.txt'
    PATH_COMMENT_KEY_WORD = 'data' + os.sep + 'train' + os.sep + 'commentKeyWord'
    PATH_COMMIT_RELATION = 'data' + os.sep + 'train' + os.sep + 'prCommitRelation'

    @staticmethod
    def getLocalPath():
        """取得当前项目的更目录"""
        curPath = os.path.abspath(os.path.dirname(__file__))
        projectName = projectConfig.projectName
        localPath = os.path.join(curPath.split(projectName)[0], projectName)  # 获取myProject，也就是项目的根路径
        return localPath

    @staticmethod
    def getExportPath():
        """由于现在的数据太大了，从其他项目直接读数据
        ，实现复用节约磁盘的空间
        """
        exportPath = r'C:\Users\ThinkPad\Desktop\Python\re4\review'
        return exportPath

    @staticmethod
    def getRootPath(isLocal=True):
        """root path 根据指示的不同选择本地还是外部路径"""
        if isLocal:
            return projectConfig.getLocalPath()
        else:
            return projectConfig.getExportPath()

    @staticmethod
    def getChromeDataPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_CHROME_DATA)

    @staticmethod
    def getSampleIssueCommentDataPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_SAMPLE_ISSUE_COMMENT)

    @staticmethod
    def getPrCommitRelationPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_COMMIT_RELATION)

    @staticmethod
    def getIssueCommentPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_ISSUE_COMMENT_PATH)

    @staticmethod
    def getDataTrainPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_DATA_TRAIN)

    @staticmethod
    def getCommitFilePath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_COMMIT_FILE)

    @staticmethod
    def getReviewChangeDataPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_REVIEW_CHANGE)

    @staticmethod
    def getPullRequestPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_PULL_REQUEST)

    @staticmethod
    def getPRTimeLineDataPath(isLocal=True):
        return os.path.join(projectConfig.getRootPath(isLocal), projectConfig.PATH_TIMELINE)


if __name__ == "__main__":
    print(projectConfig.getRootPath())
    print(projectConfig.getChromeDataPath())
    print(projectConfig.getIssueCommentPath(False))
