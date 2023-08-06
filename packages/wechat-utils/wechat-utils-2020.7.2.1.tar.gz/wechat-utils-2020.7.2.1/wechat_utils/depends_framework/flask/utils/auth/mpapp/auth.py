#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask import request

from wechat_utils.depends_framework.flask.exceptions.auth import AuthException
from wechat_utils.depends_database.auth.mpapp import MpAuth
from wechat_utils.depends_database.redis.mpapp import MpRedis

def auth(func):
	def wrapper1(*args,**kwargs):

		token = request.environ.get('HTTP_TOKEN')
		mpauth = MpAuth()
		if not token:
			logger.info('>>> auth: missing token')
			raise AuthException(errcode=981106)

		user = mpauth.login_by_token(token)
		request.wechat_user = user

		return func(*args,**kwargs)
	return wrapper1

def oauth(func):
	def wrapper1(*args,**kwargs):

		args = request.get_json()
		code = args.get('code')
		state = args.get('state')
		mpauth = MpAuth()
		mpredis = MpRedis()

		if state:
			redirect_url = mpredis.retrieve_redirect_url(state)
		if not redirect_url:
			redirect_url = mpauth.post_oauth_redirect_url_default

		if not code:
			logger.info('>>> login: missing code')
			raise AuthException(errcode=100002)

		token,user = mpauth.oauth_login(code=code)
		request.wechat_user = user
		request.redirect_url = redirect_url

		return func(*args,**kwargs)
	return wrapper1

def locator(func):
	def wrapper1(*args,**kwargs):

		mpauth = MpAuth()
		redirect_url = mpauth.generate_redirect_url(request.referrer)
		request.redirect_url = redirect_url

		return func(*args,**kwargs)
	return wrapper1

