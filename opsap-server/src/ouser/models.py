# coding: utf-8

from django.contrib.auth.models import AbstractUser, Group
from django.db import models


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
    managers = models.ManyToManyField('User', related_name="mana_group_set", related_query_name="mana_group")


class User(AbstractUser):
    """
    自定义用户模型
    """
    USER_ROLE_CHOICES = (
        ('SU', 'SuperUser'),
        ('GM', 'GroupManager'),
        ('CU', 'CommonUser'),
        ('SN', 'ServiceNode')
    )
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=2, choices=USER_ROLE_CHOICES, default='CU')
    ssh_key_str = models.TextField(null=True)
    ssh_key_pwd = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.username
