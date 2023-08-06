from django.db import models

# Create your models here.
class BaseUser(models.Model):
	appid = models.CharField(max_length=100,verbose_name="appid")
	app_secret = models.CharField(max_length=100,verbose_name="app_secret")
	app_category = models.CharField(max_length=100,verbose_name="app_category")
	mch_id = models.CharField(max_length=100,verbose_name="mch_id")
	mch_secret = models.CharField(max_length=100,verbose_name="mch_secret")
	token_secret_key = models.CharField(max_length=100,verbose_name="token_secret_key")
	token_salt = models.CharField(max_length=100,verbose_name="token_salt")
	token_expiration = models.CharField(max_length=100,verbose_name="token_expiration")
	redis_db = models.CharField(max_length=100,verbose_name="redis_db")
	redis_host = models.CharField(max_length=100,verbose_name="redis_host")
	redis_port = models.CharField(max_length=100,verbose_name="redis_port")
	redis_password = models.CharField(max_length=100,verbose_name="redis_password")
	access_token_expiration = models.CharField(max_length=100,verbose_name="access_token_expiration")
	oauth_redirect_url = models.CharField(max_length=100,verbose_name="oauth_redirect_url")
	post_oauth_redirect_url_default = models.CharField(max_length=100,verbose_name="post_oauth_redirect_url_default")
	mp_token = models.CharField(max_length=100,verbose_name="mp_token")

	def to_dict(self):
		return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])#type(self._meta.fields).__name__
	
	class Meta:
		abstract = True
		managed = False
		db_table = 'wechat_user'

class User(BaseUser):
	class Meta:
		managed = False
		db_table = 'wechat_user'
