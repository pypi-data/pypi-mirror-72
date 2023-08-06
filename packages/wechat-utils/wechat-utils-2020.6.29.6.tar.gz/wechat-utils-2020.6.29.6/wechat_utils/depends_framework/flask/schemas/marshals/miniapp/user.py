#coding:utf8
from wechat_utils.depends_framework.flask.apis import api
from flask_restplus import fields

User = api.model(
	'User',
	{
		'id':fields.String(),
		'nickname':fields.String(),
		'avatar':fields.String(),
		'gender':fields.String(),
	}
)

Single = api.model(
	'Single',
	{
		'code':fields.Integer(),
		'single':fields.Nested(User),
	},
)

List = api.model(
	'List',
	{
		'code':fields.Integer(),
		'count':fields.Integer(),
		'entries':fields.List(fields.Nested(User)),
	},
)
