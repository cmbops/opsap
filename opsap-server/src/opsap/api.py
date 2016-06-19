# coding: utf-8

import hashlib
import json
import logging
import random
import subprocess
import uuid
from binascii import b2a_hex, a2b_hex

#import crypt
import pwd
#from Crypto.Cipher import AES
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import permissions

from ouser.models import ExUser,Group
from .models import *
from .settings import *


def chown(path, user, group=''):
    if not group:
        group = user
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(group).pw_gid
        os.chown(path, uid, gid)
    except KeyError:
        pass


def mkdir(dir_name, username='', mode=0755):
    """
    insure the dir exist and mode ok
    目录存在，如果不存在就建立，并且权限正确
    """
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
        os.chmod(dir_name, mode)
    if username:
        chown(dir_name, username)


def set_log(level, filename='opsap.log'):
    """
    return a log file object
    根据提示设置log打印
    """
    mkdir(LOG_DIR)
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


# def list_drop_str(a_list, a_str):
#     for i in a_list:
#         if i == a_str:
#             a_list.remove(a_str)
#     return a_list
#
#
# class PyCrypt(object):
#     """
#     This class used to encrypt and decrypt password.
#     加密类
#     """
#
#     def __init__(self, key):
#         self.key = key
#         self.mode = AES.MODE_CBC
#
#     @staticmethod
#     def gen_rand_pass(length=16, especial=False):
#         """
#         random password
#         随机生成密码
#         """
#         salt_key = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
#         symbol = '!@$%^&*()_'
#         salt_list = []
#         if especial:
#             for i in range(length - 4):
#                 salt_list.append(random.choice(salt_key))
#             for i in range(4):
#                 salt_list.append(random.choice(symbol))
#         else:
#             for i in range(length):
#                 salt_list.append(random.choice(salt_key))
#         salt = ''.join(salt_list)
#         return salt
#
#     @staticmethod
#     def md5_crypt(string):
#         """
#         md5 encrypt method
#         md5非对称加密方法
#         """
#         return hashlib.new("md5", string).hexdigest()
#
#     @staticmethod
#     def gen_sha512(salt, password):
#         """
#         generate sha512 format password
#         生成sha512加密密码
#         """
#         return crypt.crypt(password, '$6$%s$' % salt)
#
#     def encrypt(self, passwd=None, length=32):
#         """
#         encrypt gen password
#         对称加密之加密生成密码
#         """
#         if not passwd:
#             passwd = self.gen_rand_pass()
#
#         cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
#         try:
#             count = len(passwd)
#         except TypeError:
#             raise ServerError('Encrypt password error, TYpe error.')
#
#         add = (length - (count % length))
#         passwd += ('\0' * add)
#         cipher_text = cryptor.encrypt(passwd)
#         return b2a_hex(cipher_text)
#
#     def decrypt(self, text):
#         """
#         decrypt pass base the same key
#         对称加密之解密，同一个加密随机数
#         """
#         cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
#         try:
#             plain_text = cryptor.decrypt(a2b_hex(text))
#         except TypeError:
#             raise ServerError('Decrypt password error, TYpe error.')
#         return plain_text.rstrip('\0')


class ServerError(Exception):
    """
    self define exception
    自定义异常
    """
    pass


