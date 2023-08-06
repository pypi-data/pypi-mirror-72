#coding:utf8

from ..depends_none.meta import Singleton
from mongoengine import connect
from wechat_utils.depends_none.sqlalchemy_engine_session import EngineSession
from wechat_utils.depends_database.settings import Settings

class WechatUtils(object):

	def __init__(
		self,
		db_type,
		db_name,
		db_host,
		db_port,
		db_username,
		db_password
	):
		if db_type == 'mongo':
			connect(
				db_name,
				host=db_host,
				port=db_port,
				username=db_username, 
				password=db_password, 
			)
		elif db_type in ['sqlite','sqlite3','mysql',]:
			if db_type in ['sqlite','sqlite3',]:
				url = 'sqlite:///'+db_name+'?check_same_thread=False'
				print('>>> wechat_utils')
				print(url)
			elif db_type == 'mysql':
				url = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
					db_username,
					db_password,
					db_host,
					db_port,
					db_name,
				)
			else:
				raise Exception('wrong DB_TYPE')
			# 单例模式，第一次调用后，之后的实例化都不需要输入参数了。
			engine,session = EngineSession(url=url)
			settings = Settings(db_type=db_type)

			# 创建数据库
			from wechat_utils.depends_database.models.Sqlalchemy.configuration import Base
			Base.metadata.create_all(engine)
			from wechat_utils.depends_database.models.Sqlalchemy.user import Base
			Base.metadata.create_all(engine)
