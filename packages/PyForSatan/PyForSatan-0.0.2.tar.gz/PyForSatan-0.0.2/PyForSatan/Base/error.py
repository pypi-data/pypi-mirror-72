
class NotFindConfigFile(Exception):
    """
    用于没有找到配置文件的异常
    """
    def __str__(self):
        print("没有设置配置文件路径或在默认的路径下没有找到配置文件!!")


class ConfigurationFailRecipient(Exception):
    """
    用于没有找到配置文件的异常
    """
    def __str__(self):
        print("EmailResprond 类中收件人类型无法检测")


class NotFindEmailAddressInfo(Exception):
    """
    在字符串中没有搜到email地址
    """
    def __str__(self):
        print("EmailResprond 字符串中没有搜到email地址")
