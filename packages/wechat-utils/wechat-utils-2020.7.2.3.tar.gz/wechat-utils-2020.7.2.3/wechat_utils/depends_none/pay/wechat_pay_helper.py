# -*-coding: utf-8 -*-



"""""""""""""""""""""""""""""""""""""""
pay.py
=============
* 小弟在此感谢前面两位大佬  :       goodspeed、zongxiao
* 搬运工                 :      黄旭辉
* 时间                   :        ２０１９年０６月１５日１５：１７：３７
what
----
wechat_pay.py is a framework-agnostic library for wechat pay.
why
---
no why
how
---
```python
from pay import WeixinPay
# 创建支付对象
wxpay = WeixinPay(
        appid=appid,                # 小程序id
        mch_id=mch_id,              # 商户号
        partner_key=partner_key     # 商户支付秘钥
    )
# 支付结果
unified_order = wxpay.unifiedorder(
    body=xxx,          # 支付备注
    openid=xxx,        #　支付用户openid
    total_fee=1,       #　支付价格
    notify_url=xxx,    # 支付结果通知接口
    out_trade_no=xxx   # 订单号(开发者定义)，支付结果通知时带上的参数
)
# 根据本次支付结果处理自己的支付流程，但最终支付结果要根据微信支付结果通知接口返回的结果为准
if unified_order['return_code'] == 'SUCCESS':
    pass
elif unified_order['err_code'] == 'PRDERPAID':
    pass
else:
    pass
```
"""""""""""""""""""""""""""""""""""""""















"""""""""""""""""""""""""""
支付加密部分
"""""""""""""""""""""""""""

# from __future__ import unicode_literals

"""
File:   client.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   2015-02-11
Description: Weixin helpers
"""

import sys
import datetime
from hashlib import sha1
from decimal import Decimal

import six
from six.moves import html_parser

PY2 = sys.version_info[0] == 2

_always_safe = (b'abcdefghijklmnopqrstuvwxyz'
                b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-+')

safe_char = _always_safe

error_dict = {
    'AppID 参数错误': {
        'errcode': 40013,
        'errmsg': 'invalid appid'
    }
}


if PY2:
    text_type = unicode
    iteritems = lambda d, *args, **kwargs: d.iteritems(*args, **kwargs)

    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.encode(charset, errors)
else:
    text_type = str
    iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))

    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.decode(charset, errors)


"""
The md5 and sha modules are deprecated since Python 2.5, replaced by the
hashlib module containing both hash algorithms. Here, we provide a common
interface to the md5 and sha constructors, preferring the hashlib module when
available.
"""

try:
    import hashlib
    md5_constructor = hashlib.md5
    md5_hmac = md5_constructor
    sha_constructor = hashlib.sha1
    sha_hmac = sha_constructor
except ImportError:
    import md5
    md5_constructor = md5.new
    md5_hmac = md5
    import sha
    sha_constructor = sha.new
    sha_hmac = sha


class Promise(object):
    """
    This is just a base class for the proxy class created in
    the closure of the lazy function. It can be used to recognize
    promises in code.
    """
    pass


class _UnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj,
                                              type(self.obj))


def smart_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a text object representing 's' -- unicode on Python 2 and str on
    Python 3. Treats bytestrings using the 'encoding' codec.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, Promise):
        # The input is the result of a gettext_lazy() call.
        return s
    return force_text(s, encoding, strings_only, errors)


_PROTECTED_TYPES = six.integer_types + (type(None), float, Decimal,
                                        datetime.datetime, datetime.date,
                                        datetime.time)


def is_protected_type(obj):
    """Determine if the object instance is of a protected type.
    Objects of protected types are preserved as-is when passed to
    force_text(strings_only=True).
    """
    return isinstance(obj, _PROTECTED_TYPES)


def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if issubclass(type(s), six.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not issubclass(type(s), six.string_types):
            if six.PY3:
                if isinstance(s, bytes):
                    s = six.text_type(s, encoding, errors)
                else:
                    s = six.text_type(s)
            elif hasattr(s, '__unicode__'):
                s = six.text_type(s)
            else:
                s = six.text_type(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise _UnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join(force_text(arg, encoding, strings_only, errors)
                         for arg in s)
    return s


def smart_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, Promise):
        # The input is the result of a gettext_lazy() call.
        return s
    return force_bytes(s, encoding, strings_only, errors)


def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and is_protected_type(s):
        return s
    if isinstance(s, Promise):
        return six.text_type(s).encode(encoding, errors)
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join(force_bytes(arg, encoding,
                                             strings_only, errors)
                                 for arg in s)
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)

smart_str = smart_text
force_str = force_text
smart_unicode = smart_text
force_unicode = force_text

