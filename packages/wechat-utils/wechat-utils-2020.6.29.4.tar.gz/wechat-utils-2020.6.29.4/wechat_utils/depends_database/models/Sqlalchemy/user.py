#coding:utf8
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def to_dict(self):
	return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict

class BaseUser(Base):
	__tablename__ = 'wechat_user'
	__abstract__ = True

	id = Column(Integer, primary_key=True)
	openid = Column(String(200))
	unionid = Column(String(200))
	nickname = Column(String(200))
	gender = Column(String(200))
	language = Column(String(200))
	city = Column(String(200))
	province = Column(String(200))
	country = Column(String(200))
	avatar = Column(String(1000))
	mobile = Column(String(200))
	session_key = Column(String(200))
	category = Column(String(200))

class User(BaseUser):
	pass
