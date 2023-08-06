# coding:utf8
from rest_framework import serializers

class LoginDisserializer(serializers.Serializer):
	code = serializers.CharField(required=True)
