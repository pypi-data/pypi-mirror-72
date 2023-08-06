#coding:utf8
from wechat_utils.depends_none.auth.miniapp import BaseMiniappAuth
from wechat_utils.depends_database.settings import Settings
from wechat_utils.depends_database.orm import ORM
class MiniappAuth(BaseMiniappAuth):

	"""
		1. 将settings作为必要参数输入
		2. 实现一些抽象方法，例如获取用户、插入用户、更新用户等。
	"""

	def __init__(self):
		settings = Settings()

		super().__init__(
			appid = settings.appid,
			app_secret = settings.app_secret,
			token_secret_key = settings.token_secret_key,
			token_salt = settings.token_salt,
			token_expiration = settings.token_expiration
		)

	def get_user_by_openid(self,openid):
		"""
			return user object,or none
		"""
		try:
			return ORM('WechatUser').get(openid=openid)
		except:
			return None

	def save_user(self,userinfo):
		"""
			save user,
			and return user object
		"""
		try:
			return ORM('WechatUser').save(**userinfo)
		except:
			return None

	def update_user(self,openid,decrypted_data):
		"""
			update user,
			and return user object
		"""
		try:
			orm = ORM('WechatUser')
			instance = orm.get(openid=openid)
			orm.update(instance,**decrypted_data)
			return instance
		except:
			return None
