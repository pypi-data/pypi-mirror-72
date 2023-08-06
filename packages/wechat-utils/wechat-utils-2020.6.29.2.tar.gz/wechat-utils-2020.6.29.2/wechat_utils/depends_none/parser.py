# -*- coding: utf-8 -*-



from flask import request
from functools import wraps
from marshmallow import Schema, EXCLUDE

from .common import sentinel

from wechat_utils.depends_none.exceptions.parse import ParseException

def parse_with(mallow):
    assert issubclass(mallow, Schema)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self = args[0]
            args = args[1:]

            self.parser = Parser(mallow)
            self.parser.payload = kwargs
            if request.endpoint_arguments and isinstance(request.endpoint_arguments, dict):
                kwargs = request.endpoint_arguments
            else:
                kwargs = {}
            return f(self, **kwargs)
        return wrapper
    return decorator


class Parser(object):
    def __init__(self, schema_cls):
        self.schema_cls = schema_cls
        self.schema = schema_cls()
        self._payload = None
        self._parsed = sentinel

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, val):
        if self._payload != val:
            self._parsed = sentinel
            self._payload = val

    def parse(self, payload=None):
        if payload is not None:
            self.payload = payload
        if self._parsed is sentinel:
            self._parsed = self.schema.load(self.payload)
        return self._parsed


class ParserBase(Schema):
    class Meta:
        unknown = EXCLUDE

    def handle_error(self, exc, data):
        raise ParseException(
            errcode=991001,
            message=exc.messages,
        )
