# coding: utf-8
# Author: Dunkle Qiu

from django.contrib.auth.models import UserManager
from django.utils import timezone


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
