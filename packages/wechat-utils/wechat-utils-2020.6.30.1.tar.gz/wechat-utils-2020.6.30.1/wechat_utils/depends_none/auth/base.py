#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadTimeSignature, BadSignature

class BaseAuth:

	@staticmethod
	def decrypt(token,secret_key,salt,expires_in):
		cryption = Serializer(
			secret_key=secret_key,
			salt=salt,
			expires_in=expires_in
		)
		try:
			data = cryption.loads(token)
		except SignatureExpired:
			raise SignatureExpired
		except BadSignature:
			raise BadSignature
		except BadTimeSignature:
			raise BadTimeSignature
		except Exception as e:
		 raise e
		return data

	@staticmethod
	def encrypt(data,secret_key,salt,expires_in):
		cryption = Serializer(
			secret_key=secret_key,
			salt=salt,
			expires_in=expires_in
		)
		en_data = cryption.dumps(data)
		return en_data
