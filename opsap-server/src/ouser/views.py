# coding: utf-8
# Author: Dunkle Qiu

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from ouser.permissions import *
from opsap.utils.decorators import post_validated_fields, status, post_data_to_dict
from opsap.utils.base import logger

from ouser.serializers import ExUserSerializer, ExGroupSerializer
from ouser.user_api import *


@api_view(['POST'])
@permission_classes((require_role('SU'),))
@post_validated_fields(require=['username', 'email', 'password'])
def user_add(request):
    """
    添加用户

    * 权限 - 超级管理员(SU)
    * 参数
    ** username - 用户名称
    ** email - 邮箱地址
    ** password - 密码
    ** name - 显示名称
    ** role - 角色(CU/GM/SN), SU只通过后台创建
    """
    msg_prefix = u"添加用户 %s "
    req_dict = post_data_to_dict(request.data)

    username = req_dict.pop('username')
    email = req_dict.pop('email')
    password = req_dict.pop('password')

    name = req_dict.pop('name', '')
    role = req_dict.pop('role', 'CU')
    try:
        if ExUser.objects.filter(username=username):
            raise Exception(u'用户名已存在')
        user = ExUser.objects.create_user(username, email, password, name, role)
        serializer = ExUserSerializer(user)
    except Exception, e:
        msg = (msg_prefix % username) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % username) + u"成功!"
        return Response({"status": 1, "msg": msg, "data": serializer.data})


@api_view(['GET'])
@permission_classes((require_role('SU'),))
def user_list(request):
    """
    获取用户列表

    * 权限 - 超级管理员(SU)
    """
    msg_prefix = u"获取用户列表 "
    try:
        user_list = ExUser.objects.all()
        serializer = ExUserSerializer(user_list, many=True)
    except Exception, e:
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 0, "msg": msg, "data": serializer.data})


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def user_detail(request):
    """
    获取用户详情

    * 权限 - 登陆用户
    * 参数
    ** username/id - 用户名称/用户id
    """
    msg_prefix = u"获取用户详情 "
    req_user = request.user
    try:
        if request.method == 'GET':
            user = req_user
        if request.method == 'POST':
            req_dict = post_data_to_dict(request.data)
            username = req_dict.pop('username', '')
            id = req_dict.pop('id', '')
            if username:
                user = ExUser.objects.get(username=username)
            elif id:
                user = ExUser.objects.get(pk=int(id))
            if req_user.role != 'SU' and not req_user.mana_group_set.filter(user=user).exist():
                raise PermissionDenied(u"当前用户不具备该权限!")
        serializer = ExUserSerializer(user)
    except Exception, e:
        if isinstance(e,PermissionDenied):
            raise e
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 0, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role('CU'),))
@post_validated_fields(require_one=['username', 'id'])
def user_edit(request):
    """
    修改用户信息

    * 权限 - 普通用户(CU)
    * 参数
    ** username/id - 用户名称/用户id
    ** email - 邮箱地址
    ** password - 密码
    ** name - 显示名称
    ** role - 角色(CU/GM/SN), SU只通过后台创建
    """
    msg_prefix = u"修改用户信息 %s "
    req_dict = post_data_to_dict(request.data)
    req_user = request.user

    username = req_dict.pop('username', '')
    id = req_dict.pop('id', '')
    email = req_dict.pop('email', '')
    password = req_dict.pop('password', '')
    name = req_dict.pop('name', '')
    role = req_dict.pop('role', '')



    try:
        if username:
            user = ExUser.objects.get(username=username)
        elif id:
            user = ExUser.objects.get(pk=int(id))
        if req_user.role != 'SU' and req_user != user:
            raise PermissionDenied(u"当前用户不具备该权限!")

        if email:
            user.email = email
        if role and req_user.role == 'SU':
            user.role = role
            user.is_superuser = (role == 'SU')
            user.is_staff = (role == 'SU')
        if name:
            user.name = name
        if password:
            user.set_password(password=password)
        user.save()
        serializer = ExUserSerializer(user)
    except Exception, e:
        if isinstance(e,PermissionDenied):
            raise e
        msg = (msg_prefix % username) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % username) + u"成功!"
        return Response({"status": 1, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
@post_validated_fields(require=['username', 'id'])
def user_delete(request):
    """
    删除用户

    * 权限 - 超级管理员(SU)
    * 需同时提供用户名及id列表
    * 参数
    ** username - 用户名称(','号分隔列表)
    ** id - 用户id(','号分隔列表)
    """
    msg_prefix = u"删除用户 "
    req_dict = post_data_to_dict(request.data)
    req_user = request.user
    username = req_dict.pop('username').split(',')
    id = req_dict.pop('id').split(',')
    try:
        user_set = ExUser.objects.filter(id__in=id).filter(username__in=username)
        if not user_set.exists():
            raise Exception(u"没有符合条件的用户")
        if req_user in user_set:
            raise Exception(u"不能删除当前用户!")
        data = list(user_set.values('id', 'username', 'name', 'role'))
        user_set.delete()
    except Exception, e:
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 1, "msg": msg, "data": data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
@post_validated_fields(require=['name'])
def group_add(request):
    """
    添加用户组

    * 权限 - 超级管理员(SU)
    * 参数
    ** name - 用户组名称
    ** comment - 用户组描述
    ** users_id - 初始用户(id)(','号分隔列表)
    ** member_type - 成员类型 staff/service (默认staff)
    ** managers_id - 管理用户(id)(','号分隔列表)
    """
    msg_prefix = u"添加用户组 %s "
    req_dict = post_data_to_dict(request.data)

    name = req_dict.pop('name')
    users_id = req_dict.pop('users_id', '').split(',')
    managers_id = req_dict.pop('managers_id', '').split(',')
    comment = req_dict.pop('comment', '')
    member_type = req_dict.pop('member_type','staff')
    try:
        if Group.objects.filter(name=name):
            raise Exception(u'组名已存在')
        group = ExGroup.objects.create(name=name, comment=comment, member_type=member_type)
        logger.debug(users_id)
        group_add_users(group, *users_id)
        group_add_manager(group, *managers_id)
        serializer = ExGroupSerializer(group)
    except Exception, e:
        msg = (msg_prefix % name) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % name) + u"成功!"
        return Response({"status": 1, "msg": msg, "data": serializer.data})


@api_view(['GET'])
@permission_classes((require_role('SU'),))
def group_list(request):
    """
    用户组列表

    * 权限 - 超级管理员(SU)
    * 参数
    ** search - 用户组名称(可选)
    ** id - 组id(可选)
    """
    keyword = request.GET.get('search', '')
    group_id = request.GET.get('id', '')
    user_group_list = ExGroup.objects.all().order_by('name')
    many = True

    if keyword:
        user_group_list = user_group_list.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword))

    if group_id:
        many = False
        user_group_list = user_group_list.filter(id=int(group_id))

    serializer = ExGroupSerializer(user_group_list, many=many)
    return Response({"status": "success", "msg": "", "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
def group_delete(request):
    """
    删除用户组

    * 权限 - 超级管理员(SU)
    * 参数
    ** id - 组id(列表)
    """
    group_id_list = request.POST.getlist('id', '')
    for group_id in group_id_list:
        ExGroup.objects.filter(id=group_id).delete()
    msg = u'删除组成功'
    return Response({"status": "success", "msg": msg, "data": {}})
