#coding:utf8
from rest_framework.views import APIView as _APIView

from pprint import pprint

class APIView(_APIView):

	def dispatch(self, request, *args, **kwargs):

		print('>>> dispatch')
		try:
			response = super().dispatch(request,*args,**kwargs)

			"""
	        此处是抛出错误格式
	        """
			if response.exception == True and hasattr(response.data['detail'],'code'):
				try:
					response.data['code'] = int(response.data['detail'].code)
				except:
					response.data['code'] = response.data['detail'].code

			pprint(response.__dict__)

			return response
		except Exception as exc:
			response = self.handle_exception(exc)



		self.response = self.finalize_response(request, response, *args, **kwargs)
		return self.response