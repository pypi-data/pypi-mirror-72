#coding:utf8
from .base import BaseORM
from importlib import import_module
from wechat_utils.depends_none.sqlalchemy_engine_session import EngineSession


class ORM(BaseORM):

	def __init__(self,model):
		self.engine,self.session = EngineSession()
		pre_path = 'wechat_utils.depends_database.models.Sqlalchemy.'
		self.model = import_module(pre_path+model)

	def get(self,**kwargs):
		return self.session.query(self.model).filter(**kwargs)

	def save(self,**kwargs):
		instance = model(**kwargs)
		self.session.add(instance)
		self.session.commit()

	def update(self,instance,**kwargs):
		for key,value in kwargs.items():
			setattr(instance,key,value)
		self.session.commit()
