# coding: utf-8
# Author: Dunkle Qiu

from opsap.utils.fields import JsonField
from ouser.models import ExUser
from ovm.managers import *

_sis = {}


# Create your models here.
class VCenter(models.Model):
    uuid = models.CharField(max_length=50, unique=True)
    version = models.CharField(max_length=30)
    ip = models.GenericIPAddressField(protocol='ipv4')
    port = models.PositiveIntegerField()
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    last_connect = models.DateTimeField(null=True)
    last_sync = models.DateTimeField(null=True)

    extensions = JsonField(default={})
    objects = VCenterManager()

    def connect(self):
        content = vmomi.connect_vc(self.uuid, self.ip, self.port, self.user, self.password)
        self.last_connect = timezone.now()
        self.save(update_fields=['last_connect'])
        return content


class VMObject(models.Model):
    vcenter = models.ForeignKey('VCenter')
    moid = models.CharField(max_length=30)
    name = models.CharField(max_length=255)

    extensions = JsonField(default={})
    objects = VMObjectManager()

    class Meta:
        abstract = True
        unique_together = ('vcenter', 'moid')

    def __str__(self):
        return self.moid + " : " + self.name


class ComputeResource(VMObject):
    is_cluster = models.BooleanField()
    ha = models.NullBooleanField()
    drs = models.NullBooleanField()

    # def free_cpu(self):
    #     """
    #     :return: cpu_free_percent
    #     """
    #     total_cpu = 0
    #     usage_cpu = 0
    #     qset = self.hostsystem_set.all()
    #     if not qset.exists():
    #         return 0
    #     for host in qset:
    #         total_cpu += host.cpu_total()
    #         usage_cpu += host.usage_cpu_mhz
    #     return 100 - (float(usage_cpu) * 100 / total_cpu)
    #
    # def free_mem(self):
    #     """
    #     :return: memory_free_percent
    #     """
    #     total_mem = 0
    #     usage_mem = 0
    #     qset = self.hostsystem_set.all()
    #     if not qset.exists():
    #         return 0
    #     for host in qset:
    #         total_mem += host.total_mem_mb
    #         usage_mem += host.usage_mem_mb
    #     return 100 - (float(usage_mem) * 100 / total_mem)


class ResourcePool(VMObject):
    share_cpu_level = models.CharField(max_length=30)
    share_mem_level = models.CharField(max_length=30)
    limit_cpu_mhz = models.BigIntegerField()
    limit_mem_mb = models.BigIntegerField()
    # related fields
    owner = models.ForeignKey('ComputeResource', null=True)
    parent = models.ForeignKey('ResourcePool', null=True)

    def set_ext(self, env_type=None):
        ext = self.extensions
        if isinstance(env_type, dict):
            ext['env_type'] = env_type
        elif env_type is None:
            ext['env_type'] = self.vcenter.extensions['env_type']
        else:
            raise TypeError("dict expected: env_type")
        self.extensions = ext


class Network(VMObject):
    net = models.GenericIPAddressField(protocol='ipv4')
    netmask = models.PositiveSmallIntegerField(default=24)

    @property
    def get_netmask(self):
        """
        返回掩码字符串
        """
        mask_bin = (self.netmask * '1').ljust(32, str(0))
        return ip_bin2str(mask_bin)

    def set_ext(self, **kwargs):
        ext = self.extensions
        ext.update(kwargs)
        self.extensions = ext
        self.save(update_fields=['extensions'])

    def modify(self, nw=None, mask=None):
        if nw:
            self.net = nw
        if isinstance(mask, int):
            self.netmask = mask
        self.save()


class IPUsage(models.Model):
    ipaddress = models.GenericIPAddressField(protocol='ipv4')
    network = models.ForeignKey('Network')
    vm = models.ForeignKey('VirtualMachine', null=True, on_delete=models.SET_NULL)
    used_manage = models.BooleanField(default=False)
    used_manage_app = models.CharField(max_length=255, null=True)
    used_occupy = models.BooleanField(default=False)
    used_unknown = models.BooleanField(default=False)
    lock_until = models.DateTimeField(null=True)

    objects = IPUsageManager()

    class Meta:
        unique_together = ('network', 'ipaddress')

    def get_occupy(self):
        self.used_manage = False
        self.used_unknown = False
        self.used_occupy = True
        self.save(update_fields=['used_manage', 'used_unknown', 'used_occupy'])

    def release_occupy(self):
        self.used_occupy = False
        self.save(update_fields=['used_occupy'])

    def manage(self, app):
        self.used_unknown = False
        self.used_occupy = False
        self.used_manage = True
        self.used_manage_app = app
        self.save(update_fields=['used_manage', 'used_manage_app', 'used_unknown', 'used_occupy'])


class Datastore(VMObject):
    MT_NORM = 'normal'
    MT_INMT = 'inMaintenance'
    MT_TOMT = 'enteringMaintenance'
    MT_MODE_CHOICE = (
        (MT_NORM, 'normal'),
        (MT_INMT, 'in maintenance'),
        (MT_TOMT, 'entering maintenance')
    )
    url = models.CharField(max_length=255, null=True)
    accessible = models.BooleanField()
    multi_hosts_access = models.BooleanField()
    maintenance_mode = models.CharField(max_length=10, choices=MT_MODE_CHOICE)
    total_space_mb = models.BigIntegerField(null=True)
    free_space_mb = models.BigIntegerField(null=True)


