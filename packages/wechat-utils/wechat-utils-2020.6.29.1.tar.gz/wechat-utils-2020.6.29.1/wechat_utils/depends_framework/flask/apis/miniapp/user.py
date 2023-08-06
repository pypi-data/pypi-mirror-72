#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

from wechat_utils.depends_framework.flask.auth.miniapp import (
	login,
	auth,
	FlaskMiniappAuth,
)

# 兼容之前写的插件
from flask import current_app
if current_app.config['DB_TYPE'] in ['mongo']:
	from wechat_utils.depends_database.models.Mongoengine.user import User as UserModel
else:
	from wechat_utils.depends_database.models.Sqlalchemy.user import User as UserModel

from wechat_utils.depends_framework.flask.schemas.parsers.miniapp.user import(
	Post as PostParser,
	Patch as PatchParser,
	List as ListParser,
)
from wechat_utils.depends_framework.flask.schemas.marshals.miniapp.user import (
	Single as SingleMarshal,
	List as ListMarshal,
)

@ns.route('/user')
class Single(Resource):

	@api.doc(parser=PostParser)
	@login
	def post(self):
		return {
			'code':0,
			'token':request.token,
		}

	@api.doc(parser=PatchParser)
	@auth
	@api.marshal_with(SingleMarshal)
	def patch(self):
		return {
			'code':0,
			'single':request.wechat_user,
		}

# @ns.route('/user/list')
# class List(Resource):
# 	@api.doc(parser=ListParser)
# 	@searching(UserModel,key='searching',fields=['nickname',])
# 	@ordering(UserModel,key='ordering',fields=['-nickname','+nickname'])
# 	#@filting(UserModel,filting_list)
# 	@paginating(UserModel,page_field='page',page_size_field='page_size')
# 	@ns.marshal_with(ListMarshal)
# 	def get(self):
# 		return {
# 			'code':0,
# 			'count':request.page_count,
# 			'entries':request.queryset,
# 		}