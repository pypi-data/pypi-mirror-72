# -*- coding: utf-8 -*-

from .base import BaseHTTPException


class AuthException(BaseHTTPException):
    # category
    # auth: 98
    category = 'web-auth'

    # sub category:
    #   - admin.creation 10
    #   - login 11
    #   - login.wechat 12
    #   - login.admin 13
    #   - authorization 14
    co_msg_mapping = {
        981001: {
            'message': 'username existed',
            'http_code': 400,
            'sub_category': 'admin.creation'
        },
        981002: {
            'message': 'role not exists',
            'http_code': 400,
            'sub_category': 'admin.creation'
        },
        981051: {
            'message': 'db error while creating admin',
            'http_code': 500,
            'sub_category': 'admin.creation'
        },

        981101: {
            'message': 'Missing login credentials',
            'http_code': 400,
            'sub_category': 'login',
        },
        981102: {
            'message': 'Token expired',
            'http_code': 400,
            'sub_category': 'login',
        },
        981103: {
            'message': 'Token corrupted',
            'http_code': 400,
            'sub_category': 'login',
        },
        981104: {
            'message': 'Missing uid in deserialized data',
            'http_code': 400,
            'sub_category': 'login',
        },
        981105: {
            'message': 'Not supported user type',
            'http_code': 400,
            'sub_category': 'login',
        },
        981106: {
            'message': 'Missing token',
            'http_code': 400,
            'sub_category': 'login',
        },
        981107: {
            'message': 'Wrong token format',
            'http_code': 400,
            'sub_category': 'login',
        },
        981201: {
            'message': 'Retrieving session_info from wechat error',
            'http_code': 400,
            'sub_category': 'login.wechat',
        },
        981202: {
            'message': 'No openid found in session_info returned from wechat',
            'http_code': 404,
            'sub_category': 'login.wechat',
        },
        981203: {
            'message': 'Wechat user not found by id',
            'http_code': 404,
            'sub_category': 'login.wechat',
        },
        981251: {
            'message': 'Creating user in db error',
            'http_code': 500,
            'sub_category': 'login.wechat',
        },
        981301: {
            'message': 'Missing username while admin login',
            'http_code': 400,
            'sub_category': 'login.admin',
        },
        981302: {
            'message': 'Missing password while admin login',
            'http_code': 400,
            'sub_category': 'login.admin',
        },
        981303: {
            'message': 'Specified admin not exists',
            'http_code': 404,
            'sub_category': 'login.admin',
        },
        981304: {
            'message': 'Password not matched',
            'http_code': 400,
            'sub_category': 'login.admin',
        },
        981305: {
            'message': 'admin not found by id',
            'http_code': 404,
            'sub_category': 'login.admin',
        },
        981401: {
            'message': 'Permission denied',
            'http_code': 403,
            'sub_category': 'authorization',
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