class HostSystem(VMObject):
    vmotion_enable = models.BooleanField()
    total_cpu_cores = models.PositiveSmallIntegerField()
    total_cpu_mhz = models.PositiveIntegerField()
    total_mem_mb = models.PositiveIntegerField()
    connection_state = models.CharField(max_length=30)
    in_maintenance_mode = models.BooleanField()
    usage_cpu_mhz = models.PositiveIntegerField()
    usage_mem_mb = models.PositiveIntegerField()
    # related fields
    cluster = models.ForeignKey('ComputeResource', null=True)
    networks = models.ManyToManyField('Network')
    datastores = models.ManyToManyField('Datastore')

    def cpu_total(self):
        return self.total_cpu_mhz * self.total_cpu_cores

    def free_mem_mb(self):
        return self.total_mem_mb - self.usage_mem_mb

    def free_mem_percent(self):
        return self.free_mem_mb() / self.total_mem_mb


class VirtualMachine(VMObject):
    istemplate = models.BooleanField()
    annotation = models.TextField()
    cpu_num = models.PositiveSmallIntegerField()
    cpu_cores = models.PositiveSmallIntegerField()
    memory_mb = models.PositiveIntegerField()
    storage_mb = models.PositiveIntegerField()
    guestos_shortname = models.CharField(max_length=30)
    guestos_fullname = models.CharField(max_length=255)
    hostsystem = models.ForeignKey('HostSystem', null=True)
    resourcepool = models.ForeignKey('ResourcePool', null=True)
    networks = models.ManyToManyField('Network')
    datastores = models.ManyToManyField('Datastore')


class Template(models.Model):
    virtualmachine = models.OneToOneField(VirtualMachine)
    extensions = JsonField(default={})

    objects = TemplateManager()


class CustomSpec(models.Model):
    vcenter = models.ForeignKey('VCenter')
    name = models.CharField(max_length=80)
    available = models.BooleanField(default=False)
    spec_type = models.CharField(max_length=10, choices=OSTYPES.as_choice())
    extensions = JsonField(default={})

    objects = CustomSpecManager()

    def set_ext(self, **kwargs):
        ext = self.extensions
        ext.update(kwargs)
        self.extensions = ext
        self.save(update_fields=['extensions'])


class Software(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=255, null=True)
    init_params = JsonField(default={})
    extensions = JsonField(default=[])


class Approval(models.Model):
    """审核表"""
    APPROVAL_STATUS = (
        ('NEW', 'Not submitted.'),
        ('SUB', 'Submitted.'),
        ('APR', 'Approved, untreated.'),
        ('GEN', 'Handling VM orders.'),
        ('COM', 'Completed the handling.'),
        ('ERR', 'Errors occurred.'),
    )
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=3, choices=APPROVAL_STATUS, default='NEW')
    env_type = models.CharField(max_length=20)

    applicant = models.ForeignKey(ExUser)
    apply_msg = models.TextField()
    apply_date = models.DateTimeField()

    approver = models.ForeignKey(ExUser, related_name="handled_approval_set", related_query_name="handled_approval")
    appro_msg = models.TextField()
    appro_date = models.DateTimeField()


class VMOrder(models.Model):
    """生成表"""
    ORDER_STATUS = (
        ('NPR', 'Not related to any workflow'),
        ('NST', 'Still in approving, not ready'),
        ('GEN', 'Handling VM order.'),
        ('COM', 'Completed the handling.'),
        ('ERR', 'Errors occurred.'),
    )
    approval = models.ForeignKey('Approval', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=3, choices=ORDER_STATUS, default='NPR')

    apply_softwares = JsonField(default=[])
    apply_cpu = models.SmallIntegerField()
    apply_memory_gb = models.IntegerField()
    apply_os_version = models.CharField(max_length=50)
    apply_datadisk_gb = models.IntegerField()

    appro_softwares = models.ManyToManyField('Software')
    appro_cpu = models.SmallIntegerField()
    appro_memory_gb = models.IntegerField()
    appro_template = models.ForeignKey('Template', null=True, on_delete=models.SET_NULL)
    appro_datadisk_gb = models.IntegerField()

    loc_hostname = models.CharField(max_length=20, null=True)
    loc_ip = models.ForeignKey('IPUsage', null=True, on_delete=models.SET_NULL)
    loc_cluster = models.ForeignKey('ComputeResource', null=True, on_delete=models.SET_NULL)
    loc_resp = models.ForeignKey('ResourcePool', null=True, on_delete=models.SET_NULL)
    loc_storage = models.ForeignKey('Datastore', null=True, on_delete=models.SET_NULL)

    gen_log = models.TextField(null=True)
    gen_time = models.DateTimeField(null=True)
    gen_progress = models.PositiveIntegerField(default=0)

    def add_log(self, log):
        new_log = str(log) + '\n'
        if self.gen_log:
            self.gen_log = str(self.gen_log) + new_log
        else:
            self.gen_log = new_log
        self.save(update_fields=['gen_log'])
        return str(self.gen_log)
