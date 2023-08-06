#coding:utf8
from wechat_utils.depends_framework.flask.apis import api

Post = api.parser()
Post.add_argument('code', type=str, required=True)

Patch = api.parser()
Patch.add_argument('iv', type=str, required=True)
Patch.add_argument('decryptedData', type=str, required=True)

List = api.parser()
List.add_argument('page', type=int, default=0, required=False)
List.add_argument('page_size', type=int, default=10,  required=False)
List.add_argument('ordering', type=str, required=False)
List.add_argument('searching', type=str, required=False)
