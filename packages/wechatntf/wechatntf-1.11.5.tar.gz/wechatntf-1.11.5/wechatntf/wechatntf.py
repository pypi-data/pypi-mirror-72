# coding="utf-8"

import requests
import json
import configparser
import time


class wechatntf():
    def __init__(self):
        self.url = "http://wxpusher.zjiecode.com/api/send/message"
        self.headers = {
            "Content-Type": "application/json"
        }

    def wechatsend(self, summary="", content="", contentType=1):
        """
        summary为消息概览，content为消息内容，
        contentType为消息类型：
        1表示文字
        2表示html(只发送body标签内部的数据即可，不包括body标签)
        3表示markdown
        """
        self.data = {
            "summary": summary,
            "content": content,
            "contentType": contentType
        }
        config = configparser.ConfigParser()
        config.read('/usr/local/wechatntf_config.ini')  # 读取配置文件信息

        self.data["appToken"] = config.get('DEFAULT', 'appToken')
        # 配置文件获取到的[424] 为str形式，转换为python数据格式，需loads
        self.data["topicIds"] = json.loads(config.get('DEFAULT', 'topicIds'))
        self.data = json.dumps(self.data)
        i = 0
        # 如果数据发送超时，则进行5次发送尝试
        while i < 5:
            try:
                requests.post(url=self.url, headers=self.headers, data=self.data,
                              timeout=5).content.decode()
                break
            except Exception as ret:
                time.sleep(0.5)
                i += 1


if __name__ == '__main__':
    a = wechatntf()
    res = a.wechatsend(content="这是一条测试消息")
