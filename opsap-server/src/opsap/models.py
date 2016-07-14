# coding: utf-8
# Author: Dunkle Qiu

from opsap.managers import *
from opsap.utils.fields import JsonField


class DataDict(models.Model):
    """
    应用参数及动态表单选项
    """
    CH_SETTING_TYPE = (
        ('PARAM', 'parameter'),
        ('OPTION', 'field options')
    )
    app = models.CharField(max_length=20)
    setting_type = models.CharField(max_length=20, choices=CH_SETTING_TYPE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    display = models.CharField(max_length=255, null=True)
    ext_attr = JsonField(default={})

    objects = models.Manager()
    params = ParamManager()
    options = OptionManager()

    class Meta:
        unique_together = ('app', 'setting_type', 'name', 'value')

    def __unicode__(self):
        return "_%s_%s_%s" % (self.app, self.setting_type, self.name)
