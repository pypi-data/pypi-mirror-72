#coding:utf8
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from wechat_utils.depends_none.redis.Redis import BaseWechatRedis
from wechat_utils.depends_none.constans import Keys

class BaseMpRedis(BaseWechatRedis):

	"""
		这里提供公众号的功能
			1. 提供登录成功后的重定向
	"""

	def __init__(self,
		appid,
		app_secret,
		oauth_redirect_token_expiration,

		host,
		port,
		db,
		password
	):

		self.oauth_redirect_token_expiration = oauth_redirect_token_expiration

		super().__init__(
			appid = appid,
			app_secret = app_secret,

			host = host,
			port = port,
			db = db,
			password = password
		)

	def persist_redirect_token(self, token, url):
		try:
			key = Keys.oauth_redirect_token.format(token)
			self.set(key, self.oauth_redirect_token_expiration, url)
		except:
			logger.error(
				'Error while persisting oauth redirect token. token: %s url: %s Err: %s',
				token,
				url,
				traceback.format_exc(),
			)
			return False
		else:
			return True

	def retrieve_redirect_url(self, token):
		try:
			key = Keys.oauth_redirect_token.format(token)
			url = self.get(key)
		except:
			logger.error(
				'Error while retrieving oauth redirect url. token: %s Err: %s',
				token,
				traceback.format_exc(),
			)
			return None
		else:
			return url
