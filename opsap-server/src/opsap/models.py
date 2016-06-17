# coding: utf-8

from django.db import models


class ParaOption(models.Model):
    """
    应用参数及动态表单选项
    """
    CH_SETTING_TYPE = (
        ('param', 'parameter'),
        ('option', 'field options')
    )
    app = models.CharField(max_length=20)
    setting_type = models.CharField(max_length=20, choices=CH_SETTING_TYPE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    display = models.CharField(max_length=255, null=True)
    ext_attr = models.CharField(max_length=255, default='{}')

    class Meta:
        unique_together = ('app', 'setting_type', 'name', 'value')

    def __unicode__(self):
        return "%s_%s_%s" % (self.app, self.setting_type, self.name)
