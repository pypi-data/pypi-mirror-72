#coding:utf8
import os
from wechat_utils.depends_database import WechatUtils as DependsDatabaseWechatUtils
from .admins.init import init_app as init_app_for_flask_admin

class WechatUtils(object):

	def __init__(
		self,
		app,
		is_use_flask_admin=False,
		is_use_blueprint=False,
		template_path=None,
	):
		"""
			1. 初始化依赖数据库，包括mongoengine连接、sqlalchemy建立对话
		"""
		DependsDatabaseWechatUtils(
			db_type=app.config['DB_TYPE'],
			db_name=app.config['DB_NAME'],
			db_host=app.config['DB_HOST'],
			db_port=app.config['DB_PORT'],
			db_username=app.config['DB_USERNAME'],
			db_password=app.config['DB_PASSWORD']
		)

		"""
			2. 初始化flask-admin
		"""
		init_app_for_flask_admin(app,is_use_flask_admin,template_path)


		"""
			是否使用蓝图
		"""
		key = 'WECHAT_UTILS_APPLICATION_NAME'
		if not app.config.get(key):
			app.config[key] = 'wechat'




		app.app_context().push()