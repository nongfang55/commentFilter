import os

from utils.ExcelHelper import ExcelHelper
from utils.StringKeyUtils import StringKeyUtils


class SingleDataAnalyzer:
    """输入两列数据， 第一列数据是权重， 第二列数据是数量，
        计算数值的各种指标，计算的结果写道 Excel 中
    """

    def process(self, weights, nums, labels, excelName, sheetName):
        """数据可能有若干列
           weight : 权重列， 或者是数值列
           nums : 若干列的数量
           labels : 不同的标签
           实例：   weight = [1,2,3,4]
                    nums = [[4,3,2,1], [2,3,1,4]]
                    labels = ['a', 'b']
                    相当于 a => [(1,2,3,4), (4,3,2,1)]
                          b => [(1,2,3,4), (2,3,1,4)]
        """

        """初始化excel"""

        if os.path.exists(excelName):
            ExcelHelper().addSheet(filename=excelName, sheetName=sheetName)
        else:
            ExcelHelper().initExcelFile(fileName=excelName, sheetName=sheetName)

        """计算基本的信息 """
        result_list = []

        """先放label"""
        label_row = ['']
        label_row.extend(labels)
        result_list.append(label_row)

        """数量总数"""
        sum_list = [StringKeyUtils.STR_KEY_SUM_NUM]
        sum_list.extend([sum(data) for data in nums])
        result_list.append(sum_list)

        """包括最大值， 最下值， 加权平均值"""
        max_list = [StringKeyUtils.STR_KEY_MAX_NUM]
        max_list.extend([max([weights[index] for index, _ in enumerate(data) if data[index] > 0]) for data in nums])
        result_list.append(max_list)

        min_list = [StringKeyUtils.STR_KEY_MIN_NUM]
        min_list.extend([min([weights[index] for index, _ in enumerate(data) if data[index] > 0]) for data in nums])
        result_list.append(min_list)

        weight_mean_list = [StringKeyUtils.STR_KEY_WEIGHT_MEAN]
        for index, numList in enumerate(nums):
            weight_mean_num = 0
            for weight, num in zip(weights, numList):
                weight_mean_num += weight * num
            weight_mean_num /= sum_list[1 + index]
            weight_mean_list.append("%.2f" % weight_mean_num)

        result_list.append(weight_mean_list)

        result_list.append([""])

        """白分类比例数值， 每5 % 为一列"""
        sample_lists = []
        for numList in nums:
            sample_list = []
            for index, weight in enumerate(weights):
                sample_list.extend([weight for _ in range(0, numList[index])])
            sample_list.sort(reverse=False)
            sample_lists.append(sample_list)

        for i in range(0, 20):
            ratio_list = ["%.2f" % (i * 0.05)]
            for sample_list in sample_lists:
                ratio_list.append(sample_list[int(i * 0.05 * sample_list.__len__())])
            result_list.append(ratio_list)

        """计算每个小块的占比"""
        result_list.append([""])
        for index_1, weight in enumerate(weights):
            ratio_list = []
            ratio_list.append(weight)
            for index_2, sum_num in enumerate(sum_list[1:]):
                ratio_list.append("%.2f" % ((1.0 * nums[index_2][index_1]) / sum_num))
            result_list.append(ratio_list)

        """修改格式"""
        result_list = [[str(y) for y in x] for x in result_list]
        ExcelHelper().appendExcelRowWithDataLists(fileName=excelName, sheetName=sheetName, dataLists=result_list,
                                                  style=ExcelHelper.getNormalStyle())


if __name__ == "__main__":
    weight = [1, 2, 3, 4, 5]
    data = [[1, 2, 3, 4, 5], [1, 4, 10, 3, 0]]
    excelName = 'aaaa.xls'
    sheetName = 'demo'

    SingleDataAnalyzer().process(weight, data, ['A', 'B'], excelName, sheetName)
