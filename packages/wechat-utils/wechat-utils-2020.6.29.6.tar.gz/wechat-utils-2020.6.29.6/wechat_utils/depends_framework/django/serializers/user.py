#coding:utf8
from rest_framework import serializers

class Single(serializers.Serializer):
	code = serializers.Emailfield()