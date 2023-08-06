#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

from wechat_utils.depends_framework.flask.schemas.parsers.mpapp.oauth import(
	Post as PostParser,
)


@ns.route('/oauth')
class oauth(Resource):

	@api.doc(parser=PostParser)
	@oauth
	def get(self):
		return redirect(request.redirect_url)
