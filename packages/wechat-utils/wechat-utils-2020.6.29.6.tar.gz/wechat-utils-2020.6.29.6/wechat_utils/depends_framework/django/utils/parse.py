
def valid(Disserializer):
	def wrapper1(func):
		def wrapper2(*args,**kwargs):
			request = args[1]
			disser = Disserializer(data=request.data)
			disser.is_valid(raise_exception=True)
			return func(*args,**kwargs)
		return wrapper2
	return wrapper1
