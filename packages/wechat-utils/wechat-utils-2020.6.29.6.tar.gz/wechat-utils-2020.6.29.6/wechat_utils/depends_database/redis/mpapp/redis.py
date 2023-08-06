#coding:utf8
from wechat_utils.depends_none.redis.mpapp import BaseMpRedis
from wechat_utils.depends_database.settings import Settings

class MpRedis(BaseMpRedis):

	"""
		将settings作为参数，详细功能看父类
	"""

	def __init__(self):
		settings = Settings()

		super().__init__(
			
			appid = settings.appid,
			app_secret = settings.app_secret,
			oauth_redirect_token_expiration = settings.oauth_redirect_token_expiration,

			host = settings.redis_host,
			port = settings.redis_port,
			db = settings.redis_db,
			password = settings.password,

		)
