#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)

from flask import request
from flask_restplus import Resource

from wechat_utils.depends_framework.flask.auth.miniapp.auth import auth,login
from flask_mongoengine_orm import (
	ordering,
	searching,
	filting,
	paginating,
	retrieve,
)

from .. import api,bp
from . import ns
