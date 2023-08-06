from PyForSatan.Base.error import ConfigurationFailRecipient
from email.utils import formataddr
from PyForSatan.Base.error import NotFindEmailAddressInfo
import re, os


class EmailResprond:
    __recipients__ = ""

    __active_type__ = None

    __BodyContent__ = None

    __AttachmentFile__ = None

    __Subject__ = None

    def __init__(self):
        self.__AttachmentFile__ = []
        self.__BodyContent__ = ""
        self.__active_type__ = "html"
        self.__recipients__ = ""
        self.__Subject__ = ""

    def addRecipient(self, shoujianreng):
        """
        添加收件人地址
        :param shoujianreng: 添加用户  格式 ceshi ceshi@163.com 或者 ceshi@163.com 或者 ["ceshi@163.com",..] 或者{"ceshi":"ceshi@163.com",...}
        :return:
        EmailResprond().addRecipient(["ceshi@163.com","ceshi@163.com"]).addRecipient(" wenjian wenjian@163.com ").addRecipient({"wenjian":"ceshi@163.com"})
        """
        if type(shoujianreng) is str:
            pattern_string = re.compile(r'([^\s]+)[\s]+([^\s]+?@[^\s]+)')
            String_data = pattern_string.findall(shoujianreng)
            if type(String_data) is list and len(String_data) > 0 and len(String_data[0]) > 1:
                if self.__recipients__ == "":
                    self.__recipients__ = formataddr([String_data[0][0], String_data[0][1]])
                else:
                    self.__recipients__ = self.__recipients__ + "," + formataddr([String_data[0][0], String_data[0][1]])
            else:
                pattern = re.compile(r'[^\s]+?@[^\s]+')
                String_pattern = pattern.findall(shoujianreng)
                if len(String_pattern) == 1:
                    if self.__recipients__ == "":
                        self.__recipients__ = formataddr([String_pattern[0], String_pattern[0]])
                    else:
                        self.__recipients__ = self.__recipients__ + "," + formataddr(
                            [String_pattern[0], String_pattern[0]])
                else:
                    raise NotFindEmailAddressInfo()

        elif type(shoujianreng) is list:
            if len(shoujianreng) > 0:
                for i in shoujianreng:
                    if self.__recipients__ == "":
                        self.__recipients__ = formataddr([i, i])
                    else:
                        self.__recipients__ = self.__recipients__ + "," + formataddr([i, i])
            else:
                raise Exception("传入的数组为空")

        elif type(shoujianreng) is dict:
            recipients_list = []
            for key in shoujianreng:
                recipients_list.append(formataddr([key, shoujianreng[key]]))
            if len(recipients_list) > 0:
                self.__recipients__ = self.__recipients__ + ",".join(recipients_list)
        else:
            raise ConfigurationFailRecipient()

        return self

    def setBody(self, type="html", content=""):
        """

        :param type: 可以为html或text
        :return:
        """
        if type == "html":
            self.__BodyContent__ = content
            self.__active_type__ = "html"
        elif type == "txt":
            self.__BodyContent__ = content
            self.__active_type__ = "txt"

        return self

    def setAttachment(self, file_path):
        """

        :param file_path:
        :return:
        """
        self.__AttachmentFile__.append(os.path.abspath(file_path))
        return self

    def setSubJect(self, content=""):
        """
        设置主题内容
        :param content:
        :return:
        """
        self.__Subject__ = content
        return self

    def getRecipients(self):
        return self.__recipients__

    def getActive_type(self):
        return self.__active_type__

    def getBodyContent(self):
        return self.__BodyContent__

    def getAttachmentFile(self):
        return self.__AttachmentFile__

    def getSubject(self):
        if self.__Subject__ is None:
            return ""
        return self.__Subject__

    def __str__(self):
        info = "收件人  :" + self.__recipients__ + "\n" \
               + "主题    :" + self.__Subject__ + "\n" \
               + "内容类型:" + self.__active_type__ + "\n" \
               + "内容    :" + self.__BodyContent__
        return info
