# coding: utf-8
# Author: Dunkle Qiu

from ovm.models import *
from ovm.api.vmomi import vim, get_moid
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

_typeMap = {
    vim.ComputeResource: ComputeResource,
    vim.ResourcePool: ResourcePool,
    vim.Network: Network,
    vim.Datastore: Datastore,
    vim.HostSystem: HostSystem,
    vim.VirtualMachine: VirtualMachine
}


def _raw_type(vimobj):
    for vt in _typeMap.keys():
        if isinstance(vimobj, vt):
            return vt
    raise TypeError("vim types expected: vimobj")


def _map_vimtype(vmtype):
    for k, v in _typeMap.items():
        if v == vmtype:
            return k


def _map_vmtype(vimtype):
    return _typeMap[vimtype]


class VMObjectTranslator(object):
    """
    VMOMI对象与ovm模块对象的转换类
    """

    def _vim_update(self, related):
        obj = self.obj
        vimobj = self.vimobj
        if not (obj and vimobj):
            raise Exception(u"获取虚拟环境对象失败")
        obj.name = vimobj.name.strip()
        return obj, vimobj

    def _get_vimobj(self):
        if self.vimobj:
            return self.vimobj
        content = self.vc.connect()
        moid = self.obj.moid
        obj_view = content.viewManager.CreateContainerView(content.rootFolder, [_map_vimtype(type(self.obj))], True)
        for o in obj_view.view:
            if get_moid(o) == moid:
                self.vimobj = o
                break
        obj_view.Destroy()
        return self.vimobj

    def __init__(self, from_vim=True, force_update=False, **kwargs):
        # 初始化对象
        self.uuid = ''
        self.vimobj = None
        self.vc = None
        self.obj = None
        self.created = False
        related = kwargs.get('related', False)
        # 从VMOMI对象初始化
        if from_vim:
            self.uuid = kwargs.get('uuid')
            self.vimobj = kwargs.get('vimobj')
            try:
                self.vc = VCenter.objects.get(uuid=self.uuid)
                self.obj, self.created = _map_vmtype(_raw_type(self.vimobj)).objects.match_obj(self.vc, self.vimobj)
            except:
                pass
            else:
                if self.created or force_update:
                    self._vim_update(related)
        else:
            self.vc = kwargs.get('vc')
            self.obj = kwargs.get('obj')
            assert isinstance(self.vc, VCenter)
            assert isinstance(self.obj, VMObject)
            self.uuid = self.vc.uuid
            self._get_vimobj()
            if self.vimobj and force_update:
                self._vim_update(related)

    def update(self, related):
        return self._vim_update(related)


class ComputeResourceTranslator(VMObjectTranslator):
    def _vim_update(self, related):
        obj, vimobj = super(self, ComputeResourceTranslator)._vim_update(related)
        obj.is_cluster = isinstance(vimobj, vim.ClusterComputeResource)
        if obj.is_cluster:
            config = vimobj.configuration
            obj.ha = config.dasConfig.enabled
            obj.drs = config.drsConfig.enabled
        obj.save()
        return obj, vimobj


class ResourcePoolTranslator(VMObjectTranslator):
    def _vim_update(self, related):
        obj, vimobj = super(self, ResourcePoolTranslator)._vim_update(related)
        config = vimobj.config
        config_cpu = config.cpuAllocation
        obj.share_cpu_level, obj.limit_cpu_mhz = config_cpu.shares.level, config_cpu.limit
        config_memory = config.memoryAllocation
        obj.share_mem_level, obj.limit_mem_mb = config_memory.shares.level, config_memory.limit
        if related:
            # update owner
            clus = vimobj.owner
            if isinstance(clus, vmomi.vim.ComputeResource):
                owner = ComputeResourceTranslator(vimobj=clus, uuid=self.uuid, related=related)
                obj.owner = owner.obj
            # update parent
            resp = vimobj.parent
            if isinstance(resp, vmomi.vim.ResourcePool):
                parent = ResourcePoolTranslator(vimobj=resp, uuid=self.uuid, related=related)
                obj.parent = parent.obj
        if self.created:
            obj.set_ext()
        obj.save()
        return obj, vimobj


class NetworkTranslator(VMObjectTranslator):
    def _vim_update(self, related):
        obj, vimobj = super(self, NetworkTranslator)._vim_update(related)
        obj.net = obj.name.split('-')[-1]
        obj.netmask = 24
        obj.save()
        return obj, vimobj


