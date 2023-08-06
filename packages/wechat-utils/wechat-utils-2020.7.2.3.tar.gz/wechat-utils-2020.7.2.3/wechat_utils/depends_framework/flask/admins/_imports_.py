#coding:utf8
import os
import logging
logging.basicConfig(level=logging.DEBUG)

from flask_admin import BaseView, expose
from flask import request,current_app

from wechat_utils.depends_database.settings import Settings