# if six.PY3:
#     smart_str = smart_text
#     force_str = force_text
# else:
#     smart_str = smart_bytes
#     force_str = force_bytes
#     # backwards compatibility for Python 2
#     smart_unicode = smart_text
#     force_unicode = force_text

smart_str.__doc__ = """
Apply smart_text in Python 3 and smart_bytes in Python 2.
This is suitable for writing to sys.stdout (for instance).
"""

force_str.__doc__ = """
Apply force_text in Python 3 and force_bytes in Python 2.
"""


def genarate_js_signature(params):
    keys = params.keys()
    keys.sort()
    params_str = b''
    for key in keys:
        params_str += b'%s=%s&' % (smart_str(key), smart_str(params[key]))
    params_str = params_str[:-1]
    return sha1(params_str).hexdigest()


def genarate_signature(params):
    sorted_params = sorted([v for k, v in params.items()])
    params_str = smart_str(''.join(sorted_params))
    return sha1(str(params_str).encode('utf-8')).hexdigest()


def get_encoding(html=None, headers=None):
    try:
        import chardet
        if html:
            encoding = chardet.detect(html).get('encoding')
            return encoding
    except ImportError:
        pass
    if headers:
        content_type = headers.get('content-type')
        try:
            encoding = content_type.split(' ')[1].split('=')[1]
            return encoding
        except IndexError:
            pass


def iter_multi_items(mapping):
    """
    Iterates over the items of a mapping yielding keys and values
    without dropping any from more complex structures.
    """
    if isinstance(mapping, dict):
        for key, value in iteritems(mapping):
            if isinstance(value, (tuple, list)):
                for value in value:
                    yield key, value
            else:
                yield key, value
    else:
        for item in mapping:
            yield item


def url_quote(string, charset='utf-8', errors='strict', safe='/:', unsafe=''):
    """
    URL encode a single string with a given encoding.
    :param s: the string to quote.
    :param charset: the charset to be used.
    :param safe: an optional sequence of safe characters.
    :param unsafe: an optional sequence of unsafe characters.
    .. versionadded:: 0.9.2
    The `unsafe` parameter was added.
    """
    if not isinstance(string, (text_type, bytes, bytearray)):
        string = text_type(string)
    if isinstance(string, text_type):
        string = string.encode(charset, errors)
    if isinstance(safe, text_type):
        safe = safe.encode(charset, errors)
    if isinstance(unsafe, text_type):
        unsafe = unsafe.encode(charset, errors)
    safe = frozenset(bytearray(safe) + _always_safe) - frozenset(bytearray(unsafe))
    rv = bytearray()
    for char in bytearray(string):
        if char in safe:
            rv.append(char)
        else:
            rv.extend(('%%%02X' % char).encode('ascii'))
    return to_native(bytes(rv))


def url_quote_plus(string, charset='utf-8', errors='strict', safe=''):
    return url_quote(string, charset, errors, safe + ' ', '+').replace(' ', '+')


def _url_encode_impl(obj, charset, encode_keys, sort, key):
    iterable = iter_multi_items(obj)
    if sort:
        iterable = sorted(iterable, key=key)
    for key, value in iterable:
        if value is None:
            continue
        if not isinstance(key, bytes):
            key = text_type(key).encode(charset)
        if not isinstance(value, bytes):
            value = text_type(value).encode(charset)
        yield url_quote_plus(key) + '=' + url_quote_plus(value)


def url_encode(obj, charset='utf-8', encode_keys=False, sort=False, key=None,
               separator=b'&'):
    separator = to_native(separator, 'ascii')
    return separator.join(_url_encode_impl(obj, charset, encode_keys, sort, key))


class WeixiErrorParser(html_parser.HTMLParser):

    def __init__(self):
        html_parser.HTMLParser.__init__(self)
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag != 'h4':
            return
        if self.recording:
            self.recording += 1
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'h4' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)


def error_parser(error_html, encoding='gbk'):
    html = text_type(error_html, encoding or 'gbk')
    error_parser = WeixiErrorParser()
    error_parser.feed(html)
    if error_parser.data:
        return error_dict.get(error_parser.data[0], None)


def validate_xml(xml):
    """
    使用lxml.etree.parse 检测xml是否符合语法规范
    """
    from lxml import etree
    try:
        return etree.parse(xml)
    except etree.XMLSyntaxError:
        return False





"""""""""""""""""""""""""""
支付业务部分
"""""""""""""""""""""""""""



'''
Created on 2016-05-01
微信接口
@author: zongxiao
'''
import logging
_logger = logging.getLogger(__name__)

import time
import random
import string
import socket

import requests
import xmltodict

