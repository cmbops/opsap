# coding: utf-8
# Author: Dunkle Qiu

from .models import ExUser, ExGroup


def group_add_users(group, *user_id):
    """
    用户组中添加用户
    """
    count = 0
    for val in user_id:
        if isinstance(val, int):
            user = ExUser.objects.filter(pk=val)
        elif val:
            user = ExUser.objects.filter(pk=int(val))
        else:
            continue
        if user.exists():
            group.user_set.add(user[0])
        count += 1
    return count


def group_add_manager(group, *user_id):
    """
    用户组中添加组管理员
    """
    count = 0
    if not isinstance(group, ExGroup):
        raise TypeError("group must be ExGroup")
    for val in user_id:
        if isinstance(val, int):
            user = ExUser.objects.filter(pk=val)
        elif val:
            user = ExUser.objects.filter(pk=int(val))
        else:
            continue
        if user.exists():
            group.managers.add(user[0])
        count += 1
    return count


#
# def user_add_mail(user, kwargs):
#     """
#     add user send mail
#     发送用户添加邮件
#     """
#     user_role = {'SU': u'超级管理员', 'GA': u'组管理员', 'CU': u'普通用户'}
#     mail_title = u'恭喜你的跳板机用户 %s 添加成功 Jumpserver' % user.name
#     mail_msg = u"""
#     Hi, %s
#         您的用户名： %s
#         您的权限： %s
#         您的web登录密码： %s
#         您的ssh密钥文件密码： %s
#         密钥下载地址： %s/ouser/key/down/?uuid=%s
#         说明： 请登陆后再下载密钥！
#     """ % (user.name, user.username, user_role.get(user.role, u'普通用户'),
#            kwargs.get('password'), kwargs.get('ssh_key_pwd'), URL, user.uuid)
#
