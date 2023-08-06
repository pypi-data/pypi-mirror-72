wechat-utils
============

```python
from flask import Flask
from wechat_utils.adaptor.flask import WechatUtils

app = Flask(__name__)
WechatUtils(app)

if __name__ == '__main__':
  app.run()
```
