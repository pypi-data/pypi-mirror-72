
# f -*- coding: utf-8 -*-
import socket, paramiko
import os, random, time
from PyForSatan import logger
import sys


class Create_Connect(object):
    __client__ = None

    __Sftp__ = None

    def __init__(self, ip="", username="", password="", port=22, timeout=20):
        """
        初始化程序
        :param ip: 目标ip地址
        :param username: 用户名
        :param password: 密码
        :param port: 登录端口
        :param timeout: 超时时间
        """
        super().__init__()

        # 初始化设置
        self.__client__ = paramiko.SSHClient()
        self.__client__.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__client__.connect(ip, username=username, password=password, port=port, timeout=timeout)


    def run_one_command(self, start_command='',guolv = True):
        """
        运行一条指令
        :param start_command: 运行的指令
        :return:
        """
        logger.info(start_command)
        stdin, stdout, stderr = self.__client__.exec_command(start_command, get_pty=True)

        if guolv != True:
            return stdout.readlines()
        return self.guolv_r_n(stdout.readlines())

    def guolv_r_n(self, data):
        """
        过滤返回数据里面的\r\n等字符集
        :param data: 需要过滤的数据
        :return:
        """
        temp = []
        for i in data:
            zifu = i.strip("\r\n")
            zifu = zifu.strip("\n")
            zifu = zifu.strip("\r")
            temp.append(zifu)
        return temp

    def print_logfile(self, start_command=''):
        """
        实时打印日志
        :param start_command: 打印日志的命令
        :return:
        """
        stdin, stdout, stderr = self.__client__.exec_command(start_command, get_pty=True)

        for i in stdout:
            print(i)

    def close_source(self):
        """
        关闭资源
        :return: None
        """
        if self.__client__ is not None:
            self.__client__.close()
        if self.__Sftp__ is not None:
            self.__Sftp__.close_source()

    @staticmethod
    def check_resource(ip, port):
        """
        静态方法，用于验证
        :param ip: 目标ip地址
        :param port: 端口
        :return:
        """
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(Create_Connect.timeout)
        try:
            sk.connect((ip, port))
            result = True
        except Exception:
            result = False
        finally:
            sk.close()
        return result

    def get_Sftp_client(self):
        """
        获取一个Create_Sftp的实例
        :return: 一个Create_Sftp的实例
        """
        if self.__Sftp__ is None:
            self.__Sftp__ = Create_Sftp(self)
            return self.__Sftp__
        else:
            return self.__Sftp__

    def __enter__(self):
        """
        兼容with方法
        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        兼容with方法
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if exc_tb is None:
            self.close_source()


class Create_Sftp(object):
    """
    Sftp 客户端
    """
    __client__ = None

    # ssh封装的客户端
    __resources__ = None

    def get_client(self):
        return self.__client__

    def __init__(self, connect_obj):
        """
        实例化出一个SFTPClient的客户端
        """
        super().__init__()
        self.resources = connect_obj
        self.__client__ = paramiko.SFTPClient.from_transport(connect_obj.__client__.get_transport())

    def close_source(self):
        if self.__client__ is not None:
            self.__client__.close()

    def get_path_remote_empty(self, path):
        """
            返回当前linux目录下的连接
        """

        try:
            list_dir = self.__client__.listdir(path)
        except IOError as e:
            return False
        except Exception as e:
            return None

        return list_dir

    def get_path_Sftp_listdir_attr(self,path):
        """
        返回目标文件夹的各个文件属性包括文件夹
        :param path:
        :return:
        """
        try:
            list_dir = self.__client__.listdir_attr(path)
        except IOError as e:
            return False
        except Exception as e:
            return None

        return list_dir
        

    def upload_file(self, remote_path, local_path):
        """
        上传文件
        """
        logger.info("正在上传"+local_path)
        result = self.__client__.put(local_path, remote_path, callback=file_upload_jingdu)
        print("\n")
        return result

    def dowload_file(self, remote_path, local_path):
        """
        下载文件
        """
        logger.info("正在下载"+remote_path)
        result = self.__client__.get(remote_path, local_path, callback=file_downlaod_jingdu)
        print("\n")
        return result

    def chmod(self, file_path, mode):
        """
        修改文件权限
        """
        self.__client__.chmod(file_path, mode)


    def __enter__(self):
        """
        兼容with方法
        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        兼容with方法
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if exc_tb is None:
            self.close_source()


def file_downlaod_jingdu(yijieshou, yaojieshou):
    """
    接收一个两个参数 ，当前已接收参数 int yijieshou，还需接收 int yaojieshou
    """
    jingdu = int((yijieshou / yaojieshou) * 100)

    bar_length = 20

    hashes = '#' * int(jingdu / 100.0 * bar_length)

    spaces = ' ' * (bar_length - len(hashes))

    sys.stdout.write("\r文件下载中（linux Sftp）: [%s] %d%%" % (hashes + spaces, jingdu))
    sys.stdout.flush()


def file_upload_jingdu(yijieshou, yaojieshou):
    """
    接收一个两个参数 ，当前已接收参数 int yijieshou，还需接收 int yaojieshou
    """
    jingdu = int((yijieshou / yaojieshou) * 100)

    bar_length = 20

    hashes = '#' * int(jingdu / 100.0 * bar_length)

    spaces = ' ' * (bar_length - len(hashes))

    sys.stdout.write("\r文件上传中（linux Sftp）: [%s] %d%%" % (hashes + spaces, jingdu))
    sys.stdout.flush()
