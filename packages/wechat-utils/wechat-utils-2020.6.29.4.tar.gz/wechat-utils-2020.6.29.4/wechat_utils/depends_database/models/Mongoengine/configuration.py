#coding:utf8
from mongoengine import (
	Document,
	BooleanField,StringField,
)
from flask_mongoengine import BaseQuerySet

class BaseCongifuration(Document):
	appid = StringField(max_length=100,verbose_name="appid")
	app_secret = StringField(max_length=100,verbose_name="app_secret")
	app_category = StringField(max_length=100,verbose_name="app_category")
	mch_id = StringField(max_length=100,verbose_name="mch_id")
	mch_secret = StringField(max_length=100,verbose_name="mch_secret")
	token_secret_key = StringField(max_length=100,verbose_name="token_secret_key")
	token_salt = StringField(max_length=100,verbose_name="token_salt")
	token_expiration = StringField(max_length=100,verbose_name="token_expiration")
	redis_db = StringField(max_length=100,verbose_name="redis_db")
	redis_host = StringField(max_length=100,verbose_name="redis_host")
	redis_port = StringField(max_length=100,verbose_name="redis_port")
	redis_password = StringField(max_length=100,verbose_name="redis_password")
	access_token_expiration = StringField(max_length=100,verbose_name="access_token_expiration")
	oauth_redirect_url = StringField(max_length=100,verbose_name="oauth_redirect_url")
	post_oauth_redirect_url_default = StringField(max_length=100,verbose_name="post_oauth_redirect_url_default")
	mp_token = StringField(max_length=100,verbose_name="mp_token")

	meta = {
		'abstract': True,
		'allow_inheritance': True,
		'queryset_class': BaseQuerySet,
		'collection':'wechat_configuration',
	}

class Configuration(BaseCongifuration):
	"""
		wechat-utils的有些地方会调用这个类，比如settings
	"""
	pass
