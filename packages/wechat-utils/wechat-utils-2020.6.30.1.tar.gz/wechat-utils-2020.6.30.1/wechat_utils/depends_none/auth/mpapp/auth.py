#coding:utf8
import hashlib
import logging
logger = logging.getLogger(__name__)
from six.moves.urllib.parse import quote

from wechat_utils.depends_none.auth.base import BaseAuth
from wechat_utils.depends_none.common import Random

import abc

# 第三方
from wechatpy import WeChatOAuth
from wechatpy import parse_message
from wechatpy.utils import check_signature, random_string

class BaseMpAuth(metaclass=abc.ABCMeta):

	"""
		1. 提供重定向功能
		1. 需要实现获取用户方法
	"""

	access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
	oauth_scope = 'snsapi_userinfo'
	oauth_base_url = 'https://open.weixin.qq.com/connect/'

	def __init__(self,
		appid,
		app_secret,
		token_secret_key,
		token_salt,
		token_expiration,
		oauth_redirect_url,
		post_oauth_redirect_url_default
		):
		self.appid = appid
		self.app_secret = app_secret
		self.token_secret_key = token_secret_key
		self.token_salt = token_salt
		self.token_expiration = token_expiration
		self.oauth_redirect_url=oauth_redirect_url
		self.post_oauth_redirect_url_default=post_oauth_redirect_url_default

		self.oauth = WeChatOAuth(
			self.appid,
			self.app_secret,
			self.oauth_redirect_url,
			self.oauth_scope,
		)

	@abc.abstractmethod
	def redis_persist_redirect_token(self,token, referrer):
		"""
			参数：
				token：用户token
				referrer：用户登录前的url
		"""
		pass

	@abc.abstractmethod
	def get_user(self,openid):
		pass

	def _generate_redirect_url(self, state=None):
		redirect_uri = quote(self.oauth_redirect_url, safe=b'')
		url_list = [
			self.oauth_base_url,
			'oauth2/authorize?appid=',
			self.appid,
			'&redirect_uri=',
			redirect_uri,
			'&response_type=code&scope=',
			self.oauth_scope
		]
		if state:
			url_list.extend(['&state=', state])
		url_list.append('#wechat_redirect')
		logger.info('>>> {}'.format(url_list))
		return ''.join(url_list)

	def generate_redirect_url(self, referrer):
		if not referrer:
			referrer = self.post_oauth_redirect_url_default
		md5 = hashlib.md5(referrer.encode('utf8')).hexdigest()
		token = Random.generate(8, suffix=md5)
		self.redis_persist_redirect_token(token, referrer)
		return self._generate_redirect_url(token)

	def oauth_login(self,code):
		res = self.oauth.fetch_access_token(code)
		user = self.get_user(openid=res.get('openid'))
		token = BaseAuth.encrypt(
			data={'openid':str(user.openid)},
			secret_key=self.token_secret_key,
			salt=self.token_salt,
			expires_in=self.token_expiration
		)
		return token,user

	def parse_message(self, xml_payload):
		return parse_message(xml_payload)