import os,sys, datetime,json,xlrd
from xlrd import xldate_as_datetime


class read_xlsx:
    __data__ = {}

    resource = None

    # 当前的sheet_names
    sheet_names = None

    def __init__(self, file_path=""):
        if not os.path.exists(file_path):
            raise IOError("无法打开文件：" + file_path)
        self.resource = xlrd.open_workbook(file_path)

    def __get_sheet(self, sheet_names):
        """
        主要获取sheet页
        :param sheet_names:
        :return:
        """
        # 获取sheet页
        if sheet_names is None:
            sheets = self.resource.sheet_by_index(0)
        elif type(sheet_names) == str and len(sheet_names) != 0:
            sheets = self.resource.sheet_by_name(sheet_names)
        elif type(sheet_names) == int:
            sheets = self.resource.sheet_by_index(sheet_names)
        else:
            raise RuntimeError("获取sheet页发生异常，sheet_names 参数错误")
        return sheets

    def __get_keys_values(self, sheets=None, hang_local=None, start_location=None, stop_location=None):
        """

        :param hang_local: 从哪行读取 一般是0
        :param start_location: 从哪行的第几个列开始读取
        :param stop_location: 哪行的第几个列结束 不包括这列数据
        :return:
        """
        if hang_local is None:
            keys = sheets.row_values(0)
        else:
            keys = sheets.row_values(hang_local)

        if start_location is None:
            start_location = 0
        else:
            start_location = start_location

        if stop_location is None:
            if len(keys) >= 1:
                stop_location = len(keys)
            else:
                stop_location = 0
        else:
            stop_location = stop_location
        return keys[start_location:stop_location+1]

    def __get_data_yuanshi(self, sheet_names=None, hulue_start=None, hulue_stop=None, read_lie=None, keys_hang_local=None,
                         keys_start_location=None, keys_stop_location=None):
        """
        获取execl原始数据
        :param sheet_names: execl sheet页的名字 ,可以为None ,可以为字符串，也可以为数字
        :param hulue_start: 忽略从多少行开始  包括这一行
        :param hulue_stop: 忽略到第几行结束  包括这一行
        :param read_lie: 最多读取多少列，一般为自动读取的最大值
        :param keys_hang_local: 标题名，也就是execl的头部文件的位置一般是0 表示key值
        :param keys_start_location: keys从哪里开始  包括这一行
        :param keys_stop_location: keys到哪里结束  包括这一行
        :return: self
        """
        # 参数初始化
        if hulue_start is None and hulue_stop is None:
            hulue_value = range(0, 1)
        else:
            hulue_value = range(hulue_start, hulue_stop+1)

        sheets = self.__get_sheet(sheet_names)

        keys = self.__get_keys_values(sheets, hang_local=keys_hang_local, start_location=keys_start_location,
                                      stop_location=keys_stop_location)

        # 最多获取多少行
        if read_lie is not None:
            values_len = int(read_lie)
        else:
            values_len = sheets.nrows

        sheet_names_local = sheets.name

        data_temp = []

        # 逐行读取
        for i in range(0, values_len):
            data_temp_temp = []
            if i not in hulue_value:
                for j in range(0, len(keys)):
                    if keys_start_location is None:
                        data_temp_temp.append({keys[j]: sheets.cell(i, j)})
                    else:
                        data_temp_temp.append({keys[j]: sheets.cell(i, j + keys_start_location)})
                data_temp.append(data_temp_temp)
        self.__data__.update({sheet_names_local: data_temp})

        return sheet_names_local

    def __to_str(self, cells):
        """
        对cell对象进行格式化字符串
        :param cells: 一个行的对象
        :return: 返回转化字符串的对象
        """
        if cells.ctype == 0:
            return cells.value
        elif cells.ctype == 1:
            return cells.value
        elif cells.ctype == 2:
            return str(int(cells.value))
        elif cells.ctype == 3:
            if cells.value >= 1:
                return xldate_as_datetime(cells.value, 0).strftime('%Y/%d/%m %H:%M:%S')
            else:
                return xldate_as_datetime(cells.value, 0).strftime('%H:%M:%S')
        elif cells.ctype == 4:
            if cells.value == 1:
                return "True"
            elif cells.value == 0:
                return "False"
            else:
                return ""
        elif cells.ctype == 5:
            return None
        elif cells.ctype == 6:
            return ""

    def __check_sheet_before(self,sheet_names):
        if sheet_names is not None and sheet_names not in self.__data__.keys():
            raise KeyError("sheet_names 表没有被载入")
        if self.sheet_names is None:
            raise RuntimeError("请在获取数据之前先载入数据，当前的sheet_names 为空")

    def __check_sheet_before_get(self,sheet_names=None):
        """

        :param sheet_names:获取那个sheet页的数据 None表示上个被载入的sheet页
        :return: 目标获取sheet页
        """
        self.__check_sheet_before(sheet_names)
        if sheet_names is None:
            bianli = self.__data__[self.sheet_names]
        else:
            bianli = self.__data__[sheet_names]
        return bianli

    def get_hang_data(self,hangshu,sheet_names=None):
        """
        获取指定sheet_names中指定行的集合 默认当前sheets
        :param hangshu:
        :return:
        """
        if sheet_names is None:
            sheets = self.__get_sheet(self.sheet_names)
        else:
            sheets = self.__get_sheet(sheet_names)

        return sheets.row_values(hangshu)

    def get_shu_data(self,shu,sheet_names=None):
        """
        获取指定sheet_names中指定竖的集合 默认当前sheets
        :param shu:
        :param sheet_names:
        :return:
        """
        if sheet_names is None:
            sheets = self.__get_sheet(self.sheet_names)
        else:
            sheets = self.__get_sheet(sheet_names)

        return sheets.col_values(shu)

    # 兼容with语句
    def load_get_data(self, sheet_names=None, hulue_start=None, hulue_stop=None, read_lie=None, keys_hang_local=None,
                     keys_start_location=None, keys_stop_location=None):
        """

        :param sheet_names:
        :param hulue_start:
        :param hulue_stop:
        :param read_lie:
        :param keys_hang_local:
        :param keys_start_location:
        :param keys_stop_location:
        :return: 返回该对象  然后使用get_data() get_str_data() 等方法返回数据
        """
        self.sheet_names = self.__get_data_yuanshi(sheet_names=sheet_names, hulue_start=hulue_start, hulue_stop=hulue_stop, read_lie=read_lie, keys_hang_local=keys_hang_local,
                     keys_start_location=keys_start_location, keys_stop_location=keys_stop_location)

        return self

    def get_sheets_data(self,sheet_names):
        """
        手动指定哪个sheets页
        :param sheet_name:
        :return:
        """
        self.__check_sheet_before(sheet_names)
        self.sheet_names = sheet_names
        return self

    def get_general_data(self,sheet_names=None):
        """

        :param sheet_names: 获取那个sheet页的数据 None表示上个被载入的sheet页
        :return: 普通的数据
        """
        bianli = self.__check_sheet_before_get(sheet_names)

        data = []
        for i in bianli:
            # 一行的数据
            data_temp = []
            for j in i:
                for k in j:
                    data_temp.append({k: j[k].value})
            data.append(data_temp)
        return data

    def get_str_data(self, sheet_names=None):
        """
            输出普通数据
        :param sheet_names: execl sheet页的名字 ,可以为None ,可以为字符串，也可以为数字
        :param hulue_start: 忽略从多少行开始  包括这一行
        :param hulue_stop: 忽略到第几行结束  包括这一行
        :param read_lie: 最多读取多少列，一般为自动读取的最大值
        :param keys_hang_local: 标题名，也就是execl的头部文件的位置一般是0 表示key值
        :param keys_start_location: keys从哪里开始  包括这一行
        :param keys_stop_location: keys到哪里结束  包括这一行
        :return: 返回data
        """
        bianli = self.__check_sheet_before_get(sheet_names)
        data = []
        for i in bianli:
            # 一行的数据
            data_temp = []
            for j in i:
                for k in j:
                    data_temp.append({k: self.__to_str(j[k])})
            data.append(data_temp)
        return data

    def close(self):
        """
        关闭系统资源
        :return:
        """
        if self.resource is not None:
            self.resource.release_resources()

    # 兼容with语句
    def __enter__(self):
        return self

    # 兼容with语句
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.close()

    def get_one_keys_dict(self,data_type="default"):
        """
        获取一个数据字典
        :param data_type: 数据类型 具体请看源码有多少中
        :return: 一个数据字典
        """
        if data_type == "default":
            data =  self.get_general_data()
        elif data_type == "str":
            data =  self.get_str_data()
        else:
            raise Exception("暂未定义该方法获取数据")

        keys = []

        for i in data[0]:
            for j in i:
                if j in keys:
                    raise KeyError("该表不符合此方法的要求因为头部数据keys不唯一")
                else:
                    keys.append(j)
        data_temp = []

        for i in data:
            data_temp_dict={}
            for j in i:
                data_temp_dict.update(j)
            data_temp.append(data_temp_dict)

        return data_temp

    @staticmethod
    def data_guolv_result(data=None,dataType=list,baoliu_start=0,baoliu_stop=None,shanchu=None):
        """

        :param data: 数据
        :param dataType: 输入进来的数据类型
        :param baoliu:  保留那几列
        :param shanchu: 删除那几列
        :return:
        """
        data_temp = []

        if baoliu_stop is not None:
            baoliu = range(baoliu_start, baoliu_stop)
        else:
            baoliu = range(baoliu_start, len(data[0]))

        if dataType is list:
            for i in range(len(data)):
                data_temp_temp = []
                for j in range(len(data[i])):
                    if j in baoliu:
                        if shanchu is not None:
                            if j not in shanchu:
                                data_temp_temp.append(data[i][j])
                        else:
                            data_temp_temp.append(data[i][j])
                data_temp.append(data_temp_temp)

        return data_temp

    @staticmethod
    def transform_data_to_json(data=[]):
        """
        把原始数据格式转化为一行为dict格式的数组
        :param data:
        :return:
        """
        data_temp = []
        for i in data:
            data_temp_dict = {}
            for j in i:
                data_temp_dict.update(j)
            data_temp.append(data_temp_dict)

        return data_temp

    @staticmethod
    def transform_json_to_data(data=[]):
        """
        把数据格式从一行是dict格式的转化为 原始格式 方便创建data数据
        :param data:
        :return:
        """
        data_temp = []
        for i in data:
            data_temp_hang = []
            for j in i:
                data_temp_hang.append({j:i[j]})
            data_temp.append(data_temp_hang)

        return data_temp




