# wxgbot

用于发送企业微信机器人消息，如文本、图片、文件
是对微信机器人的简单封装，其他可参考腾讯企业微信官网说明
https://work.weixin.qq.com/help?person_id=1&doc_id=13376&helpType=undefined

## 安装
可以直接 `pip` 安装
> pip install wxgbot

### 举例
```text
from wxgbot.send_msg import *
#test_bot是群机器人的key
test_bot = r"**********************************"
coment = r"牛逼哄哄带闪电！"
#发送文本消息
send_text(text = coment,bot = test_bot)      #bot是群机器人的key
#发送其他消息
send_markdown(text,bot)        #text是markdown语法的，
send_img(file_path,bot)        #file_path是文件路径
send_file(file_path,bot)
```


