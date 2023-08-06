#coding:utf8
from ._imports_ import *
logger = logging.getLogger(__name__)

from wechat_utils.depends_framework.flask.schemas.parsers.mpapp.gateway import (
	Verification as VerificationParser
)


@ns.route('/gateway')
class Gateway(Resource):

	@api.doc(parser=VerificationParser)
	def get(self):

		payload = VerificationParser.parse_args()
		try:
			check_signature(payload['signature'], payload['timestamp'], payload['nonce'])
		except:
			logger.error(
				'Checking signature failed. payload %s Err: %s',
				payload,
				traceback.format_exc(),
			)
			return ''
		return payload['echostr']


	@api.doc(parser=VerificationParser)
	def post(self):

		try:
			mpauth = MpAuth()
			payload = mpauth.parse_message(request.data.decode('utf8'))
			logger.info('>>> received payload type: %s', type(payload))

			# 关注事件
			if isinstance(payload, EVENT_TYPES['subscribe']):
				logger.info('>>> sub source: %s', payload.source)
				logger.info(dict(payload._data))
				msg = '''
					<xml>
						<ToUserName><![CDATA[%s]]></ToUserName>
						<FromUserName><![CDATA[%s]]></FromUserName>
						<CreateTime>%s</CreateTime>
						<MsgType><![CDATA[text]]></MsgType>
						<Content><![CDATA[%s]]></Content>
					</xml>'''%(
						dict(payload._data)['FromUserName'],
						dict(payload._data)['ToUserName'],
						str(int(time.time())),
						"thanks for your subscribing",)

				logger.info(msg)

				return msg

			# 取消关注时间
			elif isinstance(payload, EVENT_TYPES['unsubscribe']):
				logger.info('>>>>unsub source: %s', payload.source)

		except:
			pass
		return ''



# @bp_wechat.route('/mpapp/gateway', methods=['GET'])
# @parse_with(VerificationParser)
# def gateway_get():
# 	payload = VerificationParser.parse_args()
# 	try:
# 		check_signature(payload['signature'], payload['timestamp'], payload['nonce'])
# 	except:
# 		logger.error(
# 			'Checking signature failed. payload %s Err: %s',
# 			payload,
# 			traceback.format_exc(),
# 		)
# 		return ''
# 	return payload['echostr']

# @bp_wechat.route('/mpapp/gateway', methods=['POST'])
# def gateway_post():
# 	try:

# 		mpauth = MpAuth()
# 		payload = mpauth.parse_message(request.data.decode('utf8'))
# 		logger.info('>>> received payload type: %s', type(payload))

# 		# 关注事件
# 		if isinstance(payload, EVENT_TYPES['subscribe']):
# 			logger.info('>>> sub source: %s', payload.source)
# 			logger.info(dict(payload._data))
# 			msg = '''
# 				<xml>
# 					<ToUserName><![CDATA[%s]]></ToUserName>
# 					<FromUserName><![CDATA[%s]]></FromUserName>
# 					<CreateTime>%s</CreateTime>
# 					<MsgType><![CDATA[text]]></MsgType>
# 					<Content><![CDATA[%s]]></Content>
# 				</xml>'''%(
# 					dict(payload._data)['FromUserName'],
# 					dict(payload._data)['ToUserName'],
# 					str(int(time.time())),
# 					"thanks for your subscribing",)

# 			logger.info(msg)

# 			return msg

# 		# 取消关注时间
# 		elif isinstance(payload, EVENT_TYPES['unsubscribe']):
# 			logger.info('>>>>unsub source: %s', payload.source)

# 	except:
# 			pass
# 	return ''
