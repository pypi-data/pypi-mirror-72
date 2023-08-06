#coding:utf8
import os

def init_app(
		app,
		is_use_flask_admin=False,
		template_path=None,
	):
	"""
		2. BASE_PATH
	"""
	app.config['BASE_PATH'] = os.path.abspath(os.path.dirname(__file__))

	"""
		3. template_path，默认工作路径下
	"""
	if template_path is None:
		base_wechatutils_path = os.path.abspath(os.path.dirname(__file__))
		template_path = os.path.join(base_wechatutils_path, 'templates')
		app.template_path = template_path

	app.app_context().push()

	"""
		4. flask-admin，默认使用配置页
	"""
	if is_use_flask_admin:
		from wechat_utils.depends_framework.flask.admins.configuration import (
			BaseConfiguration as BaseConfigurationAdmin,
		)
		admin = app.extensions['admin'][0]
		admin.add_view(BaseConfigurationAdmin(name=u'微信设置'))

	return app