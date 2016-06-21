# coding: utf-8
# Author: Dunkle Qiu

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from opsap.api import require_role, ServerError, permissions
from ouser.user_api import *
from .serializers import ExUserSerializer, ExGroupSerializer


@api_view(['POST'])
@permission_classes((require_role('SU'),))
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
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    name = request.POST.get('name', '')
    role = request.POST.get('role', 'CU')
    msg_prefix = u"添加用户 %s "
    try:
        if not (username and password and email):
            raise ServerError(u'用户名/密码/邮箱 不能为空')
        if ExUser.objects.filter(username=username):
            raise ServerError(u'用户名已存在')
        user = ExUser.objects.create_user(username, email, password, name, role)
        serializer = ExUserSerializer(user)
    except Exception, e:
        msg = (msg_prefix % username) + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
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
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 0, "msg": msg, "data": serializer.data})


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def user_detail(request):
    """
    获取用户详情

    * 权限 - 超级管理员(SU)
    * 参数
    ** username/id - 用户名称/用户id
    """
    user = request.user
    msg_prefix = u"获取用户详情 "
    try:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            id = request.POST.get('id', '')
            if username:
                user = ExUser.objects.get(username=username)
            elif id:
                user = ExUser.objects.get(pk=int(id))
        serializer = ExUserSerializer(user)
    except Exception, e:
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 0, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role('CU'),))
def user_edit(request):
    """
    修改用户信息

    * 权限 - 超级管理员(SU)
    * 参数
    ** username/id - 用户名称/用户id
    ** email - 邮箱地址
    ** password - 密码
    ** name - 显示名称
    ** role - 角色(CU/GM/SN), SU只通过后台创建
    """
    username = request.POST.get('username', '')
    id = request.POST.get('id', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    name = request.POST.get('name', '')
    role = request.POST.get('role', 'CU')
    msg_prefix = u"修改用户信息 %s "
    try:
        if username:
            user = ExUser.objects.get(username=username)
        elif id:
            user = ExUser.objects.get(pk=int(id))
        else:
            raise ServerError(u'用户名/用户id 至少提供一项')

        req_user = request.user
        if req_user.role != 'SU' and req_user != user:
            return Response(status=403)

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
        msg = (msg_prefix % username) + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = (msg_prefix % username) + u"成功!"
        return Response({"status": 1, "msg": msg, "data": serializer.data})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
def user_delete(request):
    """
    删除用户

    * 权限 - 超级管理员(SU)
    * 需同时提供用户名及id列表
    * 参数
    ** username - 用户名称(列表)
    ** id - 用户id(列表)
    """
    username = request.POST.getlist('username', '')
    id = request.POST.getlist('id', '')
    msg_prefix = u"删除用户 "
    delete_list = []
    try:
        for value in id:
            if value==request.user.id:
                continue
            user = ExUser.objects.get(pk=int(value))
            if user.username in username:
                delete_list.append({
                    'id': value,
                    'username': username,
                    'role': user.role
                })
                user.delete()
    except Exception, e:
        msg = msg_prefix + u"失败, 错误信息: " + unicode(e)
        return Response({"status": -1, "msg": msg, "data": {}})
    else:
        msg = msg_prefix + u"成功!"
        return Response({"status": 1, "msg": msg, "data": delete_list})


@api_view(['POST'])
@permission_classes((require_role('SU'),))
def group_add(request):
    """
    添加用户组

    * 权限 - 超级管理员(SU)
    * 参数
    ** name - 用户组名称
    ** comment - 用户组描述
    ** users_selected - 初始用户(id)(列表)
    """
    group_name = request.POST.get('name', '')
    users_selected = request.POST.getlist('users_selected', '')
    comment = request.POST.get('comment', '')
    try:
        if not group_name:
            raise ServerError(u'组名 不能为空')
        if ExGroup.objects.filter(name=group_name):
            raise ServerError(u'组名已存在')
        db_add_group(name=group_name, users_id=users_selected, comment=comment)
    except Exception, e:
        msg = str(e)
        return Response({"status": "error", "msg": msg, "data": {}})
    else:
        msg = u'添加组 %s 成功' % group_name
        return Response({"status": "success", "msg": msg, "data": {}})


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
@permission_classes((require_role('super'),))
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

# @require_role(role='super')
# def group_edit(request):
#     error = ''
#     msg = ''
#     header_title, path1, path2 = '编辑用户组', '用户管理', '编辑用户组'
#
#     if request.method == 'GET':
#         group_id = request.GET.get('id', '')
#         user_group = get_object(UserGroup, id=group_id)
#         # user_group = UserGroup.objects.get(id=group_id)
#         users_selected = User.objects.filter(group=user_group)
#         users_remain = User.objects.filter(~Q(group=user_group))
#         users_all = User.objects.all()
#
#     elif request.method == 'POST':
#         group_id = request.POST.get('group_id', '')
#         group_name = request.POST.get('group_name', '')
#         comment = request.POST.get('comment', '')
#         users_selected = request.POST.getlist('users_selected')
#
#         try:
#             if '' in [group_id, group_name]:
#                 raise ServerError('组名不能为空')
#
#             if len(UserGroup.objects.filter(name=group_name)) > 1:
#                 raise ServerError(u'%s 用户组已存在' % group_name)
#             # add user group
#             user_group = get_object_or_404(UserGroup, id=group_id)
#             user_group.user_set.clear()
#
#             for user in User.objects.filter(id__in=users_selected):
#                 user.group.add(UserGroup.objects.get(id=group_id))
#
#             user_group.name = group_name
#             user_group.comment = comment
#             user_group.save()
#         except ServerError, e:
#             error = e
#
#         if not error:
#             return HttpResponseRedirect(reverse('user_group_list'))
#         else:
#             users_all = User.objects.all()
#             users_selected = User.objects.filter(group=user_group)
#             users_remain = User.objects.filter(~Q(group=user_group))
#
#     return my_render('ouser/group_edit.html', locals(), request)
#

# @require_role(role='admin')
# def user_del(request):
#     if request.method == "GET":
#         user_ids = request.GET.get('id', '')
#         user_id_list = user_ids.split(',')
#     elif request.method == "POST":
#         user_ids = request.POST.get('id', '')
#         user_id_list = user_ids.split(',')
#     else:
#         return HttpResponse('错误请求')
#
#     for user_id in user_id_list:
#         user = get_object(User, id=user_id)
#         if user and user.username != 'admin':
#             logger.debug(u"删除用户 %s " % user.username)
#             bash('userdel -r %s' % user.username)
#             user.delete()
#     return HttpResponse('删除成功')
#
#
# @require_role('admin')
# def send_mail_retry(request):
#     uuid_r = request.GET.get('uuid', '1')
#     user = get_object(User, uuid=uuid_r)
#     msg = u"""
#     跳板机地址： %s
#     用户名：%s
#     重设密码：%s/ouser/password/forget/
#     请登录web点击个人信息页面重新生成ssh密钥
#     """ % (URL, user.username, URL)
#
#     try:
#         pass
#         # send_mail(u'邮件重发', msg, MAIL_FROM, [user.email], fail_silently=False)
#     except IndexError:
#         return None,
#     return HttpResponse('发送成功')
#
#
# @defend_attack
# def forget_password(request):
#     if request.method == 'POST':
#         defend_attack(request)
#         email = request.POST.get('email', '')
#         username = request.POST.get('username', '')
#         name = request.POST.get('name', '')
#         user = get_object(User, username=username, email=email, name=name)
#         if user:
#             timestamp = int(time.time())
#             hash_encode = PyCrypt.md5_crypt(str(user.uuid) + str(timestamp) + KEY)
#             msg = u"""
#             Hi %s, 请点击下面链接重设密码！
#             %s/ouser/password/reset/?uuid=%s&timestamp=%s&hash=%s
#             """ % (user.name, URL, user.uuid, timestamp, hash_encode)
#             # send_mail('忘记跳板机密码', msg, MAIL_FROM, [email], fail_silently=False)
#             msg = u'请登陆邮箱，点击邮件重设密码'
#             return http_success(request, msg)
#         else:
#             error = u'用户不存在或邮件地址错误'
#
#     return render_to_response('ouser/forget_password.html', locals())
#
#
# @defend_attack
# def reset_password(request):
#     uuid_r = request.GET.get('uuid', '')
#     timestamp = request.GET.get('timestamp', '')
#     hash_encode = request.GET.get('hash', '')
#     action = '/ouser/password/reset/?uuid=%s&timestamp=%s&hash=%s' % (uuid_r, timestamp, hash_encode)
#
#     if hash_encode == PyCrypt.md5_crypt(uuid_r + timestamp + KEY):
#         if int(time.time()) - int(timestamp) > 600:
#             return http_error(request, u'链接已超时')
#     else:
#         return HttpResponse('hash校验失败')
#
#     if request.method == 'POST':
#         password = request.POST.get('password')
#         password_confirm = request.POST.get('password_confirm')
#         print password, password_confirm
#         if password != password_confirm:
#             return HttpResponse('密码不匹配')
#         else:
#             user = get_object(User, uuid=uuid_r)
#             if user:
#                 user.password = PyCrypt.md5_crypt(password)
#                 user.save()
#                 return http_success(request, u'密码重设成功')
#             else:
#                 return HttpResponse('用户不存在')
#
#     else:
#         return render_to_response('ouser/reset_password.html', locals())
#
#     return http_error(request, u'错误请求')
#
#
# @require_role(role='super')
# def user_edit(request):
#     header_title, path1, path2 = '编辑用户', '用户管理', '编辑用户'
#     if request.method == 'GET':
#         user_id = request.GET.get('id', '')
#         if not user_id:
#             return HttpResponseRedirect(reverse('index'))
#
#         user_role = {'SU': u'超级管理员', 'CU': u'普通用户'}
#         user = get_object(User, id=user_id)
#         group_all = UserGroup.objects.all()
#         if user:
#             groups_str = ' '.join([str(group.id) for group in user.group.all()])
#             admin_groups_str = ' '.join([str(admin_group.group.id) for admin_group in user.admingroup_set.all()])
#
#     else:
#         user_id = request.GET.get('id', '')
#         password = request.POST.get('password', '')
#         name = request.POST.get('name', '')
#         email = request.POST.get('email', '')
#         groups = request.POST.getlist('groups', [])
#         role_post = request.POST.get('role', 'CU')
#         admin_groups = request.POST.getlist('admin_groups', [])
#         extra = request.POST.getlist('extra', [])
#         is_active = True if '0' in extra else False
#         email_need = True if '2' in extra else False
#         user_role = {'SU': u'超级管理员', 'GA': u'部门管理员', 'CU': u'普通用户'}
#
#         if user_id:
#             user = get_object(User, id=user_id)
#         else:
#             return HttpResponseRedirect(reverse('user_list'))
#
#         if password != '':
#             password_decode = password
#         else:
#             password_decode = None
#
#         db_update_user(user_id=user_id,
#                        password=password,
#                        name=name,
#                        email=email,
#                        groups=groups,
#                        admin_groups=admin_groups,
#                        role=role_post,
#                        is_active=is_active)
#
#         if email_need:
#             msg = u"""
#             Hi %s:
#                 您的信息已修改，请登录跳板机查看详细信息
#                 地址：%s
#                 用户名： %s
#                 密码：%s (如果密码为None代表密码为原密码)
#                 权限：：%s
#
#             """ % (user.name, URL, user.username, password_decode, user_role.get(role_post, u''))
#             # send_mail('您的信息已修改', msg, MAIL_FROM, [email], fail_silently=False)
#
#         return HttpResponseRedirect(reverse('user_list'))
#     return my_render('ouser/user_edit.html', locals(), request)
#
#
# @require_role('user')
# def profile(request):
#     user_id = request.user.id
#     if not user_id:
#         return HttpResponseRedirect(reverse('index'))
#     user = User.objects.get(id=user_id)
#     return my_render('ouser/profile.html', locals(), request)
#
#
# def change_info(request):
#     header_title, path1, path2 = '修改信息', '用户管理', '修改个人信息'
#     user_id = request.user.id
#     user = User.objects.get(id=user_id)
#     error = ''
#     if not user:
#         return HttpResponseRedirect(reverse('index'))
#
#     if request.method == 'POST':
#         name = request.POST.get('name', '')
#         password = request.POST.get('password', '')
#         email = request.POST.get('email', '')
#
#         if '' in [name, email]:
#             error = '不能为空'
#
#         if not error:
#             User.objects.filter(id=user_id).update(name=name, email=email)
#             if len(password) > 0:
#                 user.set_password(password)
#                 user.save()
#             msg = '修改成功'
#
#     return my_render('ouser/change_info.html', locals(), request)
#
#
# @require_role(role='user')
# def regen_ssh_key(request):
#     uuid_r = request.GET.get('uuid', '')
#     user = get_object(User, uuid=uuid_r)
#     if not user:
#         return HttpResponse('没有该用户')
#
#     username = user.username
#     ssh_key_pass = PyCrypt.gen_rand_pass(16)
#     gen_ssh_key(username, ssh_key_pass)
#     return HttpResponse('ssh密钥已生成，密码为 %s, 请到下载页面下载' % ssh_key_pass)
#
#
# @require_role(role='user')
# def down_key(request):
#     if is_role_request(request, 'super'):
#         uuid_r = request.GET.get('uuid', '')
#     else:
#         uuid_r = request.user.uuid
#
#     if uuid_r:
#         user = get_object(User, uuid=uuid_r)
#         if user:
#             username = user.username
#             private_key_file = os.path.join(KEY_DIR, 'user', username+'.pem')
#             print private_key_file
#             if os.path.isfile(private_key_file):
#                 f = open(private_key_file)
#                 data = f.read()
#                 f.close()
#                 response = HttpResponse(data, content_type='application/octet-stream')
#                 response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(private_key_file)
#                 return response
#     return HttpResponse('No Key File. Contact Admin.')
#
