#coding:utf8
import peewee
from flask import current_app

#db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)

class BaseModel(peewee.Model):
	class Meta:
		database = current_app.db