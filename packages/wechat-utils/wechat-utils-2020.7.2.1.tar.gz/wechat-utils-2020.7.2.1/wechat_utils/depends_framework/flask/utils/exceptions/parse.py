# -*- coding: utf-8 -*-
from .base import BaseHTTPException

class ParseException(BaseHTTPException):

    category = 'parse'

    co_msg_mapping = {
        100003: {
            'message': 'ParseException',
            'http_code': 400,
            'sub_category': 'parse',
        },
    }