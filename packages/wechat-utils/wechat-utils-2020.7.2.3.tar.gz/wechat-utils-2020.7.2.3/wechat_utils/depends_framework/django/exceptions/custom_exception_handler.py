#coding:utf8
from rest_framework.views import exception_handler

# 不需要使用这个，直接使用这个包的APIView也一样
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
