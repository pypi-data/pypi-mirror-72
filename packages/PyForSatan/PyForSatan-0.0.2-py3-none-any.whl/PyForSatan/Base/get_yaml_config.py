from PyForSatan.Base.get_config import config
import yaml
from yaml import BaseLoader

class get_yaml(config):

    def __init__(self, file_path=""):
        super().__init__(file_path)

    def getdata(self):
        with open(self.file_path,'r',encoding='utf-8') as file:
            data = yaml.load(file.read(),Loader=BaseLoader)
        return data
