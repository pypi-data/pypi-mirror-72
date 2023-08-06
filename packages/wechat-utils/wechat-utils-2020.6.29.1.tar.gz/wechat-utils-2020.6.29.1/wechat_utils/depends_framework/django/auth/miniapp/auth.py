#coding:utf8
from crequest.middleware import CrequestMiddleware

from wechat_utils.depends_database.auth.miniapp import MiniappAuth
from wechat_utils.depends_framework.django.utils.common import POST_to_dict
from pprint import pprint

from wechat_utils.depends_framework.django.middleware import WechatUtilsMiddleware

from wechat_utils.depends_framework.django.exceptions.auth import AuthException

from wechat_utils.depends_framework.django.schemas.disserializers.user import LoginDisserializer

import json

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from rest_framework.parsers import JSONParser

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

		print('>>> wrapper.login')

		current_request = WechatUtilsMiddleware.get_request()

		# # 自己实现parser
		#stream = current_request._stream.read().decode('utf8')
		#data = json.loads(stream)
		#code = POST_to_dict(current_request.POST).get('code')
		#code = data.get('code')

		# # 使用框架parser
		from rest_framework import parsers
		from rest_framework.request import Request
		request = Request(
			current_request,
			parsers=[JSONParser(),]
		)
		data,_ = request._parse()
		code = data.get('code')

		if not code:
			logger.info('>>> login: missing code')
			raise AuthException(errcode=981108)

		token,user = DjangoMiniappAuth().login_by_code(code=code)
		current_request.token = token
		current_request.wechat_user = user
		return func(*args,**kwargs)
	return wrapper1









