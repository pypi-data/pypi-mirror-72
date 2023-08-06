defaults = {
	'appid':'xxx',
	'app_secret':'xxx',
	'app_category':'xxx',
	'mch_id':'xxx',
	'mch_secret':'xxx',

	'token_secret_key':'xxx',
	'token_salt':'xxx',
	'token_expiration':60*60*24*7,
	
	'redis_db':0,
	'redis_host':'xxx',
	'redis_port':6379,
	'redis_password':'xxx',
	'access_token_expiration':60*60*2,
	
	'oauth_redirect_url':'xxx',
	'post_oauth_redirect_url_default':'xxx',
	'oauth_redirect_token_expiration':60*60*24*365,
	'mp_token':'xxx',
}

from .Mongoengine import Settings as MongoengineSettings
from .Sqlalchemy import Settings as SqlalchemySettings
from wechat_utils.depends_none.meta import Singleton

class Settings(object, metaclass=Singleton):

	def __init__(self, db_type, *args, **kwargs):
		pass

	def __new__(cls, db_type=None, *args, **kwargs):
		if db_type == 'mongo':
			return MongoengineSettings()
		if db_type in ['sqlite','sqlite3','mysql',]:
			return SqlalchemySettings()
