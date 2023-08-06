from PyForSatan.LinuxConnect.base_drivers import Create_Connect,Create_Sftp
from PyForSatan import logger
import re,os,traceback
from stat import S_ISDIR

class get_info(object):
    """
    基于 base_drivers 做的简易工具

    """

    resource = None
    def get_resource_client(self):
        """
        获取命令行客户端
        """
        return self.resource

    def get_resource_Sftp(self):
        """
        获取一个客户端Sftp
        """
        return self.resource.get_Sftp_client()

    def __init__(self, resource):
        super().__init__()
        self.resource = resource
        if resource is None:
            raise RuntimeError('所引入的linux连接资源为None，不通过,请重新检查linux资源是否可用')

    def dir_path_isempty(self, path):
        """
        检查目标linux是否有该文件夹
        """
        cmd = r"if [ -d %s ]; then echo you; else echo wu; fi" % (path)

        result = self.resource.run_one_command(cmd)

        if result is not None and len(result) > 0:
            if str(result[0]).strip("\r\n") == 'you':
                return True
            elif str(result[0]).strip("\r\n") == 'wu':
                return False

        return None

    def makedirs(self, path):
        cmd = r"mkdir -p %s" % (path)
        result = self.resource.run_one_command(cmd)

    def cycle_copy_dowload(self,remote_dir="",local_dir=""):
        """
        遍历循环下载
        :param remote_dir: 远程linux文件夹
        :param local_dir:  本地文件夹
        :return: True or False
        """
        list_dur_remote = bianlixunhuan(self).get_wenjian_list(remote_dir)

        for i in list_dur_remote:
            locals_dir = local_dir+i[len(remote_dir):-1]
            if not os.path.exists(os.path.dirname(locals_dir)):
                os.makedirs(os.path.dirname(locals_dir))
            print("远程路径",i)
            print("本地路径",locals_dir)
            try:
                self.resource.get_Sftp_client().dowload_file(i,locals_dir)
                logger.info("下载成功")
            except  IOError :
                traceback.print_exc()
                logger.error("下载失败")

    def version(self):
        """
        获取linux的版本
        """
        version = self.resource.run_one_command('cat /etc/redhat-release')
        if version is not None:
            if version[0].strip(' ') == '':
                return ""
            return version[0].strip('\n')
        return None

    def sn(self):
        """
           获取linux sn
        """
        sn_linux = self.resource.run_one_command("dmidecode -t 1|grep UUID")
        pattern = re.compile(r'.*?(UUID.*)\s*', re.S)
        temp = ""
        for i in range(len(sn_linux)):
            items = re.findall(pattern, sn_linux[i])
            if items is not None and len(items) > 0:
                temp = items[0]
        return temp


    def get_service_port(self,proc):
        port_linux = self.resource.run_one_command("netstat -plnt |grep "+str(proc)+" |grep -v grep|awk '{print$4}'")
        pattern = re.compile(r'.*?:+(.*)', re.S)
        temp_port = []
        for i in range(len(port_linux)):
            items = re.findall(pattern, port_linux[i])
            if items is not None:
                if len(items) > 0:
                    temp_port.extend(items)
        return temp_port

    def port(self):
        """
        获取端口号 返回一个数组
        """
        port_linux = self.resource.run_one_command("netstat -plnt|awk '{print$4}'")
        pattern = re.compile(r'.*?:+(.*)', re.S)
        temp_port = []
        for i in range(len(port_linux)):
            items = re.findall(pattern, port_linux[i])
            if items is not None:
                if len(items)>0:
                    temp_port.extend(items)
        return temp_port

    def networks_linux(self):
        pass

    def cpu_model(self):
        """
        获取cpu信息
        """
        try:
            # cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c
            # more /proc/cpuinfo |grep "physical id"|uniq|wc -l
            # cat /proc/cpuinfo |grep MHz|uniq
            cpu_info = self.resource.run_one_command('more /proc/cpuinfo |grep "physical id"|uniq|wc -l')
            cpu_info_string = " ".join(cpu_info).strip().replace('\n', '').replace('\r', '')
        except:
            cpu_info_string = ""
        finally:
            return cpu_info_string

    def service_to_tomcat_list(self):
        """
        获取所有tomcat应用程序列表
        """
        tomcat = self.resource.run_one_command("source /etc/profile; "+'ps -ef |grep -v grep|grep org.apache.catalina.startup.Bootstrap')
        if tomcat is not None and len(tomcat) != 0:
            patten_string = r'(.*?)\s+?([0-9]+).*?Dcatalina\.home=(.*?)\s+?.*'
            pattern = re.compile(patten_string, re.S)
            data_temp = []
            for i in tomcat:
                shuju = re.findall(pattern, i)
                if len(shuju) > 0:
                    data_temp.append(
                        {
                            "user": shuju[0][0],
                            "proc": shuju[0][1],
                            "path": shuju[0][2],
                            "ps":i,
                            "port":self.get_service_port(shuju[0][1])
                        }
                    )
            return data_temp

    def service_tomcat_extend(self):
        data = self.service_to_tomcat_list()
        if data is not None:
            for i in data:
                types = 9
                Sftp = self.get_resource_Sftp()
                dir_path_tomcat = Sftp.get_path_remote_empty(i["path"])
                if dir_path_tomcat is not None :
                    if "bin" in dir_path_tomcat:
                        dir_path_jiaoben = Sftp.get_path_remote_empty(i["path"]+"/bin")
                        if dir_path_jiaoben is not None and "startup.sh" in dir_path_jiaoben:
                            types = 1
                        else:
                            types = 2
                        if dir_path_jiaoben is not None and "version.sh" in dir_path_jiaoben:
                            version = self.get_resource_client().run_one_command("source /etc/profile; "+"source /etc/profile > /dev/null 2>&1;bash %s"%(i["path"]+"/bin/version.sh"))
                            if version is not None:
                                i["version_info"] = "\r\n".join(version)
                                patten_string = r'.*?Server version:(.*?)\r\n'
                                pattern = re.compile(patten_string, re.S)
                                version_info_find = re.findall(pattern,i["version_info"])
                                if version_info_find is not None:
                                    i["version"] = version_info_find[0].strip()
                else:
                    types = 8
                i["type"] = types
                restart_script = "#!/bin/sh \n" \
                                  "pid=`ps -ef|grep java|grep {} |grep -v \"grep\"|awk '{{print $2}}'`\n" \
                                  "if [ -n \"$pid\" ];then\n" \
                                  "{{\n" \
                                  "   kill -9 $pid    \n" \
                                  "}}\n" \
                                  "else\n" \
                                  "       echo \"{} is not running\"\n" \
                                  "fi\n" \
                                  "cd {}/bin\n" \
                                  "{}/bin/startup.sh".format(i["path"], i["path"],
                                                             i["path"], i["path"])
                i["restart_script"] = restart_script

                stop_script = "#!/bin/sh \n" \
                                  "pid=`ps -ef|grep java|grep {} |grep -v \"grep\"|awk '{{print $2}}'`\n" \
                                  "if [ -n \"$pid\" ];then\n" \
                                  "{{\n" \
                                  "   kill -9 $pid    \n" \
                                  "}}\n" \
                                  "else\n" \
                                  "       echo \"{} is not running\"\n".format(i["path"], i["path"])
                i["stop_script"] = stop_script

                port_data = self.get_resource_client().run_one_command("netstat -plnt |grep %s|awk '{print $4}'|grep -o -G [0-9]*$"%(str(i["proc"])))
                if port_data is not None and len(port_data)>0 and type(port_data) == list:
                    i["port"] = ",".join(port_data)

        return data

    def service_to_jar_list(self):
        """
        打印出所有java -jar 启动的服务
        """
        jar_list = self.resource.run_one_command('ps -ef |grep -P "java.*?-jar.*"|grep -v grep')
        if jar_list is not None and len(jar_list) != 0:
            patten_string = r'(.*?)\s+?([0-9]+).*?java\s+-jar\s+([^\s]*)'
            pattern = re.compile(patten_string, re.S)
            data_temp = []
            for i in jar_list:
                shuju = re.findall(pattern, i)
                if len(shuju) > 0:
                    data_temp.append(
                        {
                            "user": shuju[0][0],
                            "proc": shuju[0][1],
                            "path": shuju[0][2],
                            "ps": i,
                            "port":self.get_service_port(shuju[0][1])
                        }
                    )
            return data_temp
    def service_jar_extend(self):
        """
        :return:
        """
        data = self.service_to_jar_list()

        if data is not None:
            for i in data:
                patten_string = r'--spring\.profiles\.active=(.*)'
                pattern = re.compile(patten_string, re.S)
                huanjing_data = re.findall(pattern,i["ps"])
                if huanjing_data is not None and len(huanjing_data)>0:
                    huanjing_data = huanjing_data[0].strip()
                restart_script = "#!/bin/sh \n" \
                                  "pid=`ps -ef|grep {} |grep -v \"grep\"|awk '{{print $2}}'`\n" \
                                  "if [ -n \"$pid\" ];then\n" \
                                  "{{\n" \
                                  "     kill -9 $pid \n" \
                                  "}}\n" \
                                  "else\n" \
                                  "echo  ' {}'\n" \
                                  "fi\n" \
                                  "cd {}\n" \
                                  "nohup java -jar {} --spring.profiles.active=prod > {} &".format(
                                                            i["path"],
                                                            i["path"],
                                                            i["path"],
                                                            i["path"],
                                                            i["path"] + '.log')
                i["restart_script"] = restart_script

                stop_script = "#!/bin/sh \n" \
                                 "pid=`ps -ef|grep {} |grep -v \"grep\"|awk '{{print $2}}'`\n" \
                                 "if [ -n \"$pid\" ];then\n" \
                                 "{{\n" \
                                 "     kill -9 $pid \n" \
                                 "}}\n" \
                                 "else\n" \
                                 "echo  ' {}'\n" \
                                 "fi\n".format(i["path"],i["path"])
                i["stop_script"] = stop_script
                port_data = self.get_resource_client().run_one_command("netstat -plnt |grep %s|awk '{print $4}'|grep -o -G [0-9]*$" % (str(i["proc"])))
                if port_data is not None and len(port_data) > 0 and type(port_data) == list:
                    i["port"] = ",".join(port_data)
        return data


    def application_kill(self):
        pass

    def service_restart_tomcat(self, path):
        pass

    def close_source(self):
        if self.resource is not None:
            self.resource.close_source()

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



class bianlixunhuan:
    """
    仅用于遍历循环 不用关闭资源 在linux连接流 中工作
    """
    resource = None

    def __init__(self,get_info_object):
        self.resource = get_info_object

    data_temp_file = []

    def remote_dir_list_digui(self,path):
        """
        递归查询该文件夹的文件
        :param path:
        :return:
        """
        list_dir = self.resource.get_resource_Sftp().get_path_Sftp_listdir_attr(path)
        for i in list_dir:
            if S_ISDIR(i.st_mode):
                self.remote_dir_list_digui(path+'/'+i.filename)
            else:
                self.data_temp_file.append(path+'/'+i.filename)
    def get_wenjian_list(self,remote_path):
        """

        :return:
        """
        self.remote_dir_list_digui(remote_path)

        return self.data_temp_file