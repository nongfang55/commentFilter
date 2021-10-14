import matplotlib.pyplot as plt


class BoxDrawerUtils:
    """绘制箱型图的工具类"""

    @staticmethod
    def drawBoxPic(inputData, labels, xlabel, ylabel):

        plt.rc('font', family='Times New Roman')
        plt.rcParams['savefig.dpi'] = 100
        meanpointprops = dict(marker='D', markeredgecolor='black',
                              markerfacecolor='firebrick')
        f = plt.boxplot(inputData, labels=labels, patch_artist=True, meanline=False, showmeans=True, meanprops=meanpointprops)
        # data.boxplot()#画箱型图的另一种方法，参数较少，而且只接受dataframe，不常用
        plt.xticks(rotation=30, fontsize=16)
        plt.yticks(fontsize=16)
        if xlabel is not None:
            plt.xlabel(xlabel, fontsize=18)

        if ylabel is not None:
            plt.ylabel(ylabel, fontsize=18)

        ax = plt.gca()  # 获取边框
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5)

        for box in f['boxes']:
            # 箱体边框颜色
            box.set(color='black')
            # # 箱体内部填充颜色
            box.set(facecolor='#4F81BD')

        for median in f['medians']:
            median.set(color='black')

        plt.show()  # 显示图像