def get_object(model, **kwargs):
    """
    use this function for query
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


def get_options(app, name):
    """
    根据应用名、表单名获取动态表单选项
    """
    return ParaOption.objects.filter(setting_type='option', app=app, name=name)


def add_option(app, name, value, display='', **ext_attr):
    """
    在指定的表单下，添加选项，如果已存在则更新选项
    """
    defaut_dict = {}
    if display:
        defaut_dict['display'] = display
    if ext_attr:

        defaut_dict['ext_attr'] = json.dumps(ext_attr)
    return ParaOption.objects.update_or_create(defaults=defaut_dict, setting_type='option', app=app, name=name,
                                               value=value)


def modify_option(app, name, value, display='', ext_attr=None):
    """
    修改指定的表单选项
    注：value不可修改，只支持增删
    """
    modify = False
    try:
        obj = ParaOption.objects.get(setting_type='option', app=app, name=name, value=value)
        if display:
            modify = True
            obj.display = display
        if ext_attr and isinstance(ext_attr, dict):
            modify = True
            obj.ext_attr = json.dumps(ext_attr)
        if modify:
            obj.save()
        return modify
    except:
        return False


def delete_options(app, name, values):
    """
    删除指定的动态表单选项
    """
    if isinstance(values, str):
        ParaOption.objects.filter(setting_type='option', app=app, name=name, value=values).delete()
    elif isinstance(values, list):
        ParaOption.objects.filter(setting_type='option', app=app, name=name, value__in=values).delete()


def get_param(app, name, default_value=''):
    """
    根据应用名、参数名获取参数, 如获取失败，自动添加由default_value指定的参数项
    """
    if default_value:
        defaut_dict = {'value': default_value}
        return ParaOption.objects.get_or_create(defaults=defaut_dict, setting_type='param', app=app, name=name)
    else:
        try:
            return ParaOption.objects.get(setting_type='param', app=app, name=name), False
        except ObjectDoesNotExist:
            return None


def set_param(app, name, value, display='', ext_attr=None):
    """
    设置应用参数
    """
    defaut_dict = {'value': value}
    if display:
        defaut_dict['display'] = display
    if ext_attr and isinstance(ext_attr, dict):
        defaut_dict['ext_attr'] = json.dumps(ext_attr)
    return ParaOption.objects.update_or_create(defaults=defaut_dict, setting_type='param', app=app, name=name)


def require_role(role='CU'):
    """
    验证用户是某种角色 ['SU','GM','CU','SN']的函数
    """
    class RoleAuthenticated(permissions.IsAuthenticated):
        message = "Permission denied, role of %s or above is required" % role

        def has_permission(self, request, view):
            is_auth = super(RoleAuthenticated,self).has_permission(request, view)
            if not is_auth:
                return False
            user_role = request.user.role
            if user_role=='SU':
                return True
            elif role in ['SN','GM']:
                return user_role==role
            elif role=='CU':
                return user_role in ['GM','CU']
            else:
                return False

    return RoleAuthenticated

def require_groups(groups=None):
    """
    验证用户属于某个群组
    """
    if not groups:
        return permissions.IsAuthenticated
    if isinstance(groups, str):
        groups = [groups]
    assert type(groups) in (tuple, list), "Type Error: groups must be a tuple or a list."

    class GroupAuthenticated(permissions.IsAuthenticated):
        message = "Permission denied, only members in \"%s\" is permitted" % ("".join(groups))

        def has_permission(self, request, view):
            is_auth = super(GroupAuthenticated,self).has_permission(request, view)
            if not is_auth:
                return False
            group_set = Group.objects.filter(name__in=groups)
            if group_set.exists():
                for group in  request.user.groups:
                    if group in group_set:
                        return True
                return False
            else:
                return False

    return GroupAuthenticated




# def require_role(role='user'):
#     """
#     decorator for require user role in ["super", "admin", "user"]
#     要求用户是某种角色 ["super", "admin", "user"]的装饰器
#     """
#
#     def _deco(func):
#         def __deco(request, *args, **kwargs):
#             request.session['pre_url'] = request.path
#             if not request.user.is_authenticated():
#                 return HttpResponseRedirect(reverse('login'))
#             if role == 'admin':
#                 # if request.session.get('role_id', 0) < 1:
#                 if request.user.role == 'CU':
#                     return HttpResponseRedirect(reverse('index'))
#             elif role == 'super':
#                 # if request.session.get('role_id', 0) < 2:
#                 if request.user.role in ['CU', 'GA']:
#                     return HttpResponseRedirect(reverse('index'))
#             return func(request, *args, **kwargs)
#
#         return __deco
#
#     return _deco

#
# def is_role_request(request, role='user'):
#     """
#     require this request of user is right
#     要求请求角色正确
#     """
#     role_all = {'user': 'CU', 'admin': 'GA', 'super': 'SU'}
#     if request.user.role == role_all.get(role, 'CU'):
#         return True
#     else:
#         return False
#
#
# # require_role
# def get_session_user_info(request):
#     """
#     get the user info of the user in session, for example id, username etc.
#     获取用户的信息
#     """
#     return [request.user.id, request.user.username, request.user]


def bash(cmd):
    """
    run a bash shell command
    执行bash命令
    """
    return subprocess.call(cmd, shell=True)



# def defend_attack(func):
#     def _deco(request, *args, **kwargs):
#         if int(request.session.get('visit', 1)) > 10:
#             logger.debug('请求次数: %s' % request.session.get('visit', 1))
#             return HttpResponse('Forbidden', status=403)
#         request.session['visit'] = request.session.get('visit', 1) + 1
#         request.session.set_expiry(300)
#         return func(request, *args, **kwargs)
#
#     return _deco


# def get_mac_address():
#     node = uuid.getnode()
#     mac = uuid.UUID(int=node).hex[-12:]
#     return mac
