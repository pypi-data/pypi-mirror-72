#coding:utf8

from wechat_utils.depends_none.meta import Singleton
from wechat_utils.depends_database.models.Mongoengine.configuration import Configuration

from . import defaults

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Settings(object, metaclass=Singleton):

	def __init__(self):
		self.defaults = defaults
		self.configuration = Configuration.objects.first()

	def __setattr__(self, key, value):  #增加或修改函数
		return object.__setattr__(self,key,value)

	def __getattr__(self,key):
		configuration_dict = self.configuration.to_mongo().to_dict()
		return configuration_dict.get(key) or self.defaults.get(key)

	def update(self,dict1):
		if self.configuration:
			self.configuration.update(**dict1)
		else:
			self.configuration = Configuration(**dict1)
			self.configuration.save()
		self.configuration = Configuration.objects.first()
		return self.configuration.to_mongo().to_dict()
