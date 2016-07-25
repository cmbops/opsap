# coding: utf-8
# Author: Dunkle Qiu

from django.utils import timezone
from django.db import models
from ovm.api import base, vmomi
from opsap.utils.base import ping, ip_str2bin, ip_bin2str, OSTYPES


class VCenterManager(models.Manager):
    def discover(self, ip, port=443, env_type=list(), user='root', pwd='vmware'):
        """
        初始化VCenter
        返回tuple(vc, created)
        """
        # 参数检查
        if not isinstance(env_type, list):
            raise TypeError(u"list expect: env_type")

        uuid, version = vmomi.discover_vc(ip, port, user, pwd)
        if not uuid:
            raise Exception(u"连接VC失败, 无法添加VC")
        vc_set = self.filter(uuid=uuid)
        if vc_set.exists():
            return vc_set[0], False
        # 创建VC对象
        env_type_dict = {}
        for val in base.env_type_values:
            env_type_dict[val] = val in env_type
        vc = self.create(ip=ip, port=port, env_type=env_type_dict, user=user, password=pwd, uuid=uuid, version=version,
                         last_connect=timezone.now())
        return vc, True

    def modify(self, id, ip=None, port=None, env_type=None, user=None, pwd=None):
        """
        修改VCenter
        返回True/False
        """
        vc = self.get(id=id)
        if env_type:
            env_type_dict = {}
            for val in base.env_type_values:
                env_type_dict[val] = val in env_type
            vc.env_type = env_type_dict
        re_check = ip or port or user or pwd
        if not re_check:
            vc.save(update_fields=['env_type'])
            return True
        ip = ip or str(vc.ip)
        port = port or vc.port
        user = user or str(vc.user)
        pwd = pwd or str(vc.password)
        uuid, version = vmomi.discover_vc(ip, port, user, pwd)
        if uuid != vc.uuid:
            raise Exception('New instance\'s uuid differs from the old one, vc is left unchanged!')
        vc.ip, vc.port, vc.user, vc.password = ip, port, user, pwd
        vc.save()
        return True


class VMObjectManager(models.Manager):
    def match_obj(self, vc, vimobj):
        moid = vimobj._GetMoId()
        try:
            return self.get(moid=moid, vcenter=vc), False
        except:
            return self.model(moid=moid, vcenter=vc), True

    def match_ext(self, **kwargs):
        result_set = self.all()
        for k, v in kwargs.items():
            k_q = "\"" + k + "\": {"
            v_q = "\"" + v + "\": true"
            q_set = result_set.filter(extensions__icontains=k_q)
            if q_set.exists():
                result_set = q_set.filter(extensions__icontains=v_q)
        return result_set


class IPUsageManager(models.Manager):
    def select_ip(self, network, lock_sec=600, test=True, occupy=False):
        test_list = self.filter(network=network, used_manage=False, used_occupy=False, used_unknown=False,
                                vm__isnull=True).order_by('id')
        for ipusage in test_list:
            ip = ipusage.ipaddress
            if ipusage.lock_until and ipusage.lock_until > timezone.now():
                continue
            if test and ping(ip):
                ipusage.used_unknown = True
                ipusage.save(update_fields=['used_unknown'])
                continue
            if occupy:
                ipusage.occupy()
            else:
                ipusage.lock_until = timezone.now() + timezone.timedelta(seconds=lock_sec)
                ipusage.save(update_fields=['lock_until'])
            return ipusage

    def initial(self, network, gw_addr=None):
        q_set = self.filter(network=network)
        if q_set.exists():
            return q_set, False
        mask = network.netmask
        net_bin = ip_str2bin(network.net)
        if '1' in net_bin[mask:]:
            return None, False
        ip_list_int = range(int(net_bin, 2) + 1, int(net_bin[:mask] + '1' * (32 - mask), 2))
        ip_list_bin = [bin(subn)[2:].rjust(32, str(0)) for subn in ip_list_int]
        if isinstance(gw_addr, str):
            if ip_str2bin(gw_addr) in ip_list_bin:
                ip_list_bin.remove(ip_str2bin(gw_addr))
                gw = self.create(ipaddress=gw_addr, network=network, used_manage=True,
                                 used_manage_app='GW')
            else:
                raise Exception("network doesn't cover the gw address!")
        else:
            gw = self.create(ipaddress=ip_bin2str(ip_list_bin.pop()), network=network, used_manage=True,
                             used_manage_app='GW')
        for ip_bin in ip_list_bin:
            self.create(ipaddress=ip_bin2str(ip_bin), network=network)
        return gw, len(ip_list_int)


class TemplateManager(models.Manager):
    def match_ext(self, **kwargs):
        result_set = self.all()
        for k, v in kwargs.items():
            k_q = "\"" + k + "\": {"
            v_q = "\"" + v + "\": true"
            q_set = result_set.filter(extensions__icontains=k_q)
            if q_set.exists():
                result_set = q_set.filter(extensions__icontains=v_q)
        return result_set


class CustomSpecManager(models.Manager):
    def match_ext(self, **kwargs):
        result_set = self.all()
        for k, v in kwargs.items():
            k_q = "\"" + k + "\": {"
            v_q = "\"" + v + "\": true"
            q_set = result_set.filter(extensions__icontains=k_q)
            if q_set.exists():
                result_set = q_set.filter(extensions__icontains=v_q)
        return result_set.filter(available=True)

    def fetch_all(self, vc):
        spec_li = vmomi.get_all_custspec(vc.connect())
        for spec in spec_li:
            if not self.filter(vcenter=vc, name=spec['name']).exists():
                self.create(vcenter=vc, name=spec['name'], spec_type=spec['spec_type'],
                            extensions={'os_type': {spec['spec_type']: True}})
