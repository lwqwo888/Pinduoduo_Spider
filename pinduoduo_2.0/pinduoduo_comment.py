# coding=utf-8
import os
import re
import time
import json
import random
import jsonpath
import requests
import linecache
from lxml import etree
# from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Comment(object):
    def __init__(self):
        # self.headers = ""
        # 代理服务器
        proxyHost = "n10.t.16yun.cn"
        proxyPort = "6442"

        # 代理隧道验证信息
        proxyUser = "16SBYYUY"
        proxyPass = "658666"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        print proxyMeta
        self.proxy = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        self.srequest = requests.Session()

    def change_ua(self):
        tunnel = random.randint(1, 1036)
        # print tunnel
        user_agent = linecache.getline('1000ua-pc.log', tunnel)
        user_agent = user_agent.strip().replace('\n', '').replace('\r', '')
        # print user_agent
        # 请求头携带Host会导致无法访问数据
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "goods=goods_abY0pR; api_uid=rBQh3Vqd/BEEgl0IBpdgAg==; ua=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F63.0.3239.132%20Safari%2F537.36; webp=1; msec=86400000; rec_list=rec_list_OW96ZF",
            # "Host": "mobile.yangkeduo.com",
            "Upgrade-Insecure-Requests": "1",
            # 'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'user-agent': user_agent,
        }

    def comment_json(self):
        self.change_ua()
        url = 'http://apiv3.yangkeduo.com/reviews/9193910/list?picture=1&page=1&size=20'
        # url = "http://apiv3.yangkeduo.com/reviews/9193910/list?picture=1&page=12&size=20&pdduid=0"
        res = requests.get(url, headers=self.headers, proxies=self.proxy).text
        # print res
        json_data = json.loads(res)
        json_obj = jsonpath.jsonpath(json_data, expr='$..data[*].comment')
        time_obj = jsonpath.jsonpath(json_data, expr='$..data[*].time')
        comment_li = []  # 评论内容列表,不包含追评
        time_li = [time.strftime("%Y-%m-%d", time.localtime(i)) for i in time_obj]  # 评论时间列表,不包含追评
        j = 1
        for i in json_obj:
            if i == "":
                i = "此用户未填写文字评论"
            comment_li.append(i)

        # 购买信息(买的什么颜色,尺码一类的)
        shopping_info_list = []
        shopping_info_obj = jsonpath.jsonpath(json_data, expr='$..data[*].specs')
        for i in shopping_info_obj:
            # print i
            re_key_obj = re.compile(r'"spec_key":"(.*?)",', re.S)
            re_value_obj = re.compile(r'"spec_value":"(.*?)"', re.S)
            shopping_info_key = re_key_obj.findall(i)
            shopping_info_value = re_value_obj.findall(i)
            shopping_info_li = [i for i in zip(shopping_info_key, shopping_info_value)]
            shopping_info_str = ""
            for i, j in shopping_info_li:
                str = "%s : %s " % (i, j)
                shopping_info_str = shopping_info_str + str
            shopping_info_list.append(shopping_info_str)

        shopping_info_big_list = [i for i in zip(time_li, comment_li, shopping_info_list)]
        for x, y, z in shopping_info_big_list:
            print "%s --> %s --> %s" % (x, z, y)


if __name__ == '__main__':
    c = Comment()
    c.comment_json()