class DatastoreTranslator(VMObjectTranslator):
    def _vim_update(self, related):
        obj, vimobj = super(self, DatastoreTranslator)._vim_update(related)
        summary = vimobj.summary
        obj.accessible = summary.accessible
        obj.multi_hosts_access = summary.multipleHostAccess
        obj.maintenance_mode = summary.maintenanceMode
        if summary.accessible:
            obj.url = summary.url
            obj.total_space_mb = summary.capacity / 1024 ** 2
            obj.free_space_mb = summary.freeSpace / 1024 ** 2
        obj.save()
        return obj, vimobj


class HostSystemTranslator(VMObjectTranslator):
    def _vim_update(self, related):
        obj, vimobj = super(self, HostSystemTranslator)._vim_update(related)
        summary = vimobj.summary
        summary_hardware = summary.hardware
        summary_stat = summary.quickStats
        runtime = vimobj.runtime
        obj.vmotion_enable = summary.config.vmotionEnabled
        obj.total_cpu_cores = summary_hardware.numCpuCores
        obj.total_cpu_mhz = summary_hardware.cpuMhz
        obj.total_mem_mb = summary_hardware.memorySize / 1024 ** 2
        obj.usage_cpu_mhz = summary_stat.overallCpuUsage
        obj.usage_mem_mb = summary_stat.overallMemoryUsage
        obj.connection_state = runtime.connectionState
        obj.in_maintenance_mode = runtime.inMaintenanceMode
        if related:
            # update cluster
            clus = vimobj.parent
            if isinstance(clus, vim.ComputeResource):
                cluster = ComputeResourceTranslator(vimobj=clus, uuid=self.uuid, related=related)
                obj.cluster = cluster.obj

            # ManyToMany relationships
            # update networks
            obj.networks.clear()
            for net in vimobj.network:
                network = NetworkTranslator(vimobj=net, uuid=self.uuid, related=related)
                obj.networks.add(network.obj)
            # update datastores
            obj.datastores.clear()
            for ds in vimobj.datastore:
                datastore = DatastoreTranslator(vimobj=ds, uuid=self.uuid, related=related)
                obj.datastores.add(datastore.obj)
        obj.save()
        return obj, vimobj


class VirtualMachineTranslator(VMObjectTranslator):
    def update_ipusage(self):
        vm_guest = self.vimobj.guest
        old_ipusage_set = list(self.obj.ipusage_set.all())
        ip_list = []
        for net in vm_guest.net:
            for address in net.ipAddress:
                if str(address).count('.') == 3:
                    ip_list.append(address)
        for ip in ip_list:
            ipusage_set = IPUsage.objects.filter(ipaddress=ip)
            if ipusage_set.count() != 1:
                continue
            ipusage = ipusage_set[0]
            if ipusage in old_ipusage_set:
                old_ipusage_set.remove(ipusage)
            else:
                ip.used_occupy = False
                ip.vm = self.obj
                ip.save(update_fields=['used_occupy', 'vm'])
        for ipusage in old_ipusage_set:
            ipusage.vm = None
            if ping(ipusage.ipaddress, wait=1, count=1):
                ipusage.used_unknown = True
            ipusage.save(update_fields=['vm', 'used_unknown'])

    def _vim_update(self, related):
        obj, vimobj = super(self, VirtualMachineTranslator)._vim_update(related)
        config = vimobj.config
        summary = vimobj.summary
        config_hardware = config.hardware
        summary_config = summary.config
        obj.istemplate = config.template
        obj.annotation = config.annotation
        obj.cpu_num = config_hardware.numCPU
        obj.cpu_cores = config_hardware.numCoresPerSocket
        obj.memory_mb = config_hardware.memoryMB
        obj.storage_mb = summary.storage.committed / 1024 ** 2
        obj.guestos_shortname = summary_config.guestId
        obj.guestos_fullname = summary_config.guestFullName
        if related:
            # update hostsystem
            host = vimobj.runtime.host
            if isinstance(host, vim.HostSystem):
                hostsystem = HostSystemTranslator(vimobj=host, uuid=self.uuid, related=related)
                obj.hostsystem = hostsystem.obj
            # update resourcepool
            resp = vimobj.resourcePool
            if isinstance(resp, vim.ResourcePool):
                resourcepool = ResourcePoolTranslator(vimobj=resp, uuid=self.uuid, related=related)
                obj.resourcepool = resourcepool.obj

            # ManyToMany relationships
            # update networks
            obj.networks.clear()
            for o in vimobj.network:
                network = NetworkTranslator(vimobj=o, uuid=self.uuid, related=related)
                obj.networks.add(network.obj)
            # update datastores
            obj.datastores.clear()
            for o in vimobj.datastore:
                datastore = DatastoreTranslator(vimobj=o, uuid=self.uuid, related=related)
                obj.datastores.add(datastore.obj)

            # Reverse foreign key
            # update ipusage_set
            self.update_ipusage()
        obj.save()
        return obj, vimobj
