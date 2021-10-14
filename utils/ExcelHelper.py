# coding=gbk
import os

import xlrd
import xlwt
from datetime import date

from pandas import DataFrame
from xlutils import copy

class ExcelHelper:
    """Excel的工具实现类， 用于excel的各种读写"""

    STR_STYLE_NORMAL = 'align: vertical center, horizontal center'
    STR_STYLE_FIRST_RANK = 'pattern: pattern solid, fore_colour red'
    STR_STYLE_SECOND_RANK = 'pattern: pattern solid, fore_colour light_orange'
    STR_STYLE_THIRD_RANK = 'pattern: pattern solid, fore_colour sea_green'
    STR_STYLE_FORTH_RANK = 'pattern: pattern solid, fore_colour gray25'
    STR_STYLE_HINT_YELLOW = 'pattern: pattern solid, fore_colour yellow'
    STR_STYLE_HINT_YELLOW_AND_BOLD = 'pattern: pattern solid, fore_colour yellow; font: bold on'
    STR_STYLE_HINT_ITALIC = 'font: italic on'
    STR_STYLE_BOLD = 'font: bold on'
    STR_STYLE_DATE = 'YYYY/MM/DD hh:mm'
    STR_STYLE_DATA_DATE = '%Y-%m-%dT%H:%M:%SZ'

    def initExcelFile(self, fileName, sheetName, excel_key_list=None):
        wbook = xlwt.Workbook()
        wsheet = wbook.add_sheet(sheetName)
        style = xlwt.easyxf(self.STR_STYLE_NORMAL)
        if excel_key_list is not None:
            index = 0
            for key in excel_key_list:
                wsheet.write(0, index, key, style)
                index = index + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    @staticmethod
    def getNormalStyle():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_NORMAL)
        return style

    @staticmethod
    def getItalicStyle():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_HINT_ITALIC)
        return style

    @staticmethod
    def getFirstRankValue():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_FIRST_RANK)
        return style

    @staticmethod
    def getSecondRankValue():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_SECOND_RANK)
        return style

    @staticmethod
    def getThirdRankValue():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_THIRD_RANK)
        return style

    @staticmethod
    def getForthRankValue():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_FORTH_RANK)
        return style

    @staticmethod
    def getHintYellowValue():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_HINT_YELLOW)
        return style

    @staticmethod
    def getHintYellowAndBoldValue():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_HINT_YELLOW_AND_BOLD)
        return style

    @staticmethod
    def getBoldValue():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_BOLD)
        return style

    @staticmethod
    def getDateStyle():
        style = xlwt.XFStyle()
        style.num_format_str = ExcelHelper.STR_STYLE_DATE
        return style

    def writeExcelRow(self, fileName, sheetName, startRow, startCol, dataList, style):
        ''' 覆盖  源文件必须存在 '''

        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        pos = 0
        for item in dataList:
            wsheet.write(startRow, startCol + pos, item, style)
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def addSheet(self, filename, sheetName):
        rb = xlrd.open_workbook(filename, formatting_info=True)
        # make a copy of it
        from xlutils.copy import copy as xl_copy
        if sheetName not in rb.sheet_names():
            wb = xl_copy(rb)
            Sheet1 = wb.add_sheet(sheetName)
            wb.save(filename)

    def appendExcelRow(self, fileName, sheetName, dataList, style):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        pos = 0
        for item in dataList:
            wsheet.write(row, pos, item, style)
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def appendExcelRowWithDataLists(self, fileName, sheetName, dataLists, style):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        for dataList in dataLists:
            pos = 0
            for item in dataList:
                wsheet.write(row, pos, item, style)
                pos = pos + 1
            row = row + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def appendExcelRowWithDataListsAndStyles(self, fileName, sheetName, dataLists, styles):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        for index_list, dataList in enumerate(dataLists):
            styleList = styles[index_list]
            pos = 0
            for index, item in enumerate(dataList):
                wsheet.write(row, pos, item, styleList[index])
                pos = pos + 1
            row = row + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def appendExcelRowWithDiffStyle(self, fileName, sheetName, dataList, style):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        pos = 0
        for index, item in enumerate(dataList):
            wsheet.write(row, pos, item, style[index])
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def writeExcelCol(self, fileName, sheetName, startRow, startCol, dataList, style=None):
        ''' 覆盖  源文件必须存在 '''

        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)

        if (style == None):
            style = self.getNormalStyle()

        pos = 0
        for item in dataList:
            wsheet.write(startRow + pos, startCol, item, style)
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def appendExcelRowWithDataLists(self, fileName, sheetName, dataLists, style):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        for dataList in dataLists:
            pos = 0
            for item in dataList:
                wsheet.write(row, pos, item, style)
                pos = pos + 1
            row = row + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def writeDataFrameToExcel(self, fileName, sheetName, dataframe):
        """写Dataframe到指定的excel
           fileName: excel的名字
           sheetName: 写入的sheetName
           dataframe: 需要写入的dataframe
        """
        if isinstance(dataframe, DataFrame):
            if not os.path.exists(path=fileName):
                self.initExcelFile(fileName, sheetName)
            else:
                self.addSheet(fileName, sheetName)

            """遍历dataframe依次加入"""
            self.appendExcelRow(fileName, sheetName, dataframe.columns, style=self.getNormalStyle())
            rows = []
            for index, row in dataframe.iterrows():
                rows.append(row)
            self.appendExcelRowWithDataLists(fileName, sheetName, rows, style=self.getNormalStyle())

    def readExcelSheet(self, fileName, sheetName, formatting=True):
        rbook = xlrd.open_workbook(fileName, formatting_info=formatting)
        rsheet = rbook.sheet_by_name(sheetName)
        return rsheet

    def getExcelSheets(self, fileName):
        rbook = xlrd.open_workbook(fileName)
        return rbook.sheets()

    def readExcelRow(self, fileName, sheetName, startRow, startCol=0, formatting=True):
        rbook = xlrd.open_workbook(fileName, formatting_info=formatting)
        rsheet = rbook.sheet_by_name(sheetName)
        return rsheet.row_values(startRow)[startCol:]

    def readExcelCol(self, fileName, sheetName, startCol, startRow=0, formatting=True):
        rbook = xlrd.open_workbook(fileName, formatting_info=formatting)
        rsheet = rbook.sheet_by_name(sheetName)
        return rsheet.col_values(startCol)[startRow:]

    def get_date(self, cell, source):
        if cell.ctype == xlrd.XL_CELL_DATE:
            date_value = xlrd.xldate_as_tuple(cell.value, source.datemode)
            return date_value


if __name__ == "__main__":
    pass