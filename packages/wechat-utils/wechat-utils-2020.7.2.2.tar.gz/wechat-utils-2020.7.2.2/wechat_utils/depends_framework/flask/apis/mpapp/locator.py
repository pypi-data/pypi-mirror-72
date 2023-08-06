#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

@ns.route('/locator')
class Locator(Resource):
	@api.doc()
	@locator
	def get(self):
		return redirect(request.redirect_url)
