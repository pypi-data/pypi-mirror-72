#coding:utf8
from wechat_utils.depends_none.meta import Singleton
import abc

class BaseORM(object, metaclass=Singleton):

	@abc.abstractmethod
	def get(self,**kwargs):
		pass

	@abc.abstractmethod
	def save(self,**kwargs):
		pass

	@abc.abstractmethod
	def update(self,instance,**kwargs):
		pass
