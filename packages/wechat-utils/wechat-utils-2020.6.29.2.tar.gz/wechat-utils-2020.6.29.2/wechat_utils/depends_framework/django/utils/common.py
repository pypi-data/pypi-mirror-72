#coding:utf8

def POST_to_dict(POST):
	POST_dict = {}
	for key,value in dict(POST).items():
		POST_dict[key] = value[0]
	return POST_dict
