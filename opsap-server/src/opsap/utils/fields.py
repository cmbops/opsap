# coding: utf-8
# Author: Dunkle Qiu

from django.utils.translation import ugettext_lazy as _
from django.db import models
import json
from .base import logger


class JsonField(models.TextField):
    description = _("Json")

    def from_db_value(self, value, expression, connection, context):
        return json.loads(value)

    def get_prep_value(self, value):
        value = json.dumps(value)
        return super(JsonField, self).get_prep_value(value)
