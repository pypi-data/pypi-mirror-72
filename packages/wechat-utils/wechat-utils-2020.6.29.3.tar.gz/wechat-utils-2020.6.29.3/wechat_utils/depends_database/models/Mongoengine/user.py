#coding:uf8
from mongoengine import (
	Document,
	BooleanField,StringField,
)
from flask_mongoengine import BaseQuerySet

class BaseWechatUser(Document):
	openid = StringField(max_length=100,verbose_name="openid")
	unionid = StringField(max_length=100,verbose_name="unionid")
	nickname = StringField(max_length=100,verbose_name="昵称")
	gender = StringField(max_length=100,verbose_name="性别")
	language = StringField(max_length=100,verbose_name="语言")
	city = StringField(max_length=100,verbose_name="城市")
	province = StringField(max_length=100,verbose_name="省份")
	country = StringField(max_length=100,verbose_name="国家")
	avatar = StringField(max_length=800,verbose_name="头像")
	mobile = StringField(max_length=100,verbose_name="手机")

	session_key = StringField(max_length=100,verbose_name="session_key")

	category = db.ListField(
		db.StringField(
			max_length=100, 
			verbose_name="用户种类", 
			default='小程序',
			choices=[
				'小程序',
				'公众号',
			], 
		)
	)

	def __str__(self):
		for attr in [
			self.nickname,
			self.mobile,
			self.openid,
		]:
			if attr:
				return str(attr)
		
		return 'null'

	meta = {
		'abstract': True,
		'allow_inheritance': True,
		'queryset_class': BaseQuerySet,
		'collection':'wechat_user',
	}

class WechatUser(BaseWechatUser):
	pass
