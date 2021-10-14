import os


class projectConfig:

    projectName = 'commentFilter'

    PATH_CHROME_DATA = 'data' + os.sep + 'chrome' + os.sep + 'chromium_conversations_annotations.csv'
    PATH_SAMPLE_ISSUE_COMMENT = 'data' + os.sep + 'comment' + os.sep + 'sampleIssueComment_2.csv'

    @staticmethod
    def getRootPath():
        curPath = os.path.abspath(os.path.dirname(__file__))
        projectName = projectConfig.projectName
        rootPath = os.path.join(curPath.split(projectName)[0], projectName)  # 获取myProject，也就是项目的根路径
        return rootPath

    @staticmethod
    def exportPath():
        """由于现在的数据太大了，从其他项目直接读数据
        ，实现复用节约磁盘的空间
        """
        exportPath = r'C:\Users\ThinkPad\Desktop\Python\Reeview2\review\data\train'
        return exportPath

    @staticmethod
    def getChromeDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CHROME_DATA)

    @staticmethod
    def getSampleIssueCommentDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_SAMPLE_ISSUE_COMMENT)


if __name__ == "__main__":
    print(projectConfig.getRootPath())
    print(projectConfig.getChromeDataPath())
