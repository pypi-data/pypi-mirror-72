#coding:utf8
from flask import Blueprint
from flask_restplus import Api
from flask import current_app
#from wechat_utils.depends_framework.flask import APPLICATION_NAME

bp = Blueprint(current_app.config['WECHAT_UTILS_APPLICATION_NAME'], __name__)
api = Api(bp)

from .miniapp import user
from .mpapp import oauth,locator,gateway
