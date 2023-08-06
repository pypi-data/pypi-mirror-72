#coding:utf8
from wechat_utils.depends_framework.flask.apis import api

Post = api.parser()
Post.add_argument('code', type=str, required=True)

