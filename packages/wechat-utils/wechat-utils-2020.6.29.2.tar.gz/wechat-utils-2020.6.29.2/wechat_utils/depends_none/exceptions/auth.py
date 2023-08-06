# -*- coding: utf-8 -*-

class TokenExpiredException(Exception):
    pass
class TokenCorruptedException(Exception):
    pass
class TokenDecryptException(Exception):
    pass
class MissingTokenException(Exception):
    pass
class OpenidNotFoundException(Exception):
    pass
