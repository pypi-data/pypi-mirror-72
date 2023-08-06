import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from PyForSatan.Base.get_yaml_config import get_yaml
from PyForSatan.Email.respond import EmailResprond

class Email_Send:

    __Resource__ = None

    __config_name__="defalut"

    def __init__(self):
        pass

    def close(self):
        if self.__Resource__ is not None:
            self.__Resource__.quit()

    def get_config(self,file_path=""):
        """

        :param file_path:
        :return:
        """
        return get_yaml().getdata()["email"]

    def SwitchToResource(self,config_name="defalut"):
        """

        :param config_name:
        :return:
        """
        self.__config_name__ = config_name
        config_data = self.get_config()
        if self.__Resource__ is not None:
            self.close()
        if config_data[config_name]["SSL"] == "true":
            server = smtplib.SMTP_SSL(config_data[config_name]["Server"], int(config_data[config_name]["Port"]))
        else:
            server = smtplib.SMTP(config_data[config_name]["Server"], int(config_data[config_name]["Port"]))
        server.login(config_data[config_name]["UserName"],config_data[config_name]["Password"])
        self.__Resource__ = server
        return self

    def send(self,Body:EmailResprond):
        try:
            if self.__Resource__ is None:
                self.SwitchToResource()
            # 构造发送器
            config_data = self.get_config()[self.__config_name__]
            if Body.getActive_type() != "html":
                msg = MIMEText(Body.getBodyContent(), 'plain', 'utf-8')
            else:
                msg = MIMEText(Body.getBodyContent(), 'html', 'utf-8')
            msg['From'] = formataddr([config_data["NickName"], config_data["UserName"]])
            msg['To'] = Body.getRecipients()
            msg['Subject']=Body.getSubject()
            self.__Resource__.sendmail(config_data["EmailAddress"],msg['To'], msg.as_string())
            return True
        except Exception as e:
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__Resource__ is not None:
            self.close()


