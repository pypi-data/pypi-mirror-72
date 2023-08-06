#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import abc

from wechat_utils.depends_none.exceptions.auth import (
	TokenExpiredException,
	TokenCorruptedException,
	TokenDecryptException,
	MissingTokenException,
	OpenidNotFoundException
)

from wechat_utils.depends_none.auth.base import BaseAuth
from wechat_utils.depends_none.wx_api.miniapp.userinfo import get_session_key_from_wx,decrypt_wechat_user

class BaseMiniappAuth(metaclass=abc.ABCMeta):

	EXCEPTION_TOKEN_EXPIRED = TokenExpiredException('Token expired!')
	EXCEPTION_TOKEN_CORRUPTED = TokenCorruptedException('Token corrupted!')
	EXCEPTION_TOKEN_DECRYPT_FAIL = TokenDecryptException('Token decrypted fail!')
	EXCEPTION_MISSING_TOKEN = MissingTokenException('Missing token!')
	EXCEPTION_OPENID_NOT_FOUND = OpenidNotFoundException('Openid not found!')


	"""
		抽象出来解密过程。
		通过输入解密必要的参数和实现抽象方法，完成用户的登录，注册，更新信息等功能
	"""

	def __init__(self,
		appid,
		app_secret,
		token_secret_key,
		token_salt,
		token_expiration
	):
		self.appid = appid,
		self.app_secret = app_secret
		self.token_secret_key = token_secret_key
		self.token_salt = token_salt
		self.token_expiration = token_expiration

	@abc.abstractmethod
	def get_user_by_openid(self,openid):
		"""
			参数：
				openid：微信用户唯一标示
			返回：
				user对象
		"""
		pass

	@abc.abstractmethod
	def save_user(self,userinfo):
		"""
			参数：
				userinfo：字典
			返回：
				user对象
		"""
		pass

	@abc.abstractmethod
	def update_user(self,openid,decrypted_data):
		"""
			参数：
				decrypted_data：用户信息
			返回：
				user对象
		"""
		pass

	def login_by_code(self,code):
		_userinfo = get_session_key_from_wx(
			appid=self.appid,
			appsecret=self.app_secret,
			js_code=code
		)
		userinfo = {
			'openid':_userinfo['openid'],
			'unionid':_userinfo['unionid'],
			'session_key':_userinfo['session_key'],
		}

		user = self.get_user_by_openid(openid=userinfo.get('openid'))
		if user is None:
			user = self.save_user(userinfo=userinfo)

		token = BaseAuth.encrypt(
			data={'openid':str(user.openid)},
			secret_key=self.token_secret_key,
			salt=self.token_salt,
			expires_in=self.token_expiration
		)
		return token,user

	def login_by_token(self,token):
		try:
			data = BaseAuth.decrypt(
				token=token,
				secret_key=self.token_secret_key,
				salt=self.token_salt,
				expires_in=self.token_expiration
			)
		except SignatureExpired:
			logger.info('Token expired for: %s', token)
			#raise AuthException(errcode=981102)
			raise self.EXCEPTION_TOKEN_EXPIRED
		except (BadSignature, BadTimeSignature):
			logger.info('Token corrupted: %s', token)
			#raise AuthException(errcode=981103)
			raise EXCEPTION_TOKEN_CORRUPTED
		except Exception as e:
			logger.info('unexpected decrypt error: %s', token)
			#raise AuthException(errcode=100001)
			raise EXCEPTION_TOKEN_DECRYPT_FAIL

		if not data.get('openid'):
			logger.info('token missing openid: %s', token)
			#raise AuthException(errcode=981104)
			raise EXCEPTION_MISSING_TOKEN

		user = self.get_user_by_openid(id=data.get('openid'))

		if user is None:
			logger.info('user not found by openid: %s', data.get('openid'))
			#raise AuthException(errcode=981203)
			raise EXCEPTION_OPENID_NOT_FOUND
		return user

	def update(self,user,iv,encrypted_data):
		decrypted_data = decrypt_wechat_user(
			session_key=user.session_key, 
			iv=iv,
			encrypted_data=encrypted_data
		)
		user = self.update_user(decrypted_data['openid'],decrypted_data)
		return user
