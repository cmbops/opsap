# coding: utf-8
# Author: Dunkle Qiu

from opsap.models import DataDict


class EnvType(object):
    def __init__(self):
        self.set = DataDict.options.get_options('ovm', 'env_type')
        self.value = [option.value for option in self.set]


class OsVersion(object):
    def __init__(self):
        self.set = DataDict.options.get_options('ovm', 'os_version')
        self.value = {'Windows': [option.value for option in self.set if option.ext_attr['os_type'] == 'Windows'],
                      'Linux': [option.value for option in self.set if option.ext_attr['os_type'] == 'Linux']}
