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


@JsonField.register_lookup
class DictMapLookup(models.Lookup):
    lookup_name = 'map'

    def as_sql(self, compiler, connection):
        logger.debug(compiler)
        logger.debug(connection)
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        key, value = rhs_params[0][1:-1].split('%')
        params = ["%\"{0}\": \"{1}\"%".format(key, value)]
        return "%s LIKE %%s" % lhs, params
