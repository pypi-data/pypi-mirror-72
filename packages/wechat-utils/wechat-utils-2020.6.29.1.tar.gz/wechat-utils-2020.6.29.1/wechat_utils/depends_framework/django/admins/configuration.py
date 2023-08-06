#coding:utf8

# Register your models here.
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import path

from wechat_utils.depends_framework.django.models.configuration import Configuration as ConfigurationModel
from wechat_utils.depends_framework.django.utils.common import POST_to_dict

class BaseConfigurationModelAdmin(admin.ModelAdmin):

	@csrf_exempt
	@never_cache
	def my_view(self, request):

		_data = {
			'appid':'xxx',
			'app_secret':'xxx',
			'app_category':'xxx',
			'mch_id':'xxx',
			'mch_secret':'xxx',

			'token_secret_key':'xxx',
			'token_salt':'xxx',
			'token_expiration':60*60*24*7,
			
			'redis_db':7,
			'redis_host':'xxx',
			'redis_port':6379,
			'redis_password':'xxx',
			'access_token_expiration':60*60*2,
			
			'oauth_redirect_url':'xxx',
			'post_oauth_redirect_url_default':'xxx',
			'oauth_redirect_token_expiration':60*60*24*365,
			'mp_token':'xxx',
		}

		# 查询数据库
		data = ConfigurationModel.objects.first()
		if data is not None:
			_data.update(data.to_dict())

		if request.method == 'GET':
			pass

		elif request.method == 'POST':

			__data = POST_to_dict(request.POST)
			if data:
				for key,value in __data.items():	
					setattr(data,key,value)
			else:
				data = ConfigurationModel(**__data)
			data.save()
			data = ConfigurationModel.objects.first()
			if data is not None:
				_data.update(data.to_dict())

		# ...
		context = dict(
			# Include common variables for rendering the admin template.
			self.admin_site.each_context(request),
			# Anything else you want in the context...
			data=_data,
		)
		return TemplateResponse(request, "configuration.html", context)

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			path('', self.admin_site.admin_view(self.my_view))
		]
		print(my_urls)
		return my_urls + urls

	def has_add_permission(self, request, obj=None):
		return False

#admin.site.register(ConfigurationModel,ConfigurationModelAdmin)
