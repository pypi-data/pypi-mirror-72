# coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from rest_framework.views import APIView
#from wechat_utils.depends_framework.django.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import serializers

from wechat_utils.depends_framework.django.auth.miniapp import (
	auth,
	login,
	DjangoMiniappAuth,
)

"""
	方式1：使用rest_framework权限认证
"""
from wechat_utils.depends_framework.django.exceptions.auth import AuthException
from wechat_utils.depends_framework.django.utils.common import POST_to_dict
from wechat_utils.depends_framework.django.schemas.disserializers.user import LoginDisserializer
class Auth(object):
	def authenticate(self,request):
		token = request.environ.get('HTTP_TOKEN')
		if not token:
			logger.info('>>> auth: missing token')
			raise AuthException(errcode=981104)
		user = DjangoMiniappAuth().login_by_token(token)
		request.wechat_user = user

		return (user,token)

class Login(object):
	def authenticate(self,request):

		print('>>> login.auth')
		print(request.data)

		disser = LoginDisserializer(data=request.data)
		disser.is_valid(raise_exception=True)

		print(disser)
		#code = POST_to_dict(request.POST).get('code')
		code = disser.data.get('code')

		if not code:
			logger.info('>>> login: missing code')
			raise AuthException(errcode=981108)

		token,user = DjangoMiniappAuth().login_by_code(code=code)
		request.token = token
		request.wechat_user = user

		"""
			request.user,request.auth = tuple(,)
			rest_framework.request 第380行
		"""
		return (user, token)

class Single1(APIView):
	authentication_classes = [Login,]
	parser_classes = [JSONParser,]
	def post(self,request,*args,**kwargs):	

		user = {
			'nickname':request.wechat_user.nickname,
			'token':request.token,
		}
		return Response(user)

"""
	方式2：使用装饰器认证
"""
class Single2(APIView):

	@login
	def post(self,request,format=None):
		user = {
			'nickname':request.wechat_user.nickname,
			'token':request.token,
		}
		return Response(user)
