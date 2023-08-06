#coding:utf8
from .base import BaseORM
from importlib import import_module

class ORM(BaseORM):

	def __init__(self,model):
		pre_path = 'wechat_utils.depends_database.models.Mongoengine.'
		self.model = import_module(pre_path+model)

	def get(self,**kwargs):
		return self.model.objects.get(**kwargs)

	def save(self,**kwargs):
		instance = self.model(**kwargs)
		instance.save()
		return instance

	def update(self,instance,**kwargs):
		instance.update(**kwargs)
		return instance