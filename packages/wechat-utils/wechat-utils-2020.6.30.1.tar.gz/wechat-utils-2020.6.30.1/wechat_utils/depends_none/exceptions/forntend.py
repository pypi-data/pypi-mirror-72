# -*- coding: utf-8 -*-
from .base import BaseAppException

class FrontendException(BaseAppException):

    category = 'frontend'

    co_msg_mapping = {
        200150: {
            'message': 'Unexpected exception',
            'http_code': 500,
            'sub_category': 'user.profile.updating'
        },
    }