#from .pay_helper import smart_str, smart_unicode, md5_constructor as md5

TIMEOUT = 5

try:
    SPBILL_CREATE_IP = socket.gethostbyname(socket.gethostname())
except:
    SPBILL_CREATE_IP = '127.0.0.1'






#
# 签名
#
def build_pay_sign(app_id, nonce_str, prepay_id, time_stamp, key, signType='MD5'):
    """
    :param app_id:
    :param nonce_str:
    :param prepay_id:
    :param time_stamp:
    :param key:
    :param signType:
    :return:
    """
    sign = 'appId={app_id}' \
        '&nonceStr={nonce_str}' \
        '&package=prepay_id={prepay_id}' \
        '&signType={signType}' \
        '&timeStamp={time_stamp}' \
        '&key={key}'.format(
            app_id=app_id, 
            nonce_str=nonce_str, 
            prepay_id=prepay_id,
            time_stamp=time_stamp, 
            key=key, 
            signType=signType
        )
    return md5_constructor(bytes(sign, encoding = "utf8")).hexdigest().upper()







































def generate_nonce_str(length=32):
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(length))


def params_encoding(params, charset='utf-8'):
    newparams = {}
    for k, v in params.items():
        newparams[k] = smart_unicode(v)
    return newparams


def params_filter(
    params, delimiter='&', charset='utf-8',
    excludes=['sign', 'sign_type']):
    ks = list(params.keys())
    ks.sort()
    newparams = {}
    prestr = ''
    if params.get('input_charset', None):
        charset = params['input_charset']
    for k in ks:
        v = params[k]
        k = smart_str(k, charset)
        if k not in excludes and v != '':
            newparams[k] = smart_str(v, charset)
            prestr += '%s=%s%s' % (k, newparams[k], delimiter)
    prestr = prestr[:-1]
    return newparams, prestr


# 生成签名结果
def build_mysign(prestr, key=None, sign_type='MD5'):
    if sign_type == 'MD5':
        prestr += '&key=%s' % str(key)
        return md5_constructor(bytes(prestr, encoding = "utf8")).hexdigest().upper()
    return ''




