#coding:utf8
from wechat_utils.depends_none.Redis import BaseWechatRedis
from wechat_utils.depends_database.settings import Settings

class WechatRedis(BaseWechatRedis):

	"""
		将settings作为参数，详细功能看父类
	"""

	def __init__(self):
		settings = Settings()

		super().__init__(
			appid = settings.appid,
			app_secret = settings.app_secret,
			host = settings.redis_host,
			port = settings.redis_port,
			db = settings.redis_db,
			password = password
		)



	