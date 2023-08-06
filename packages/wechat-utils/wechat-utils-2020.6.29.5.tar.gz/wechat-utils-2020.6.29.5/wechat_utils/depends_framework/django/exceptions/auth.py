#coding:utf8
from rest_framework.exceptions import APIException

from rest_framework import status

import json

from django.utils.translation import gettext_lazy as _


class BaseAPIException(APIException):

    # error = {
    # 	100000:{
    #      'status_code':400,
    #      'detail':'unknow error!',
    # 	},
    # }

    def __init__(self, errcode):
        error = self.error[errcode]
        self.default_code = str(errcode)
        self.status_code = error['status_code']
        self.default_detail = error['detail']
        super().__init__(detail=error['detail'], code=str(errcode))

class TestAException(APIException):
    default_detail = _('default_detail')
    default_code = 'default_code'
    status_code = status.HTTP_200_OK
    detail = json.dumps({'detail':1,'code':2})
    code = 1

class AuthException(BaseAPIException):
    error = {
        981001: {
            'detail': 'username existed',
            'status_code': 400,
        },
        981002: {
            'detail': 'role not exists',
            'status_code': 400,
        },
        981051: {
            'detail': 'db error while creating admin',
            'status_code': 500,
        },

        981101: {
            'detail': 'Missing login credentials',
            'status_code': 400,
        },
        981102: {
            'detail': 'Token expired',
            'status_code': 400,
        },
        981103: {
            'detail': 'Token corrupted',
            'status_code': 400,
        },
        981104: {
            'detail': 'Missing uid in deserialized data',
            'status_code': 400,
        },
        981105: {
            'detail': 'Not supported user type',
            'status_code': 400,
        },
        981106: {
            'detail': 'Missing token',
            'status_code': 400,
        },
        981107: {
            'detail': 'Wrong token format',
            'status_code': 400,
        },
        981201: {
            'detail': 'Retrieving session_info from wechat error',
            'status_code': 400,
        },
        981202: {
            'detail': 'No openid found in session_info returned from wechat',
            'status_code': 404,
        },
        981203: {
            'detail': 'Wechat user not found by id',
            'status_code': 404,
        },
        981251: {
            'detail': 'Creating user in db error',
            'status_code': 500,
        },
        981301: {
            'detail': 'Missing username while admin login',
            'status_code': 400,
        },
        981302: {
            'detail': 'Missing password while admin login',
            'status_code': 400,
        },
        981303: {
            'detail': 'Specified admin not exists',
            'status_code': 404,
        },
        981304: {
            'detail': 'Password not matched',
            'status_code': 400,
        },
        981305: {
            'detail': 'admin not found by id',
            'status_code': 404,
        },
        981401: {
            'detail': 'Permission denied',
            'status_code': 403,
        },

        981108: {
            'detail': 'Missing code',
            'status_code': 400,
        },
        981109: {
            'detail': 'Token decrypt fail!',
            'status_code': 400,
        },
    }