# -*- coding: utf-8 -*-

import os
import binascii

class Random(object):
    @staticmethod
    def generate(length, prefix='', suffix=''):
        r= binascii.hexlify(os.urandom(length // 2)).decode('utf8')
        return ''.join((prefix, r, suffix))


sentinel = object()
