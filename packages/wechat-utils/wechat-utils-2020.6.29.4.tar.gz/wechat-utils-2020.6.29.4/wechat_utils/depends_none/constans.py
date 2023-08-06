#coding:utf8

class Keys(object):
    # string
    access_token = 'access_token'

    # zset, args: openid, member: formid, score: expires_at, needs to be cleaned up
    wechat_formid = 'wechat_formid:{}'

    # string with ttl; args: token, value: redirect url
    oauth_redirect_token = 'oauth:redirect:token:{}'

    throttle = 'throttle:{}'
