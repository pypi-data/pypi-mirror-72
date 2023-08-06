from PyForSatan.Base.path import get_absolute_jiaoben
from PyForSatan.Base.error import NotFindConfigFile
import os

class config:

    file_path = ""

    def __init__(self,file_path=""):
        """

        :param file_path: 文件路径
        """
        if file_path == "":
            ConfigFilePath = self.__getDefaultConfigPath__()
            if ConfigFilePath is not None:
                self.file_path = ConfigFilePath

        if self.file_path == "":
            raise NotFindConfigFile()

    def __getDefaultConfigPath__(self):
        """
        在默认的路径下寻找配置文件
        :return:
        """
        root_path = get_absolute_jiaoben()
        file_path = ["config.yaml","application.yaml"]
        file_dir= [".","./config"]

        for i in file_dir:
            if os.path.exists(os.path.join(root_path, i)):
                files_list_path = os.listdir(os.path.abspath(os.path.join(root_path, i)))
                for j in file_path:
                    if j in files_list_path:
                        return os.path.join(os.path.abspath(os.path.join(root_path, i)),j)
        return None
