# coding: utf-8
# Author: Dunkle Qiu

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.views import Token, ObtainAuthToken

from ouser.permissions import *
from opsap.utils.decorators import post_validated_fields, status, post_data_to_dict
from opsap.utils.base import logger
from opsap.settings import TOKEN_TMOUT

from opsap.models import DataDict


class ObtainExAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not created and TOKEN_TMOUT > 0:
            token_life = timezone.now() - token.created
            if token_life.total_seconds() > TOKEN_TMOUT:
                token.delete()
                token = Token.objects.create(user=user)
        return Response({'token': token.key, 'role': user.role})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
@post_validated_fields(require=['app', 'name', 'value'])
def param_set(request):
    """
    设置系统动态参数

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 参数名称
    ** value - 选项值
    ** display - 选项显示名称
    ** 其他 - 其他附加属性
    """
    msg_prefix = u"设置参数 <%s>:<%s> "
    req_dict = post_data_to_dict(request.data)

    app = req_dict.pop('app')
    name = req_dict.pop('name')
    value = req_dict.pop('value')
    display = req_dict.pop('display', '')
    try:
        created = DataDict.params.set_param(app, name, value, display, **req_dict)
        data = DataDict.params.get_param_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % (name, value)) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % (name, value)) + (created and u"新增" or u"修改") + u" 成功!"
        return Response({"status": int(created), "msg": msg, "data": data})


@api_view(['POST'])
@post_validated_fields(require=['app', 'name'])
def param_get(request):
    """
    设置系统动态参数

    * 权限 - 任何人
    * 参数
    ** app - 模块名称
    ** name - 参数名称
    ** default_value - 选项值(可选, 管理员)
    ** default_display - 选项显示名称(可选, 管理员)
    ** 其他 - 其他附加属性(可选, 管理员)
    """
    msg_prefix = u"获取参数 <%s> "
    req_dict = post_data_to_dict(request.data)

    app = req_dict.pop('app')
    name = req_dict.pop('name')
    default_value = req_dict.pop('default_value', '')
    default_display = req_dict.pop('default_display', '')
    if default_value and request.user.role != 'SU':
        raise PermissionDenied()
    try:
        DataDict.params.get_param(app, name, default_value, default_display, **req_dict)
        data = DataDict.params.get_param_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % name) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % name) + u" 成功!"
        return Response({"status": 0, "msg": msg, "data": data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
@post_validated_fields(require=['app', 'name', 'value'], illegal=['options'])
def option_add(request):
    """
    添加动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** value - 选项值
    ** display - 选项显示名称
    ** 其他 - 其他附加属性
    """
    msg_prefix = u"添加表单选项 <%s>:<%s> "
    req_dict = post_data_to_dict(request.data)

    app = req_dict.pop('app')
    name = req_dict.pop('name')
    value = req_dict.pop('value')
    display = req_dict.pop('display', '')
    try:
        created = DataDict.options.add_option(app, name, value, display, **req_dict)
        data = DataDict.options.get_options_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % (name, value)) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % (name, value)) + (created and u"成功!" or u"失败, 该选项已存在!")
        return Response({"status": int(created), "msg": msg, "data": data})


@api_view(['POST'])
@post_validated_fields(require=['app', 'name'], illegal=['options', 'value', 'display'])
def option_list(request):
    """
    获取动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** 其他 - 其他附加属性
    """
    msg_prefix = u"获取表单选项 <%s> "
    req_dict = post_data_to_dict(request.data)

    app = req_dict.pop('app')
    name = req_dict.pop('name')
    try:
        data = DataDict.options.get_options_serialized(app, name, **req_dict)
    except Exception, e:
        msg = (msg_prefix % name) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % name) + u"成功!"
        return Response({"status": 0, "msg": msg, "data": data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
@post_validated_fields(require=['app', 'name', 'value'], illegal=['options'])
def option_edit(request):
    """
    修改动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** value - 选项值
    ** display - 选项显示名称
    ** 其他 - 其他附加属性
    """
    msg_prefix = u"修改表单选项 <%s>:<%s> "
    req_dict = post_data_to_dict(request.data)

    app = req_dict.pop('app')
    name = req_dict.pop('name')
    value = req_dict.pop('value')
    display = req_dict.pop('display', '')
    try:
        updated = DataDict.options.update_option(app, name, value, display, **req_dict)
        data = DataDict.options.get_options_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % (name, value)) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % (name, value)) + (updated and u"成功!" or u"失败, 没有匹配的条目!")
        return Response({"status": int(updated), "msg": msg, "data": data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
@post_validated_fields(require=['app', 'name', 'value'])
def option_delete(request):
    """
    删除动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** value - 选项值(','号分隔列表)
    """
    msg_prefix = u"删除表单选项 <%s>:<%s> "
    req_dict = post_data_to_dict(request.data)

    app = req_dict.pop('app')
    name = req_dict.pop('name')
    value = req_dict.pop('value').split(',')
    try:
        deleted = DataDict.options.delete_options(app, name, *value)
        data = DataDict.options.get_options_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % (name, ','.join(value))) + u"失败, 错误信息: " + unicode(e)
        logger.error(msg)
        return Response({"status": -1, "msg": msg, "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        msg = (msg_prefix % (name, ','.join(value))) + (deleted and u"成功!" or u"失败, 没有匹配的条目!")
        return Response({"status": deleted, "msg": msg, "data": data})
