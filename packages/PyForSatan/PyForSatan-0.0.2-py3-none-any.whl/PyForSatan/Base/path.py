import os, sys


def get_absolute_jiaoben():
    """
    返回运行脚本的绝对路径(文件夹)
    :return:
    """
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def get_exec_path():
    """
    返回 执行程序的路径 exe  比如Python的路径 常见使用在打包exe程序中
    :return:
    """
    return os.path.dirname(os.path.realpath(sys.executable))


def static_get_file_dir(file_path=None, huidiao=None):
    """
    指定文件夹中 循环递归获得绝对路径
    :param file_path:
    :param huidiao:  回调函数 参数是file_path 当前文件
    :return:
    """
    file_obj = dir_path_recursion(huidiao)
    file_obj.get_dir_path(file_path)

    return file_obj.dir_jihe


class dir_path_recursion:
    """
    递归查询操作文件的类
    """
    dir_jihe = []

    huidiao = None

    def __init__(self, huidiao):
        """
        初始化
        :param huidiao:
        """
        self.dir_jihe = []
        self.huidiao = huidiao

    def get_dir_path(self, file_path):
        if os.path.isdir(file_path) is True:
            for i in os.listdir(file_path):
                self.get_dir_path(os.path.join(file_path,i))
        elif os.path.isfile(file_path):
            self.dir_jihe.append(file_path)
            if self.huidiao is not None:
                self.huidiao(file_path)