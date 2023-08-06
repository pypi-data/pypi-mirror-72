#coding:utf8
from wechat_utils.depends_none.meta import Singleton
from .Mongoengine import ORM as MongoengineORM
from .Sqlalchemy import ORM as SqlchemyORM

class ORM(object, metaclass=Singleton):

	def __init__(self, db_type, model, *args, **kwargs):
		pass

	def __new__(self, db_type, model, *args, **kwargs):
		if db_type == 'mongo':
			return MongoengineORM(model)
		elif db_type in ['mysql','sqlite',]:
			return SqlchemyORM(model)
