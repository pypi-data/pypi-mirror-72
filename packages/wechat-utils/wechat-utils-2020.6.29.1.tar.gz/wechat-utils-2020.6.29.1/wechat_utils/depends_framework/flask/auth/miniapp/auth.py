#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask import request

from wechat_utils.depends_database.auth.miniapp import MiniappAuth
from wechat_utils.depends_framework.flask.exceptions import AuthException

class FlaskMiniappAuth(MiniappAuth):
	"""
		加了flask的抛出异常
	"""
	EXCEPTION_TOKEN_EXPIRED = AuthException(errcode=981102)
	EXCEPTION_TOKEN_CORRUPTED = AuthException(errcode=981103)
	EXCEPTION_TOKEN_DECRYPT_FAIL = AuthException(errcode=981109)
	EXCEPTION_MISSING_TOKEN = AuthException(errcode=981104)
	EXCEPTION_OPENID_NOT_FOUND = AuthException(errcode=981203)

# flask
def auth(func):
	def wrapper1(*args,**kwargs):

		token = request.environ.get('HTTP_TOKEN')
		
		if not token:
			logger.info('>>> auth: missing token')
			raise AuthException(errcode=981106)

		user = FlaskMiniappAuth().login_by_token(token)
		request.wechat_user = user

		return func(*args,**kwargs)
	return wrapper1

def login(func):
	def wrapper1(*args,**kwargs):

		code = request.args.get('code')

		if not code:
			logger.info('>>> login: missing code')
			raise AuthException(errcode=981108)

		token,user = FlaskMiniappAuth().login_by_code(code=code)
		request.token = token
		request.wechat_user = user
		return func(*args,**kwargs)
	return wrapper1