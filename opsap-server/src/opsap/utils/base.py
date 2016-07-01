# coding: utf-8
# Author: Dunkle Qiu

import pwd
import logging
import subprocess
from opsap.settings import *
from django.http import QueryDict
from rest_framework.parsers import DataAndFiles

def set_log(level, filename='opsap.log'):
    """
    return a log file object
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


def get_object(model, **kwargs):
    """
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object


def bash(cmd):
    """
    run a bash shell command
    执行bash命令
    """
    return subprocess.call(cmd, shell=True)


def post_data_to_dict(data):
    if isinstance(data, QueryDict):
        return data.dict()
    elif isinstance(data, DataAndFiles):
        return data.data.dict()
    else:
        return data