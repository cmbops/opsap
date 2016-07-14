# coding: utf-8
# Author: Dunkle Qiu

import logging
import subprocess
from opsap.settings import *
from django.http import QueryDict
from rest_framework.parsers import DataAndFiles


# 定义全局常量
class ROLES(object):
    """用户角色"""
    SU = ('SU', 'SuperUser')
    GM = ('GM', 'GroupManager')
    CU = ('CU', 'CommonUser')
    SN = ('SN', 'ServiceNode')

    @classmethod
    def as_choice(cls):
        return cls.SU, cls.GM, cls.CU, cls.SN,


class OSTYPES(object):
    """操作系统类型"""
    WIN = ('Windows', 'Windows OS')
    LNX = ('Linux', 'Linux OS')

    @classmethod
    def as_choice(cls):
        return cls.WIN, cls.LNX,


# 基础处理函数
def split(str_li, sep=','):
    if not (isinstance(sep, str) and len(sep) == 1):
        raise TypeError("Sep should be a simple char such as ','")
    if not str_li:
        return []
    return str_li.split(sep)


def ip_bin2str(i_bin):
    if len(i_bin) < 32:
        i_bin = i_bin.rjust(32, str(0))
    i_raw = [i_bin[i * 8:(i + 1) * 8] for i in range(4)]
    i_str = [str(int(subn, 2)) for subn in i_raw]
    return '.'.join(i_str)


def ip_str2bin(i_str):
    i_raw = [bin(int(subn)) for subn in i_str.split('.')]
    if len(i_raw) != 4:
        return '0' * 32
    i_bin = [subn[2:].rjust(8, str(0)) for subn in i_raw]
    return ''.join(i_bin)


def ping(host, count=2, wait=2):
    args = ['ping', '-c', str(count), '-w', str(wait), host]
    status = subprocess.Popen(args).wait()
    return status == 0


def set_log(level, filename='opsap.log'):
    """
    根据提示设置log打印
    """
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_file = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(log_file):
        os.mknod(log_file)
        os.chmod(log_file, 0644)
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}
    logger_f = logging.getLogger('opsap')
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f


logger = set_log(LOG_LEVEL)


def bash(cmd):
    """
    执行bash命令
    """
    return subprocess.call(cmd, shell=True)


# 请求处理
def post_data_to_dict(data):
    """
    将request.data类型统一为dict
    """
    if isinstance(data, QueryDict):
        return data.dict()
    elif isinstance(data, DataAndFiles):
        return data.data.dict()
    else:
        return data
