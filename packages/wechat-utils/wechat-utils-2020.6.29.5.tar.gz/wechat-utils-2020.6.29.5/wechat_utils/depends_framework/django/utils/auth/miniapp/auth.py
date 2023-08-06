#coding:utf8
from crequest.middleware import CrequestMiddleware

from wechat_utils.depends_database.auth.miniapp import MiniappAuth
from wechat_utils.depends_framework.django.utils.common import POST_to_dict
from pprint import pprint

from wechat_utils.depends_framework.django.middleware import WechatUtilsMiddleware

from wechat_utils.depends_framework.django.exceptions.auth import AuthException
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DjangoMiniappAuth(MiniappAuth):
	"""
		加了flask的抛出异常
	"""
	EXCEPTION_TOKEN_EXPIRED = AuthException(errcode=981102)
	EXCEPTION_TOKEN_CORRUPTED = AuthException(errcode=981103)
	EXCEPTION_TOKEN_DECRYPT_FAIL = AuthException(errcode=981109)
	EXCEPTION_MISSING_TOKEN = AuthException(errcode=981104)
	EXCEPTION_OPENID_NOT_FOUND = AuthException(errcode=981203)


def auth(func):

	def wrapper1(args,**kwargs):
		current_request = WechatUtilsMiddleware.get_request()
		token = current_request.environ.get('HTTP_TOKEN')

		if not token:
			logger.info('>>> auth: missing token')
			raise AuthException(errcode=981104)

		user = DjangoMiniappAuth().login_by_token(token)
		current_request.wechat_user = user

		return func(*args,**kwargs)
	return wrapper1

def login(func):

	def wrapper1(*args,**kwargs):
		print('>>> login')
		current_request = WechatUtilsMiddleware.get_request()
		print(current_request.POST)
		code = POST_to_dict(current_request.POST).get('code')

		if not code:
			logger.info('>>> login: missing code')
			raise AuthException(errcode=981108)

		token,user = DjangoMiniappAuth().login_by_code(code=code)
		current_request.token = token
		current_request.wechat_user = user
		return func(*args,**kwargs)
	return wrapper1
