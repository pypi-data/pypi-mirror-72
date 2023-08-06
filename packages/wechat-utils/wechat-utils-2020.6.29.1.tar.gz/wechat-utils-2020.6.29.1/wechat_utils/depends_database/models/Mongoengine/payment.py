#coding:uf8
from mongoengine import (
	Document,
	BooleanField,StringField,
	NULLIFY,
)
from flask_mongoengine import BaseQuerySet
from .mixin import DatetimeMixin,NumberMixin

class BaseWechatPayment(Document,DatetimeMixin,NumberMixin):

	number = StringField(max_length=100,verbose_name="支付单号")
	user = ReferenceField('WechatUser',reverse_delete_rule=NULLIFY,verbose_name="用户")
	status = StringField(choices=[
		('pay_ing', '正在支付'),
		('pay_success', '支付成功'),
		('pay_fail', '支付失败'),
		('pay_unusual', '支付异常'),
	], max_length=100,verbose_name="支付状态")
	total_fee = IntField(verbose_name="支付价格")

	openid = StringField(max_length=100)
	result_code = StringField(max_length=100,verbose_name="业务结果")
	err_code = StringField(max_length=100,verbose_name="错误代码")
	err_code_des = StringField(max_length=100,verbose_name="错误代码描述")
	transaction_id = StringField(max_length=100,verbose_name="微信订单号")
	bank_type = StringField(max_length=100,verbose_name="付款银行")
	settlement_total_fee = IntField(verbose_name="应结订单金额（分）")
	cash_fee = StringField(max_length=100,verbose_name="现金支付金额")
	cash_fee_type = StringField(max_length=100,verbose_name="现金支付货币类型")
	coupon_fee = IntField(verbose_name="代金券金额（分）")
	coupon_count = IntField(verbose_name="代金券使用数量")

	#order = ReferenceField('Order',reverse_delete_rule=NULLIFY,verbose_name="订单")

	meta = {
		'abstract': True,
		'allow_inheritance': True,
		'queryset_class': BaseQuerySet,
		'collection':'wechat_payment',
	}