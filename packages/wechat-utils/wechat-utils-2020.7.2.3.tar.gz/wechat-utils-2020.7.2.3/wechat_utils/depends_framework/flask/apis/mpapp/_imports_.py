#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)

# 框架
from flask import request
from flask_restplus import Resource
from werkzeug.utils import redirect

# 第三方库
from wechatpy.events import EVENT_TYPES

# 自己的库
from wechat_utils.depends_database.auth.mpapp import MpAuth
from wechat_utils.depends_none.parser import parse_with
from wechat_utils.depends_framework.flask.auth.mpapp import locator,oauth,auth

from .. import api,bp
from . import ns
