
"""用于存放一些通用的函数"""
from utils.ExcelHelper import ExcelHelper

def covertListToExcelFromInput():
    """循环从的从终端读取输入，然后不断的追加到临时 Excel"""
    ExcelHelper().initExcelFile(fileName='temp.xls', sheetName='sheet1')
    while True:
        line = input()
        line = line.strip()
        if line.__len__() == 0:
            continue
        if line.__len__() > 2 and line[0] == '[' and line[-1] == ']':
            items = line[1:-1].split(',')
            ExcelHelper().appendExcelRow(fileName='temp.xls', sheetName='sheet1',
                                         dataList=items, style=ExcelHelper.getNormalStyle())
        else:
            if line[0] == 'n':
                break

if __name__ == "__main__":
    covertListToExcelFromInput()
