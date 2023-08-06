#coding:utf8
from .base import BaseHTTPException

class FrontendException(BaseHTTPException):

    category = 'frontend'

    co_msg_mapping = {
        200150: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'user.profile.updating'
        },
    }