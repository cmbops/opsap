# coding: utf-8
# Author: Dunkle Qiu

from ovm.models import IPUsage, VirtualMachine, Template
from ovm.api.base import env_type_values


def set_template(vm, env_type):
    assert isinstance(env_type, list)
    env_type_dict = {k: (k in env_type) for k in env_type_values}
    extensions = {'env_type': env_type_dict, 'os_version': vm.guestos_shortname}
    Template.objects.create(virtualmachine=vm, extensions=extensions)
