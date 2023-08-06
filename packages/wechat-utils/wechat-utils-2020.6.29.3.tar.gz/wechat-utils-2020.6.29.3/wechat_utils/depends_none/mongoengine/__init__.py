#coding:utf8
from mongoengine.document import Document
from mongoengine.fields import StringField,DateTimeField
from flask_mongoengine import BaseQuerySet
import datetime

# log
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DatetimeMixin(Document):

	create_datetime = DateTimeField(verbose_name="创建时间")#,default=get_time)
	write_datetime = DateTimeField(verbose_name="修改时间")

	# example
	#blog = ListField(ReferenceField('Blog'),bind_with='category')

	meta = {
		'abstract': True,
		'allow_inheritance': True,
		'queryset_class': BaseQuerySet,
	}


	#
	# 如果是第一次save(即创建)，自动补充create_datetime字段
	#
	def save(self, *args, **kwargs):
		str_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.write_datetime = str_datetime
		if self.id is None:
			self.create_datetime = str_datetime
		super().save(*args, **kwargs)



class NumberMixin(Document):

	number = StringField(max_length=100,verbose_name="单号")

	meta = {
		'abstract': True,
		'allow_inheritance': True,
		'queryset_class': BaseQuerySet,
	}

	def save(self, *args, **kwargs):

		import random
		import time

		while True:

			letter = "".join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWSYZ',5))
			day = time.strftime("%Y%m%d", time.localtime())
			number = day + letter

			try:
				self.__class__.objects.get(number=number)
			except:
				self.number = number
				import traceback
				logger.error(traceback.print_exc())
				break

		super().save(*args, **kwargs)