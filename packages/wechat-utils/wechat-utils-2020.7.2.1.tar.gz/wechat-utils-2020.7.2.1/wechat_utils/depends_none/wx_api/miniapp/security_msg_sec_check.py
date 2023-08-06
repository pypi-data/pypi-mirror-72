#coding:utf8
import requests
import json

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def security_msg_sec_check(access_token,content):
	
	url_list = [
		'https://api.weixin.qq.com/wxa/msg_sec_check?',
		'access_token=',
		access_token,
	]

	url = "".join(url_list)

	data = {'content':content}
	_data = json.dumps(data,ensure_ascii=False).encode('utf-8')

	headers = {
		"Content-Type": "application/x-www-form-urlencoded", 
	}

	response = requests.post(url,headers=headers,data=_data)
	if response.status_code != 200:
		response.raise_for_status()
	if response.json()['errcode'] != 0:
		return False
	return True