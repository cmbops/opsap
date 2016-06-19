# coding: utf-8

import json
import copy

from django.db import models


class OptionManager(models.Manager):
    def get_queryset(self):
        return super(OptionManager, self).get_queryset().filter(setting_type='option')

    def get_options(self, app, name, **ext_attr):
        """
        根据应用名、表单名获取动态表单选项
        """
        opt_set = self.filter(app=app, name=name)
        for k, v in ext_attr.items():
            f_query = "\"%s\": \"%s\"" % (k, str(v))
            opt_set = opt_set.filter(ext_attr__icontains=f_query)
        return opt_set

    def get_options_serialized(self, app, name, **ext_attr):
        options = []
        for opt in self.get_options(app, name, **ext_attr):
            opt_ext_attr = json.loads(opt.ext_attr)
            opt_ext_attr.update({ 'value': opt.value,'display': opt.display})
            options.append(opt_ext_attr)
        data = copy.deepcopy(ext_attr)
        data.update({'app': app, 'name': name, 'options': options})
        return data

    def add_option(self, app, name, value, display='', **ext_attr):
        """
        在指定的表单下，添加选项。
        """
        opt_set = self.get_options(app, name).filter(value=value)
        if opt_set.exists():
            return False
        self.create(setting_type='option', app=app, name=name, value=value, display=display,
                    ext_attr=json.dumps(ext_attr))
        return True

    def update_option(self, app, name, value, display='', **ext_attr):
        """
        修改指定的表单选项
        注：value不可修改，只支持增删
        """
        try:
            option = self.get_options(app, name).get(value=value)
            if display:
                option.display = display
            if ext_attr:
                opt_ext_attr = json.loads(option.ext_attr)
                opt_ext_attr.update(ext_attr)
                option.ext_attr = json.dumps(opt_ext_attr)
            option.save()
            return True
        except:
            return False

    def delete_options(self, app, name, *values):
        """
        删除指定的动态表单选项
        """
        opt_set = self.get_options(app, name).filter(value__in=values)
        count = opt_set.count()
        try:
            opt_set.delete()
            return count
        except:
            return 0


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

    objects = models.Manager()
    options = OptionManager()

    class Meta:
        unique_together = ('app', 'setting_type', 'name', 'value')

    def __unicode__(self):
        return "%s_%s_%s" % (self.app, self.setting_type, self.name)
