# coding: utf-8
# Author: Dunkle Qiu

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from ouser.permissions import *
from opsap.utils.decorators import post_validated_fields, status, post_data_to_dict
from opsap.utils.base import logger, split

from ouser.serializers import ExUserSerializer, ExGroupSerializer
from ouser.utils import *


@api_view(['POST'])
@permission_classes((require_role(ROLES.SU[0]),))
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


@api_view(['GET', 'POST'])
@permission_classes((require_role(ROLES.GM[0]),))
def user_list(request):
    """
    获取用户列表

    * 权限 - 超级管理员(SU)
    * 参数
    ** search - 搜索匹配(用户名/显示名/邮箱)
    ** roles - 匹配角色(','号分隔列表)
    ** group_ids - 匹配用户组(','号分隔列表)
    """
    msg_prefix = u"获取用户列表 "
    req_user = request.user
    try:
        if req_user.role == 'SU':
            users = ExUser.objects.all()
        else:
            users = ExUser.objects.none()
            for group in req_user.mana_group_set:
                users = users | group.users
        if request.method == 'POST':
            req_dict = post_data_to_dict(request.data)
            keyword = req_dict.pop('search', '')
            roles = split(req_dict.pop('role', ''))
            groups = split(req_dict.pop('group_ids', ''))
            if keyword:
                users = users.filter(
                    Q(username__icontains=keyword) | Q(name__icontains=keyword) | Q(email__icontains=keyword))
            if roles:
                users = users.filter(role__in=roles)
            if groups:
                users = users.filter(groups__in=groups)
        serializer = ExUserSerializer(users, many=True)
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
        else:
            req_dict = post_data_to_dict(request.data)
            username = req_dict.pop('username', '')
            id = req_dict.pop('id', '')
            if username:
                user = ExUser.objects.get(username=username)
            else:
                user = ExUser.objects.get(pk=int(id))
            if req_user.role != 'SU' and not req_user.mana_group_set.filter(user=user).exist():
                raise PermissionDenied(u"当前用户不具备该权限!")
        serializer = ExUserSerializer(user)
    except Exception, e:
        if isinstance(e, PermissionDenied):
            raise e
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 0, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role(ROLES.CU[0]),))
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
        else:
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
        if isinstance(e, PermissionDenied):
            raise e
        msg = (msg_prefix % username) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % username) + u"成功!"
        return Response({"status": 1, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role(ROLES.SU[0]),))
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
    username = split(req_dict.pop('username'))
    id = split(req_dict.pop('id'))
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
@permission_classes((require_role(ROLES.SU[0]),))
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
    users_id = split(req_dict.pop('users_id', ''))
    managers_id = split(req_dict.pop('managers_id', ''))
    comment = req_dict.pop('comment', '')
    member_type = req_dict.pop('member_type', 'staff')
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


@api_view(['GET', 'POST'])
@permission_classes((require_role(ROLES.GM[0]),))
def group_list(request):
    """
    用户组列表

    * 权限 - 超级管理员(SU)
    * 参数
    ** search - 用户组名称
    ** type - 用户类型
    """
    msg_prefix = u"获取用户组列表 "
    req_user = request.user
    try:
        if req_user.role == 'SU':
            groups = ExGroup.objects.all()
        else:
            groups = req_user.mana_group_set
        if request.method == 'POST':
            req_dict = post_data_to_dict(request.data)
            keyword = req_dict.pop('search', '')
            member_type = req_dict.pop('type', '').lower()
            if keyword:
                groups = groups.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword))
            if member_type:
                groups = groups.filter(member_type=member_type)
        serializer = ExGroupSerializer(groups, many=True)
    except Exception, e:
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 0, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role(ROLES.SU[0]),))
@post_validated_fields(require_one=['name', 'id'])
def group_edit(request):
    """
    修改用户信息

    * 权限 - 普通用户(CU)
    * 参数
    ** name/id - 用户组名称/id
    ** comment - 备注
    ** member_type - 成员类型 staff/service
    ** users_id/users_id_add - 用户/添加用户(id)(','号分隔列表)
    ** managers_id/managers_id_add - 管理用户/添加管理用户(id)(','号分隔列表)
    """
    msg_prefix = u"修改用户组信息 %s "
    req_dict = post_data_to_dict(request.data)

    name = req_dict.pop('name', '')
    id = req_dict.pop('id', '')
    comment = req_dict.pop('comment', '')
    member_type = req_dict.pop('member_type', '')
    users_id = split(req_dict.pop('users_id', ''))
    users_id_add = split(req_dict.pop('users_id_add', ''))
    managers_id = split(req_dict.pop('managers_id', ''))
    managers_id_add = split(req_dict.pop('managers_id_add', ''))
    try:
        # 获取用户组
        if name:
            group = ExGroup.objects.get(name=name)
        else:
            group = ExGroup.objects.get(pk=int(id))
        # 修改信息
        if comment:
            group.comment = comment
        if member_type:
            group.member_type = member_type

        if users_id:
            group.user_set.clear()
            users_id_add += users_id
        if users_id_add:
            group_add_users(group, *users_id_add)

        if managers_id:
            group.managers.clear()
            managers_id_add += managers_id
        if managers_id_add:
            group_add_manager(group, *managers_id_add)

        serializer = ExGroupSerializer(group)
    except Exception, e:
        msg = (msg_prefix % name) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % name) + u"成功!"
        return Response({"status": 1, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role(ROLES.SU[0]),))
@post_validated_fields(require=['name', 'id'])
def group_delete(request):
    """
    删除用户组

    * 权限 - 超级管理员(SU)
    * 需同时提供用户组名称及id列表
    * 参数
    ** name - 用户组名称(','号分隔列表)
    ** id - 组id(','号分隔列表)
    """
    msg_prefix = u"删除用户组 "
    req_dict = post_data_to_dict(request.data)

    name = split(req_dict.pop('name'))
    id = split(req_dict.pop('id'))
    try:
        group_set = ExGroup.objects.filter(id__in=id).filter(name__in=name)
        if not group_set.exists():
            raise Exception(u"没有符合条件的用户组")
        data = list(group_set.values('id', 'name', 'member_type'))
        group_set.delete()
    except Exception, e:
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 1, "msg": msg, "data": data})
