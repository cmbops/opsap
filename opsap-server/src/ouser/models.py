# coding: utf-8
# Author: Dunkle Qiu

from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db import models
from django.utils import timezone

from opsap.utils.base import ROLES


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


class ExUserManager(UserManager):
    """
    自定义用户管理器
    """
    use_in_migrations = True

    def _create_exuser(self, username, email, password, name, role, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, role=role,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, name='', role='CU', **extra_fields):
        if not name:
            name = username
        return self._create_exuser(username, email, password, name, role, False, False,
                                   **extra_fields)

    def create_superuser(self, username, email, password, name='', **extra_fields):
        if not name:
            name = username
        return self._create_exuser(username, email, password, name, 'SU', True, True,
                                   **extra_fields)


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
