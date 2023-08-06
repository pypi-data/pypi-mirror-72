# -*- coding: utf-8 -*-
from .base import BaseAppException

class ParseException(BaseAppException):

    category = 'parse'

    co_msg_mapping = {
        100003: {
            'message': 'ParseException',
            'http_code': 400,
            'sub_category': 'parse',
        },
    }