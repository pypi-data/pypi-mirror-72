#coding:utf8

from wechat_utils.depends_none.meta import Singleton
from wechat_utils.depends_database.models.Sqlalchemy.configuration import Configuration

from . import defaults

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from wechat_utils.depends_none.sqlalchemy_engine_session import EngineSession

class Settings(object, metaclass=Singleton):

	def __init__(self,url=None):
		self.defaults = defaults
		self.engine,self.session = EngineSession(url)
		try:
			self.configuration = self.session.query(Configuration).first()
		except:
			self.configuration = None

	def __setattr__(self, key, value):  #增加或修改函数
		return object.__setattr__(self,key,value)

	def __getattr__(self,key):
		if self.configuration:
			return self.configuration.to_dict().get(key) or self.defaults.get(key)
		else:
			return self.defaults.get(key)

	def update(self,dict1):
		if self.configuration:
			for key,value in dict1.items():	
				setattr(self.configuration,key,value)
			# self.configuration.update(**dict1)
		else:
			configuration = Configuration(**dict1)
			self.session.add(configuration)
		self.session.commit()
		self.configuration = self.session.query(Configuration).first()
		return self.configuration.to_dict()


