#!/usr/bin/python
# coding: utf-8

import os
import socket
import sys

import django
from django.core.management import call_command

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'opsap.settings'
setup = django.setup()

from ouser.models import ExUser
from install import color_print
from opsap.settings import FUNC_APPS

socket.setdefaulttimeout(2)


class Setup(object):
    """
    安装jumpserver向导
    """

    def __init__(self):
        self.admin_user = 'admin'
        self.admin_pass = 'admin'
        self.admin_email = 'admin@admin.org'

    def _input_admin(self):
        while True:
            print
            admin_user = raw_input('请输入管理员用户名 [%s]: ' % self.admin_user).strip()
            admin_pass = raw_input('请输入管理员密码: [%s]: ' % self.admin_pass).strip()
            admin_pass_again = raw_input('请再次输入管理员密码: [%s]: ' % self.admin_pass).strip()

            if admin_user:
                self.admin_user = admin_user
            if not admin_pass_again:
                admin_pass_again = self.admin_pass
            if admin_pass:
                self.admin_pass = admin_pass
            if self.admin_pass != admin_pass_again:
                color_print('两次密码不相同请重新输入')
            else:
                break
            print

    @staticmethod
    def _migrate():
        os.chdir(BASE_DIR)
        call_command('makemigrations', *FUNC_APPS)
        call_command('migrate')

    def _create_admin(self):
        ExUser.objects.create_superuser(self.admin_user,email=self.admin_email,password=self.admin_pass,
                                        name=u'超级管理员')

    def _db_initial_params(self):
        # call_command('loaddata', os.path.join(BASE_DIR, 'install/initial_data/ovm.json'))
        pass

    @staticmethod
    def _run_service():
        os.system('sh %s start' % os.path.join(BASE_DIR, 'service.sh'))
        print
        color_print('安装成功，请访问web页面, 祝您使用愉快!', 'green')

    def start(self):
        print "开始安装运维自动化平台, 标准环境为 CentOS 6.7 x86_64"
        self._migrate()
        self._input_admin()
        self._create_admin()
        self._db_initial_params()
        self._run_service()


if __name__ == '__main__':
    setup = Setup()
    setup.start()
