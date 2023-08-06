#coding:utf8
from .meta import Singleton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class EngineSession(object, metaclass=Singleton):

	def __init__(self, url=None, *args, **kwargs):
		pass

	def __new__(cls, url, *args, **kwargs):
		engine = create_engine(url, echo=True)
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		return engine,session

	def __del__(self):
		self.session.close()

		"""
			不需要这一句，
			因为create_engine中一个参数poolclass = NullPool，
			那么engine将不会再使用连接池，那么连接将会在 session.close()后直接关闭.
			默认poolclass = NullPool，
		"""
		#self.engine.dispose()
