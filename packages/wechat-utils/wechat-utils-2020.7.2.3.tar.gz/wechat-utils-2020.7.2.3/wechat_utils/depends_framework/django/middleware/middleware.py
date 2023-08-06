#coding:utf8
from django.utils.deprecation import MiddlewareMixin
from wechat_utils.depends_none.meta import Singleton
from django.conf import settings

from wechat_utils.depends_database import WechatUtils

from pprint import pprint
import json

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class WechatUtilsMiddleware(MiddlewareMixin):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def process_response(self, request, response):

        print('>>> WechatUtilsMiddleware.process_response')

        """
        此处是抛出错误格式
        """
        if hasattr(response,'exception') and response.exception == True and hasattr(response.data['detail'],'code'):
            response.data['code'] = response.data['detail'].code

            # 方法1因返回时已经render过response，要想让这里的修改有效，需要手动在render一次
            response._is_rendered = False
            response.render()

            # 方法2
            #response.content = json.dumps(response.data)

        pprint(response.__dict__)
        return response


    def process_view(self, request, *args, **kwargs):

        print('>>> WechatUtilsMiddleware.process_view')

        # current_request
        WechatUtilsMiddleware.__instance = request

        # 初始化
        settings_database = settings.DATABASES.get('default')
        engine = settings_database.get('ENGINE').split('.')[-1]
        WechatUtils(
            db_type=engine,
            db_name=settings_database.get('NAME'),
            db_host=settings_database.get('HOST'),
            db_port=settings_database.get('PORT'),
            db_username=settings_database.get('USER'),
            db_password=settings_database.get('PASSWORD')
        )

    @classmethod
    def get_request(cls):
        return cls.__instance
