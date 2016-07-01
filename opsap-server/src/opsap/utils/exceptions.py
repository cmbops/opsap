# coding: utf-8
# Author: Dunkle Qiu

from rest_framework.exceptions import APIException, status


class FieldIsNullError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, *detail):
        self.detail = u"以下参数不能为空 - " + unicode(', '.join(detail))

    def __str__(self):
        return self.detail


class FieldIsAllNullError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, *detail):
        self.detail = u"以下参数至少提供一项 - " + unicode(', '.join(detail))

    def __str__(self):
        return self.detail


class FieldIsIllegalError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, *detail):
        self.detail = u"存在非法参数 - " + unicode(', '.join(detail))

    def __str__(self):
        return self.detail
