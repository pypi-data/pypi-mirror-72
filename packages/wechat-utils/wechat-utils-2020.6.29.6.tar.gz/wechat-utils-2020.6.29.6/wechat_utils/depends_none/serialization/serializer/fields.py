#coding:utf8
from flask_restplus.fields import String
import re
import os.path as op

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class File(String):
    def __init__(self, *args, **kwargs):
        self.pre = kwargs.pop('pre',None)
        self.before = kwargs.pop('before',None)
        self.after = kwargs.pop('after',None)
        super().__init__(*args, **kwargs)
    def format(self, value):

        if not value:
            return super().format(value)

        #
        # replace
        #
        if self.before and self.after:
            value = re.sub(self.before,self.after,value)

        #
        # pre
        #
        if self.pre:
            value = op.join(self.pre, value)
        return super().format(value)


class ListFile(String):
    def __init__(self, *args, **kwargs):
        self.pre = kwargs.pop('pre',None)
        self.before = kwargs.pop('before',None)
        self.after = kwargs.pop('after',None)
        super().__init__(*args, **kwargs)
    def format(self, value):

        if not value:
            return super().format(value)

        value = eval(value)

        for v,index in zip(value,range(0,len(value))):
            #
            # replace
            #
            if self.before and self.after:
                v = re.sub(self.before,self.after,v)

            #
            # pre
            #
            if self.pre:
                v = op.join(self.pre, v)

            value[index] = v

        return value