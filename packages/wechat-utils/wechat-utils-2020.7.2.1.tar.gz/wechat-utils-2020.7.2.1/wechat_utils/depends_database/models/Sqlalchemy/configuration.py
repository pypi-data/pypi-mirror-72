#coding:utf8
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def to_dict(self):
	return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict

class BaseConfiguration(Base):
	__tablename__ = 'wechat_configuration'
	__abstract__ = True

	id = Column(Integer, primary_key=True)
	appid = Column(String(200))
	app_secret = Column(String(200))
	app_category = Column(String(200))
	mch_id = Column(String(200))
	mch_secret = Column(String(200))
	token_secret_key = Column(String(200))
	token_salt = Column(String(200))
	token_expiration = Column(Integer)
	redis_db = Column(String(200))
	redis_host = Column(String(200))
	redis_port = Column(Integer)
	redis_password = Column(String(200))
	access_token_expiration = Column(Integer)
	
	oauth_redirect_url = Column(String(200))
	oauth_redirect_token_expiration = Column(Integer)
	post_oauth_redirect_url_default = Column(String(200))
	mp_token = Column(String(200))

class Configuration(BaseConfiguration):
	pass
