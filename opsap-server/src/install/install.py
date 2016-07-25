#!/usr/bin/python
# coding: utf-8

import ConfigParser
import os
import random
import socket
import string
import struct
import subprocess
import sys
import time
from smtplib import SMTP

import MySQLdb
import fcntl

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)


def bash(cmd):
    """
    run a bash shell command
    执行bash命令
    """
    return subprocess.call(cmd, shell=True)


def color_print(msg, color='red', exits=False):
    """
    Print colorful string.
    颜色打印字符或者退出
    """
    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg
    if exits:
        time.sleep(2)
        sys.exit()
    return msg


def get_ip_addr(ifname='eth0'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        ips = os.popen(
            "LANG=C ifconfig | grep \"inet addr\" | grep -v \"127.0.0.1\" | awk -F \":\" '{print $2}' | awk '{print $1}'").readlines()
        if len(ips) > 0:
            return ips[0].strip()
    return ''


class PreSetup(object):
    def __init__(self):
        self.db_host = '127.0.0.1'
        self.db_port = 3306
        self.db_user = 'opsap'
        self.db_pass = 'opsap'
        self.db = 'opsap'
        self.mail_enable = True
        self.mail_host = ''
        self.mail_port = 25
        self.mail_addr = ''
        self.mail_pass = ''
        self.ip = ''
        self.log = 'debug'
        self.key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
                           for _ in range(16))

    def write_conf(self, conf_file=os.path.join(BASE_DIR, 'opsap.conf')):
        color_print('开始写入配置文件', 'green')
        conf = ConfigParser.ConfigParser()
        conf.read(conf_file)
        if not conf.has_section('base'):
            conf.add_section('base')
        if not conf.has_section('db'):
            conf.add_section('db')
        if not conf.has_section('websocket'):
            conf.add_section('websocket')
        if not conf.has_section('mail'):
            conf.add_section('mail')
        conf.set('base', 'url', 'http://%s' % self.ip)
        conf.set('base', 'key', self.key)
        conf.set('base', 'log', self.log)
        conf.set('db', 'host', self.db_host)
        conf.set('db', 'port', self.db_port)
        conf.set('db', 'user', self.db_user)
        conf.set('db', 'password', self.db_pass)
        conf.set('db', 'database', self.db)
        conf.set('websocket', 'web_socket_host', '%s:3000' % self.ip)
        conf.set('mail', 'mail_enable', self.mail_enable)
        conf.set('mail', 'email_host', self.mail_host)
        conf.set('mail', 'email_port', self.mail_port)
        conf.set('mail', 'email_host_user', self.mail_addr)
        conf.set('mail', 'email_host_password', self.mail_pass)

        with open(conf_file, 'w') as f:
            conf.write(f)

    def _setup_mysql(self):
        color_print('开始安装设置mysql (请手动设置mysql安全)', 'green')
        color_print('默认用户名: %s 默认密码: %s' % (self.db_user, self.db_pass), 'green')
        use_yum = raw_input('是否从yum获取版本自动安装? (y/n) [y]: ')
        if use_yum != 'n':
            bash('yum -y install mysql-server')
        elif raw_input("选择手动安装mysql, 完成后回车继续, 或使用Ctrl+C退出安装程序..."):
            pass
        bash('service mysqld start')
        bash('mysql -e "create database %s default charset=utf8"' % self.db)
        bash('mysql -e "grant all on %s.* to \'%s\'@\'%s\' identified by \'%s\'"' % (self.db,
                                                                                     self.db_user,
                                                                                     self.db_host,
                                                                                     self.db_pass))

    @staticmethod
    def _set_env():
        color_print('开始关闭防火墙和selinux', 'green')
        os.system("export LANG='en_US.UTF-8' && sed -i 's/LANG=.*/LANG=\"en_US.UTF-8\"/g' /etc/sysconfig/i18n")
        bash('service iptables stop && chkconfig iptables off && setenforce 0')

    def _test_db_conn(self):
        try:
            MySQLdb.connect(host=self.db_host, port=int(self.db_port),
                            user=self.db_user, passwd=self.db_pass, db=self.db)
            color_print('连接数据库成功', 'green')
            return True
        except MySQLdb.OperationalError, e:
            color_print('数据库连接失败 %s' % e, 'red')
            return False

    def _test_mail(self):
        try:
            smtp = SMTP(self.mail_host, port=self.mail_port, timeout=2)
            smtp.login(self.mail_addr, self.mail_pass)
            smtp.sendmail(self.mail_addr, (self.mail_addr,),
                          '''From:%s\r\nTo:%s\r\nSubject: Mail Test!\r\n\r\n  Mail test passed!\r\n''' %
                          (self.mail_addr, self.mail_addr))
            smtp.quit()
            return True

        except Exception, e:
            color_print(e, 'red')
            skip = raw_input('邮件测试失败, 是否跳过(y/n) [n]? : ')
            if skip == 'y':
                return True
            return False

    def _input_ip(self):
        ip = raw_input('\n请输入您服务器的IP地址，用户浏览器可以访问 [%s]: ' % get_ip_addr()).strip()
        self.ip = ip if ip else get_ip_addr()

    def _input_mysql(self):
        while True:
            mysql = raw_input('是否安装新的MySQL服务器? (y/n) [y]: ')
            if mysql != 'n':
                self._setup_mysql()
            else:
                db_host = raw_input('请输入数据库服务器IP [127.0.0.1]: ').strip()
                db_port = raw_input('请输入数据库服务器端口 [3306]: ').strip()
                db_user = raw_input('请输入数据库服务器用户 [opsap]: ').strip()
                db_pass = raw_input('请输入数据库服务器密码: ').strip()
                db = raw_input('请输入使用的数据库 [opsap]: ').strip()

                if db_host: self.db_host = db_host
                if db_port: self.db_port = db_port
                if db_user: self.db_user = db_user
                if db_pass: self.db_pass = db_pass
                if db: self.db = db

            if self._test_db_conn():
                break

            print

    def _input_smtp(self):

        while True:
            mail_enable = raw_input('是否启用邮件功能? (y/n) [y]: ')
            if mail_enable == 'n':
                self.mail_enable = False
                break
            self.mail_host = raw_input('请输入SMTP地址: ').strip()
            mail_port = raw_input('请输入SMTP端口 [25]: ').strip()
            self.mail_addr = raw_input('请输入账户: ').strip()
            self.mail_pass = raw_input('请输入密码: ').strip()

            if mail_port: self.mail_port = int(mail_port)

            if self._test_mail():
                color_print('\n\t请登陆邮箱查收邮件, 然后确认是否继续安装\n', 'green')
                smtp = raw_input('是否继续? (y/n) [y]: ')
                if smtp == 'n':
                    continue
                else:
                    break
            print

    def start(self):
        color_print('OPSAP运维自动化平台安装开始....')
        time.sleep(3)
        self._set_env()
        self._input_ip()
        self._input_mysql()
        self._input_smtp()
        self.write_conf()
        os.system('python %s' % os.path.join(BASE_DIR, 'install/next.py'))


if __name__ == '__main__':
    pre_setup = PreSetup()
    pre_setup.start()
