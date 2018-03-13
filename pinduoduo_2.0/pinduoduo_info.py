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
from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Pinduoduo_Spider(object):
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
            "Connection": "keep-alive",
            "Cookie": "goods=goods_abY0pR; api_uid=rBQh3Vqd/BEEgl0IBpdgAg==; ua=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F63.0.3239.132%20Safari%2F537.36; webp=1; msec=86400000; rec_list=rec_list_OW96ZF",
            # "Upgrade-Insecure-Requests": "1",
            # 'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'user-agent': user_agent,
        }
        
    def create_json(self, id,  category_name, dir_name):
        info_path = "pinduoduo_multimedia_datas/%s/%s/%s/商品详情/" % (category_name, dir_name, id)
        if (not (os.path.exists(info_path))):
            os.makedirs(info_path)
        # 商品详情大字典, 有序字典(父)
        product_details_dict = OrderedDict()
        # 商品属性详细分类字典, 有序字典(子)
        detailed_class_dict = OrderedDict()
        # 商品分类组合字典, 有序字典(子)
        category_combination_dict = OrderedDict()
        # 库存量字典, 有序字典 TODO
        # inventory_dict = OrderedDict()
        # 颜色识别码字典, 有序字典 TODO
        # color_code_dict = OrderedDict()

        # 商品ID
        goods_id_li = jsonpath.jsonpath(self.json_res, expr='$.goods.goodsID')
        id = goods_id_li[0]
        product_details_dict["id"] = id

        # 商品标题
        title_li = jsonpath.jsonpath(self.json_res, expr='$.goods.goodsName')
        title = title_li[0]
        product_details_dict["商品标题"] = title

        # 商品副标题
        # TODO
        subtitle = jsonpath.jsonpath(self.json_res, expr='$.goods.sales')
        product_details_dict["副标题"] = "已售%s件" % subtitle[0]

        # 用于提取商品属性信息的所有json  Product_attribute_info > pai
        pai_li = jsonpath.jsonpath(self.json_res, expr='$.goods.skus[*].specs')
        if pai_li[0]:
            # 商品属性分类  Product_attribute_classification > pac
            pac = jsonpath.jsonpath(pai_li[0], expr='$..spec_key')
            product_details_dict['商品属性分类'] = pac
            # for i in pac:
            #     print i

            # 商品属性详细分类
            pac_count = len(pac)  # 商品属性分类数量   pac_count > pc
            pac_combination_count = len(pai_li)  # 商品属性分类组合数量   pac_combination_count > pcc

            index_pc = 0
            while index_pc < pac_count:

                index_pcc = 0
                addr_to = []
                tmp_list = []
                pac_name = pac[index_pc]
                while index_pcc < pac_combination_count:
                    attribute_value = jsonpath.jsonpath(pai_li[index_pcc][index_pc], expr='$..spec_value')
                    index_pcc += 1
                    tmp_list.append(attribute_value[0])
                    addr_to = list(set(tmp_list))
                    addr_to.sort(key=tmp_list.index)
                detailed_class_dict[pac_name] = addr_to
                index_pc += 1

            # 商品分类组合
            index = 0
            stock_li = jsonpath.jsonpath(self.json_res, expr='$.goods.skus[*].quantity')  # 所有组合库存数量
            while index < pac_combination_count:
                info_li = jsonpath.jsonpath(pai_li[index], expr='$..spec_value')
                if stock_li[index] > 0:  # 只展示有货商品组合,如需展示所有组合去掉if即可 stock_li[index]为库存数量
                    category_combination_dict['|'.join(info_li)] = "co" + str(index+1)
                index += 1
                # print stock_li
        else:
            product_details_dict['商品属性分类'] = []
            detailed_class_dict = {}
            category_combination_dict = {}
            with open('空白json拼多多ID.txt', 'a') as f:
                f.write(str(id) + '\r\n')

        # 产品参数
        goods_info_li = jsonpath.jsonpath(self.json_res, expr='$.goods.goodsDesc')
        goods_info_li = goods_info_li[0].replace("\n", "").replace("\r", "").replace('\\','\\\\').replace('"', '\\"')
        goods_info = goods_info_li
        # print goods_info
        product_details_dict["商品属性详细分类"] = detailed_class_dict
        product_details_dict["商品分类组合"] = category_combination_dict
        product_details_dict["产品参数"] = goods_info
        j = json.dumps(product_details_dict).decode('unicode-escape')
        with open(info_path + '拼多多产品参数.txt', 'a') as f:
            f.write(j)

    # 解析图片地址
    def analysis_url(self, id, category_name, dir_name):
        # 轮播图
        turn_img_li = jsonpath.jsonpath(self.json_res, expr='$.goods.topGallery')
        # for i in turn_img_li[0]:
        #     print i
        # print ''
        length = len(turn_img_li[0])
        self.download_img(length, turn_img_li[0], id, "turn", category_name, dir_name)

        # 细节图
        detail_img_li = jsonpath.jsonpath(self.json_res, expr='$.goods.detailGallery[*].url')
        # for i in detail_img_li:
        #     print i
        # print ''
        length = len(detail_img_li)
        self.download_img(length, detail_img_li, id, "detail", category_name, dir_name)

        # 颜色图
        color_img_li = jsonpath.jsonpath(self.json_res, expr='$.goods.skus[*].thumbUrl')
        # for i in color_img_li:
        #     print i
        length = len(color_img_li)
        color_list = 1
        self.download_img(length, color_img_li, id, "color", category_name, dir_name, color_list)

    # path = "pinduoduo_multimedia_datas/%s/%s/%s/img/%s/" % (category_name, dir_name, id, doc_name)
    # def download_img(self, list_length, list, id, name, category_name, dir_name, *args):
    #
    #     k = 0
    #     while k < list_length:
    #         img_url1 = list[k].replace("http", "https")
    #         img_url_obj = re.compile(r'(https://.*?\.(jpg|png|jpeg|gif))', re.S)
    #         img_url = img_url_obj.findall(img_url1)[0][0]
    #         # print img_url, "--------------"
    #         # 图片文件夹名
    #         doc_name = name + '_img'
    #
    #         path = "pinduoduo_multimedia_datas/%s/%s/%s/img/%s/" % (category_name, dir_name, id, doc_name)
    #         if (not (os.path.exists(path))):
    #             os.makedirs(path)
    #
    #         # 后缀名
    #         format = img_url[-5:]
    #         # print format
    #         if args:
    #             img_name = id + '_co' + str(k + 1)
    #         else:
    #             img_name = id + "_" + name + "_" + str(k + 1)
    #         print "正在请求　%s" % name
    #
    #         self.change_ua()
    #
    #         response = self.srequest.get(img_url, headers=self.headers, proxies=self.proxy)
    #         self.resp_code = response.status_code
    #         if self.resp_code == 200:
    #             data = response.content
    #
    #             print "正在保存　%s" % img_name
    #             with open(path + img_name + format, 'wb') as f:
    #                 # print '******************',res
    #                 f.write(data)
    #         else:
    #             print "erro"
    #         # --------------------------------------------------------------------------------------
    #         print '共%s个　第%s个url: %s' % (list_length, k + 1, img_url)
    #         time.sleep(0)
    #
    #         k += 1
    #     print "[INFO]: %s商品%s图片已抓取完成！！\n" % (id, name)

    def download_img(self, list_length, list, id, name, category_name, dir_name, *args):
        k = 0
        while k < list_length:
            data = ''
            self.resp_code = ""
            img_url1 = list[k].replace("http", "https")
            img_url_obj = re.compile(r'(https://.*?\.(jpg|png|jpeg|gif))', re.S)
            img_url = img_url_obj.findall(img_url1)[0][0]
            # print img_url, "--------------"
            # 图片文件夹名
            doc_name = name + '_img'

            path = "pinduoduo_multimedia_datas/%s/%s/%s/img/%s/" % (category_name, dir_name, id, doc_name)
            if (not (os.path.exists(path))):
                os.makedirs(path)

            # 后缀名
            format = img_url[-5:]
            # print format
            # print id, name, category_name, dir_name, '******************'
            if args:
                img_name = id + '_co' + str(k + 1)
            else:
                img_name = id + "_" + name + "_" + str(k + 1)
            print "正在请求　%s" % name

            self.change_ua()

            try:
                time.sleep(0.2)
                response = self.srequest.get(img_url, headers=self.headers, proxies=self.proxy)
                self.resp_code = response.status_code
                if self.resp_code == 200:
                    data = response.content

            except Exception as e:
                print '数据请求失败...正在重试......', e
                with open('request.log', 'a') as f:
                    f.write('%s [代理]请求失败(%s) %s - %s\n' % (img_url, self.resp_code, id, time.ctime()))
                # # global NETWORK_STATUS
                NETWORK_STATUS = False  # 请求超时改变状态

                if NETWORK_STATUS == False:
                    #     '请求超时'
                    for i in range(1, 11):
                        time.sleep(0.3)
                        print '请求失败，第%s次重复请求' % i
                        if i == 5:
                            print "[INFO]: 代理睡眠中......"
                            time.sleep(10)
                        if i == 7:
                            print "[INFO]: 代理睡眠中......"
                            time.sleep(30)
                        if i == 9:
                            print "[INFO]: 代理睡眠中......"
                            time.sleep(60)
                        self.change_ua()

                        try:
                            response = requests.get(img_url, headers=self.headers, proxies=self.proxy)
                            self.resp_code = response.status_code
                            if self.resp_code == 200:
                                data = response.content
                                with open('request.log', 'a') as f:
                                    f.write('%s 重新请求成功%s - %s\n' % (img_url, id, time.ctime()))
                                print ('[INFO]:重发请求成功!!!!!!!!!!')
                                break
                        except:
                            with open('request.log', 'a') as f:
                                f.write('%s 重新请求失败, %s  继续重试...%s - %s\n' % (img_url, self.resp_code, id, time.ctime()))
                            print ('[INFO]:重发请求失败!!!!!!!!!!')
                            print '第%s次重复请求失败%s! 继续重试...' % (i, self.resp_code)
                            continue

                    if self.resp_code == 200:
                        with open('request.log', 'a') as f:
                            f.write('%s 最终请求成功!!!!!%s - %s\n' % (img_url, id, time.ctime()))
                        print ('[INFO]:最终请求成功!!!!!!!!!!')
                    else:
                        with open('request.log', 'a') as f:
                            f.write('%s 最终请求失败%s ! ! ! ! !%s - %s\n' % (img_url, self.resp_code, id, time.ctime()))
                        print ('[INFO]:最终请求失败%s!!!!!!!!!!') % self.resp_code

            print "正在保存　%s" % img_name
            with open(path + img_name + format, 'wb') as f:
                # print '******************',res
                f.write(data)
            # --------------------------------------------------------------------------------------
            print '共%s个　第%s个url: %s' % (list_length, k + 1, img_url)
            time.sleep(0)

            k += 1
        print "[INFO]: %s商品%s图片已抓取完成！！\n" % (id, name)

    def url_process(self, url):
        res = re.compile(r'(\?|&)goods_id=(\d+).*?', re.S)
        id = res.search(url).group(2)
        # print id
        return ''.join(id)

    def start(self, id):
        html_data = ""
        url = "https://mobile.yangkeduo.com/goods.html?goods_id=%s" % id
        # url = "https://mobile.yangkeduo.com/goods.html?goods_id=151940893&refer_page_name=opt&is_spike=0&refer_page_id=opt_1520401589628_cduy2B9GNp&refer_page_sn=10028"
        print url

        self.change_ua()

        try:
            time.sleep(0)
            res = self.srequest.get(url, headers=self.headers, proxies=self.proxy)
            self.resp_code = res.status_code
            if self.resp_code == 200:
                html_data = res.content

        except Exception as e:
            print '数据请求失败...正在重试......', e
            with open('request.log', 'a') as f:
                f.write('%s [代理]请求失败(%s) %s - %s\n' % (url, self.resp_code, id, time.ctime()))
            # # global NETWORK_STATUS
            NETWORK_STATUS = False  # 请求超时改变状态

            if NETWORK_STATUS == False:
                #     '请求超时'
                for i in range(1, 11):
                    time.sleep(0.3)
                    print '请求失败，第%s次重复请求' % i
                    if i == 5:
                        print "[INFO]: 代理睡眠中......"
                        time.sleep(10)
                    if i == 7:
                        print "[INFO]: 代理睡眠中......"
                        time.sleep(30)
                    if i == 9:
                        print "[INFO]: 代理睡眠中......"
                        time.sleep(60)
                    self.change_ua()

                    try:
                        res = self.srequest.get(url, headers=self.headers, proxies=self.proxy)
                        self.resp_code = res.status_code
                        if self.resp_code == 200:
                            html_data = res.content
                            with open('request.log', 'a') as f:
                                f.write('%s 重新请求成功%s - %s\n' % (url, id, time.ctime()))
                            print ('[INFO]:重发请求成功!!!!!!!!!!')
                            break
                    except:
                        with open('request.log', 'a') as f:
                            f.write('%s 重新请求失败, %s  继续重试...%s - %s\n' % (url, self.resp_code, id, time.ctime()))
                        print ('[INFO]:重发请求失败!!!!!!!!!!')
                        print '第%s次重复请求失败%s! 继续重试...' % (i, self.resp_code)
                        continue

                if self.resp_code == 200:
                    with open('request.log', 'a') as f:
                        f.write('%s 最终请求成功!!!!!%s - %s\n' % (url, id, time.ctime()))
                    print ('[INFO]:最终请求成功!!!!!!!!!!')
                else:
                    with open('request.log', 'a') as f:
                        f.write('%s 最终请求失败%s ! ! ! ! !%s - %s\n' % (url, self.resp_code, id, time.ctime()))
                    print ('[INFO]:最终请求失败%s!!!!!!!!!!') % self.resp_code


        # print html_data, "++++++++++++++++++++++++++++++++++"
        html = etree.HTML(html_data)
        js_data = html.xpath("/html/body/script[2]/text()")
        # 截取json数据
        json_data = js_data[0][25:-6]
        # print json_datacategory_name, dir_name, id
        self.json_res = json.loads(json_data)


if __name__ == '__main__':

    url = "http://mobile.yangkeduo.com/goods.html?goods_id=475767840"
    category_name = "文件夹"
    dir_name = "商品"
    ps = Pinduoduo_Spider()
    id = ps.url_process(url)
    ps.start(id)
    ps.create_json(id, category_name, dir_name)
    # ps.analysis_url(id, category_name, dir_name)