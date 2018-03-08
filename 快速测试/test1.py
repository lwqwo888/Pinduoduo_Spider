# coding=utf-8
import time
import json
import jsonpath
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'authority': 'detail.tmall.com',
    'method': 'GET',
    'scheme': "https",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "max-age=0",
    'cookie': "cna=XTyQEoI1uE4CAXBfh3IMFSpJ; cq=ccp%3D1; t=4d814acaeff7745d2b1df5c531cb7227; _tb_token_=3eb56ee77e988; cookie2=17B3F5F8A0D9CB4142FFBB0733EC948B; pnm_cku822=098%23E1hvApvUvbpvjQCkvvvvvjiPPL5wljtVP25hgjivPmPy1jYRRsdvzjiRR2z91jQPvpvhvvvvvvhCvvOvUvvvphvEvpCWh8%2Flvvw0zj7OD40OwoAQD7zheutYvtxr1RoKHkx%2F1RBlYb8rwZBleExreE9aWXxr1noK5FtffwLyaB4AVAdyaNoxdX3z8ikxfwoOddyCvm9vvvvvphvvvvvv96Cvpv9hvvm2phCvhRvvvUnvphvppvvv96CvpCCvkphvC99vvOC0B4yCvv9vvUvQud1yMsyCvvpvvvvviQhvCvvv9UU%3D; isg=ArOzZnnX7QJos6HBeuocdKfGQrcdQCLrPU38GWVQTFIJZNMG7bjX-hH2aqJx",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    # 'user-agent': user_agent,
}
url = "http://yangkeduo.com/goods.html?goods_id=144304661"
res = requests.get(url, headers=headers).text
html = etree.HTML(res)
js_data = html.xpath("/html/body/script[2]/text()")
# 截取json数据
json_data = js_data[0][25:-6]
# print json_data
json_res = json.loads(json_data)

# 商品ID
goods_id_li = jsonpath.jsonpath(json_res, expr='$.goods.goodsID')
print goods_id_li[0]
# 商品标题
title_li = jsonpath.jsonpath(json_res, expr='$.goods.goodsName')
print title_li[0]
# 商品副标题
# TODO

# 用于提取商品属性信息的所有json  Product_attribute_info > pai
pai_li = jsonpath.jsonpath(json_res, expr='$.goods.skus[*].specs')

# 商品属性分类  Product_attribute_classification > pac
pac = jsonpath.jsonpath(pai_li[0], expr='$..spec_key')

for i in pac:
    print i

# 商品属性详细分类
pac_count = len(pac)  # 商品属性分类数量   pac_count > pc
pac_combination_count = len(pai_li)  # 商品属性分类组合数量   pac_combination_count > pcc

index_pc = 0
while index_pc < pac_count:

    index_pcc = 0
    tmp_list = []
    pac_name = pac[index_pc]
    while index_pcc < pac_combination_count:
        attribute_value = jsonpath.jsonpath(pai_li[index_pcc][index_pc], expr='$..spec_value')
        index_pcc += 1
        tmp_list.append(attribute_value[0])
        addr_to = list(set(tmp_list))
        addr_to.sort(key=tmp_list.index)
    print pac_name, ','.join(addr_to)
    index_pc += 1


# 商品分类组合
index = 0
while index < pac_combination_count:
    info_li = jsonpath.jsonpath(pai_li[index], expr='$..spec_value')
    print '|'.join(info_li)
    index += 1


# 产品参数
goods_info = jsonpath.jsonpath(json_res, expr='$.goods.goodsDesc')
print goods_info[0]