class WeixinPay(object):

    BASE_URL = 'https://api.mch.weixin.qq.com/'
    PAY_SOURCE = 'weixin'

    def __init__(self, appid, mch_id, *args, **kwargs):
        """
        微信支付接口
        :param appid: 微信公众号 appid
        :param api_key: 商户 key
        :param mch_id: 商户号
        :param sub_mch_id: 可选，子商户号，受理模式下必填
        :param mch_cert: 可选，商户证书路径 申请退款必须
        :param mch_key: 可选，商户证书私钥路径 申请退款必选
        :param notify_url: 可选 接收微信支付异步通知回调地址 统一下单接口必选
        :param partner_key: 商户支付Key
        """
        self.appid = appid
        self.mch_id = mch_id
        self.mch_cert = kwargs.get('mch_cert')
        self.mch_key = kwargs.get('mch_key')
        self.notify_url = kwargs.get('notify_url')
        self.partner_key = kwargs.get('partner_key')
        self.time_stamp = str(int(time.time()))

    def _full_url(self, path):
        return '%s%s' % (self.BASE_URL, path)

    def get_base_params(self):
        params = {
            'appid': self.appid,                    # 公众账号ID
            'mch_id': self.mch_id,                  # 商户号
            'nonce_str': generate_nonce_str(),      # 随机字符串
        }
        return params

    def prepare_request(self, method, path, params):
        kwargs = {}
        _params = self.get_base_params()
        params.update(_params)
        newparams, prestr = params_filter(params)
        sign = build_mysign(prestr, self.partner_key)
        # 将内容转化为unicode xmltodict 只支持unicode
        newparams = params_encoding(newparams)
        newparams['sign'] = sign
        xml_dict = {'xml': newparams}
        kwargs['data'] = smart_str(xmltodict.unparse(xml_dict))
        url = self._full_url(path)
        if self.mch_cert and self.mch_key:
            kwargs['cert'] = (self.mch_cert, self.mch_key)
        return method, url, kwargs

    # 统一下单
    # https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    def unifiedorder(self, body='', out_trade_no='', total_fee='', openid='',
        detail='', attach='', time_start='', time_expire='',
        goods_tag='', product_id='', limit_pay='', device_info='',
        fee_type='CNY', spbill_create_ip=SPBILL_CREATE_IP,
        trade_type='JSAPI', notify_url=''
    ):
        """
        统一下单接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
        :param trade_type: 交易类型，取值如下：JSAPI，NATIVE，APP，WAP, MWEB
        :param body: 商品描述
        :param total_fee: 总金额，单位分
        :param notify_url: 接收微信支付异步通知回调地址
        :param client_ip: 可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        :param openid: 可选，用户在商户appid下的唯一标识。trade_type=JSAPI，此参数必传
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param detail: 可选，商品详情
        :param attach: 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param fee_type: 可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param time_start: 可选，订单生成时间，默认为当前时间
        :param time_expire: 可选，订单失效时间，默认为订单生成时间后两小时
        :param goods_tag: 可选，商品标记，代金券或立减优惠功能的参数
        :param product_id: 可选，trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :param spbill_create_ip: 调用接口的机器Ip地址
        :param limit_pay: 可选，指定支付方式，no_credit--指定不能使用信用卡支付
        :return: 返回的结果数据
        """

        _notify_url = notify_url or self.notify_url
        path = 'pay/unifiedorder'
        params = dict(
            body=body,                          # 商品描述
            total_fee=total_fee,                # 总金额
            out_trade_no=out_trade_no,          # 商户订单号
            openid=openid,                      # 用户支付公众号openid(jsapi必须)
            fee_type=fee_type,                  # 货币类型
            spbill_create_ip=spbill_create_ip,  # 终端IP
            notify_url=_notify_url,             # 通知地址
            trade_type=trade_type,              # 交易类型
            device_info=device_info,            # 设备号
            detail=detail,                      # 商品详情
            attach=attach,                      # 附加数据
            time_start=time_start,              # 交易起始时间
            time_expire=time_expire,            # 交易结束时间
            goods_tag=goods_tag,                # 商品标记
            product_id=product_id,              # 商品ID
            limit_pay=limit_pay,                # 指定支付方式
        )
        _logger.error(params)
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def order_query(self, transaction_id='', out_trade_no=''):
        """
        订单查询接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param transaction_id: 可选，微信订单号 和out_trade_no 二选一
        :return: 返回的结果数据
        -----
        trade_state 订单状态
        SUCCESS—支付成功
        REFUND—转入退款
        NOTPAY—未支付
        CLOSED—已关闭
        REVOKED—已撤销（刷卡支付）
        USERPAYING--用户支付中
        PAYERROR--支付失败(其他原因，如银行返回失败)
        """
        path = 'pay/orderquery'
        params = dict(
            transaction_id=transaction_id,
            out_trade_no=out_trade_no
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def order_close(self, out_trade_no):
        """
        订单关闭接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_3
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :return: 返回的结果数据
        """
        path = 'pay/closeorder'
        params = dict(
            out_trade_no=out_trade_no
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def refund(self, out_refund_no, total_fee, refund_fee, op_user_id,
        out_trade_no='', transaction_id='',
        device_info='', refund_fee_type='CNY'
    ):
        """
        退款查询接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_4
        :param out_refund_no: 商户退款单号
        :param total_fee: 总金额
        :param refund_fee: 退款金额
        :param op_user_id: 操作员帐号, 默认为商户号
        :param transaction_id: 可选，商户订单号，默认自动生成
        :param out_trade_no: 可选，微信订单号 以上两个二选一
        :param refund_fee_type: 可选 货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :return: 返回的结果数据
        """
        path = 'secapi/pay/refund'
        params = dict(
            out_refund_no=out_refund_no,
            total_fee=total_fee,
            refund_fee=refund_fee,
            op_user_id=op_user_id,
            transaction_id=transaction_id,
            out_trade_no=out_trade_no,
            refund_fee_type=refund_fee_type,
            device_info=device_info
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def refundquery(self, out_trade_no='', transaction_id='',
        out_refund_no='', refund_id='', device_info=''):
        """
        退款查询接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_5
        :param transaction_id: 可选，微信订单号
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param out_refund_no: 可选，商户退款单号
        :param refund_id: 可选，微信退款单号 以上四个四选一
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :return: 返回的结果数据
        ----------
        退款状态：
        SUCCESS     退款成功
        FAIL        退款失败
        PROCESSING  退款处理中
        NOTSURE     未确定，需要商户原退款单号重新发起
        CHANGE      转入代发，退款到银行发现用户的卡作废或者冻结了，
                    导致原路退款银行卡失败，资金回流到商户的现金帐号，
                    需要商户人工干预，通过线下或者财付通转账的方式进行退款。
        """
        path = 'pay/refundquery'
        params = dict(
            out_trade_no=out_trade_no,
            transaction_id=transaction_id,
            out_refund_no=out_refund_no,
            refund_id=refund_id,
            device_info=device_info,
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def make_request(self, method, url, kwargs):
        req = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        # xml to dict
        result = xmltodict.parse(req.content)
        # 只需要返回数据
        return result.get('xml')





