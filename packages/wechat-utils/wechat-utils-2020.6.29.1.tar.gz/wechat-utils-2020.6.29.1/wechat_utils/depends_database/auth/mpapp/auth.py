#coding:utf8
from wechat_utils.depends_database.settings import Settings
from wechat_utils.depends_database.redis.mpapp import MpRedis
from wechat_utils.depends_none.auth.mpapp.auth import BaseMpAuth
from wechat_utils.depends_database.orm import ORM
class MpAuth(BaseMpAuth):

	"""
			1. 默认使用数据库数据
			1. 实现了获取用户方法
	"""

	def __init__(self,
		appid=None,
		app_secret=None,
		token_secret_key=None,
		token_salt=None,
		token_expiration=None,
		oauth_redirect_url=None,
		post_oauth_redirect_url_default=None
	):
		settings = Settings()
		
		appid = appid or settings.appid
		app_secret = app_secret or settings.app_secret
		token_secret_key = token_secret_key or settings.token_secret_key
		token_salt = token_salt or settings.token_salt
		token_expiration = token_expiration or settings.token_expiration
		oauth_redirect_url = oauth_redirect_url or settings.oauth_redirect_url
		post_oauth_redirect_url_default = post_oauth_redirect_url_default or settings.post_oauth_redirect_url_default

		super().__init__(
			appid = appid,
			app_secret = app_secret,
			token_secret_key = token_secret_key,
			token_salt = token_salt,
			token_expiration = token_expiration,
			oauth_redirect_url = oauth_redirect_url,
			post_oauth_redirect_url_default = post_oauth_redirect_url_default,
		)

	def redis_persist_redirect_token(self,token, referrer):
		"""
			consistent with the Redis class
		"""
		return MpRedis().persist_redirect_token(token, referrer)

	def get_user(self,openid):
		try:
			return ORM('WechatUser').get(openid=openid)
		except:
			return None
