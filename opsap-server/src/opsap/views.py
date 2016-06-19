# coding: utf-8
# Author: Dunkle Qiu

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .api import *


@api_view(['POST'])
@permission_classes((require_role('SU'),))
def option_add(request):
    """
    添加动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** opt_value - 选项值
    ** opt_display - 选项显示名称
    ** 其他 - 其他附加属性
    """
    req_param_invalid_keys = ['options']
    req_dict = request.POST.dict()
    for key in req_param_invalid_keys:
        req_dict.pop(key, None)
    app = req_dict.pop('app', '')
    name = req_dict.pop('name', '')
    value = req_dict.pop('opt_value', '')
    display = req_dict.pop('opt_display', '')
    msg_prefix = u"添加表单选项 <%s>:<%s> "
    try:
        if not (app and name and value):
            raise ServerError(u'app 或 name 或 opt_value 不能为空')
        created = ParaOption.options.add_option(app, name, value, display, **req_dict)
        data = ParaOption.options.get_options_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % (name, value)) + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = (msg_prefix % (name, value)) + (created and u"成功!" or u"失败, 该选项已存在!")
        return Response({"status": int(created), "msg": msg, "data": data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
def option_list(request):
    """
    获取动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** 其他 - 其他附加属性
    """
    req_param_invalid_keys = ['options', 'opt_value', 'opt_display']
    req_dict = request.POST.dict()
    for key in req_param_invalid_keys:
        req_dict.pop(key, None)
    app = req_dict.pop('app', '')
    name = req_dict.pop('name', '')
    msg_prefix = u"获取表单选项 <%s> "
    try:
        if not (app and name):
            raise ServerError(u'app 或 name 不能为空')
        data = ParaOption.options.get_options_serialized(app, name, **req_dict)
    except Exception, e:
        msg = (msg_prefix % name) + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = (msg_prefix % name) + u"成功!"
        return Response({"status": 0, "msg": msg, "data": data})

@api_view(['POST'])
@permission_classes((require_role('SU'),))
def option_edit(request):
    """
    修改动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** opt_value - 选项值
    ** opt_display - 选项显示名称
    ** 其他 - 其他附加属性
    """
    req_param_invalid_keys = ['options']
    req_dict = request.POST.dict()
    for key in req_param_invalid_keys:
        req_dict.pop(key, None)
    app = req_dict.pop('app', '')
    name = req_dict.pop('name', '')
    value = req_dict.pop('opt_value', '')
    display = req_dict.pop('opt_display', '')
    msg_prefix = u"修改表单选项 <%s>:<%s> "
    try:
        if not (app and name and value):
            raise ServerError(u'app 或 name 或 opt_value 不能为空')
        updated = ParaOption.options.update_option(app, name, value, display, **req_dict)
        data = ParaOption.options.get_options_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % (name, value)) + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = (msg_prefix % (name, value)) + (updated and u"成功!" or u"失败, 没有匹配的条目!")
        return Response({"status": int(updated), "msg": msg, "data": data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
def option_delete(request):
    """
    删除动态表单选项

    * 权限 - 超级管理员(SU)
    * 参数
    ** app - 模块名称
    ** name - 表单名称
    ** opt_value - 选项值(列表)
    """
    app = request.POST.get('app', '')
    name = request.POST.get('name', '')
    value = request.POST.getlist('opt_value', [])
    msg_prefix = u"删除表单选项 <%s>:<%s> "
    try:
        if not (app and name and value):
            raise ServerError(u'app 或 name 或 opt_value 不能为空')
        deleted = ParaOption.options.delete_options(app, name, *value)
        data = ParaOption.options.get_options_serialized(app, name)
    except Exception, e:
        msg = (msg_prefix % (name, ','.join(value))) + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = (msg_prefix % (name, ','.join(value))) + (deleted and u"成功!" or u"失败, 没有匹配的条目!")
        return Response({"status": deleted, "msg": msg, "data": data})
