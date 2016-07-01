# coding: utf-8
# Author: Dunkle Qiu

from .base import post_data_to_dict
from .exceptions import *


def post_validated_fields(require=None, illegal=None, require_one=None):
    """
    验证request.data中 必填项/无效项 的装饰器
    """
    def _deco(func):
        def __deco(request, *args, **kwargs):
            if request.method == 'POST':
                post_dict = post_data_to_dict(request.data)
                # 必填参数
                if isinstance(require, list):
                    null_fields = []
                    for val in require:
                        if not (post_dict.has_key(val) and post_dict[val]):
                            null_fields.append(val)
                    if null_fields:
                        raise FieldIsNullError(*null_fields)
                # 非法参数
                if isinstance(illegal, list):
                    illegal_fields = []
                    for val in illegal:
                        if post_dict.has_key(val):
                            illegal_fields.append(val)
                    if illegal_fields:
                        raise FieldIsIllegalError(*illegal_fields)
                # 至少提供一项
                if isinstance(require_one, list):
                    all_null = True
                    for val in require_one:
                        if post_dict.has_key(val) and post_dict[val]:
                            all_null = False
                            break
                    if all_null:
                        raise FieldIsAllNullError(*require_one)
            return func(request, *args, **kwargs)

        # 装饰函数docstring
        doc_postfix = ''
        if require:
            doc_postfix += '\n 以下参数必填: ' + ','.join(require)
        if illegal:
            doc_postfix += '\n 以下参数非法: ' + ','.join(illegal)
        if require_one:
            doc_postfix += '\n 以下参数需提供其中之一: ' + ','.join(require_one)
        __deco.func_name = func.func_name
        __deco.func_doc = func.func_doc + doc_postfix
        return __deco

    return _deco
