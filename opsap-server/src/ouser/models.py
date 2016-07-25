# coding: utf-8
# Author: Dunkle Qiu

from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from opsap.utils.base import ROLES
from ouser.managers import *


class ExGroup(Group):
    """
    自定义扩展组模型
    """
    MEM_TYPE_CHOICES = (
        ('staff', 'Staff'),
        ('service', 'Service'),
    )
    comment = models.CharField(max_length=160, blank=True, null=True)
    member_type = models.CharField(max_length=10, choices=MEM_TYPE_CHOICES, default='staff')
    managers = models.ManyToManyField('ExUser', related_name="mana_group_set", related_query_name="mana_group")


class ExUser(AbstractUser):
    """
    自定义用户模型
    """
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=2, choices=ROLES.as_choice(), default='CU')
    ssh_key_str = models.TextField(null=True)
    ssh_key_pwd = models.CharField(max_length=200, null=True)

    objects = ExUserManager()

    def __unicode__(self):
        return self.username
