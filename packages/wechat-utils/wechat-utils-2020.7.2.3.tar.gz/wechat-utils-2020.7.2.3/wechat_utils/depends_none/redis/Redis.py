#coding:utf8

from wechat_utils.depends_none.meta import Singleton
from wechat_utils.depends_none.constans import Keys
import redis
import traceback

# log
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""""""""""""""""""""""""""

Client
======
* author	:	黄旭辉
* update	:	２０１９年０６月１５日１８：０５：０２


what
----
A class-based redis client

why
---
* Singleton	:	new one anywhere anytime you want,it will make itself's connention singleton.
* extend	:	you can inherit it and add some functions you want.

how-usage
---------

using it straightly is not a good idea.
you should use it like:

```python
class MyClient(object):
	def __new__(self):
		return Client(
			host=config.host,
			port=config.port,
			db=config.db,
			password=config.password)

myclient = MyClient()
myclient.client.set(name='hello', value='world', ex=60*1, px=None, nx=False, xx=False')
myclient.get('hello')
```

"""""""""""""""""""""""""""


class BaseRedis(object, metaclass=Singleton):

	"""
		这里提供redis最基础的功能
			1. 连接redis
			2. 提供get
			3. 提供set
	"""

	def __init__(self,host=None,port=6379,db=0,password=None):
		self.host = host or 'localhost'
		self.port = port
		self.db = db
		self.password = password
		self.pool = redis.ConnectionPool(
			host=self.host,
			port=self.port,
			db=self.db,
			password=self.password,
		)
		try:
			self.client = redis.StrictRedis(connection_pool=self.pool)
			logger.info('>>> baseredis')
			logger.info(self.host)
			logger.info(self.port)
			logger.info(self.password)
			self.client.ping()
		except redis.exceptions.ConnectionError as e:
			logger.error(
				'redis connection error: %s',
				traceback.format_exc(),
			)
			self.client = None
			raise e

	# 因为使用连接池，所以不需要关闭。
	# def __del__(self):
	# 	pass

	def get(self,key):
		value = self.client.get(key)
		if value is not None:
			value = value.decode('utf8')
			return value
		else:
			return None

	def set(self,key,expires_in,value):
		
		self.client.setex(key, int(expires_in), value)



class BaseWechatRedis(BaseRedis):

	"""
		这里提供公众号和小程序通用的同能
			1. access_token
	"""

	def __init__(self,
		appid,
		app_secret,

		host=None,
		port=None,
		db=None,
		password=None
	):
		self.appid = appid
		self.app_secret = app_secret

		super().__init__(
			host = host,
			port = port,
			db = db,
			password = password
		)

	@property
	def access_token(self):

		def _get_access_token_from_tencent(appid,app_secret):
			url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}".format(
				appid=appid,
				appsecret=app_secret,
			)
			response = requests.get(url)
			return response.json()['access_token'],response.json()['expires_in']

		# get access_token from redis
		access_token = self.get(Keys.access_token)
		
		if access_token is None:

			# get access_token from tencent
			access_token,expires_in = _get_access_token_from_tencent(self.appid,self.app_secret)

			# save access_token to redis
			self.set(Keys.access_token,expires_in,access_token)
		return access_token