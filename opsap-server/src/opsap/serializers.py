# coding: utf-8

import json

from rest_framework import serializers

from .api import get_options
from .models import ParaOption


class ParaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParaOption
        fields = ('app', 'name', 'value', 'display', 'ext_attr')
