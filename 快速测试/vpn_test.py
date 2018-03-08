# coding=utf-8
import time
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
    "cookie": "ubn=p; ucn=unsz; t=28edc35882e1fcf06bfaa67008da2a8f; cna=XTyQEoI1uE4CAXBfh3IMFSpJ; thw=cn; miid=6347655561018672771; uc3=sg2=WqIrBf2WEDhnXgIg9lOgUXQnkoTeDo019W%2BL27EjCfQ%3D&nk2=rUs9FkCy6Zs6Ew%3D%3D&id2=VWeZAHoeqUWF&vt3=F8dBzLgoJIN4WC0X30I%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=%5Cu6211%5Cu6210%5Cu4F60%5Cu5669%5Cu68A6; tracknick=%5Cu6211%5Cu6210%5Cu4F60%5Cu5669%5Cu68A6; _cc_=WqG3DMC9EA%3D%3D; tg=0; enc=GtOY%2B8mhUi7LXIrV9LqmUl0PYsVpr9BbSzEB9GL%2Fq3i6Czwxxh5mE60CMJjep9GIq4iV04PvQsAGhzOIdrf6iw%3D%3D; mt=ci=-1_0; UM_distinctid=160fe373fd7c89-0f04cad75d123e-393d5f0e-1fa400-160fe373fd8e5a; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=081b6ec244bfd7ba155325c85a14056e_1516103738466; _m_h5_tk_enc=8531a9b39cfb4a076e45dfad1fba7525; cookie2=16e0f40738dc82c43c53992cb5a26ebb; _tb_token_=3daeebbb3768e; v=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; uc1=cookie14=UoTdfYT5TUo4kA%3D%3D; isg=BDo6USLQNOpL5rgFeJZzPiuWi2CcQ9uEDF5FrkQyJ02YN9lxLHiA1B8ng8PrpzZd",
    # "referer": "https://item.taobao.com/item.htm?spm=a219r.lmn002.14.174.6f516358W81jq9&id=561495525977&ns=1&abbucket=16",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}
url = "https://omsproductionimg.yangkeduo.com/images/2017-10-25/7bac2e3d0253f215080621ce00b81459.jpeg"
# url = "http://dsc.taobaocdn.com/i8/550/150/557156122382/TB13lKSXSYTBKNjSZKb8qtJ8pla.desc%7Cvar%5Edesc%3Bsign%5Eb9b931bf2a0ad0b5a7d20095043315cc%3Blang%5Egbk%3Bt%5E1519630932"
proxies = {'https': 'http://16SBYYUY:658666@n10.t.16yun.cn:6442', 'http': 'http://16SBYYUY:658666@n10.t.16yun.cn:6442'}


list = [
    "http://omsproductionimg.yangkeduo.com/images/2017-12-19/0196d2f5d82e3017761efa5028d93cdb.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/1281d401bb2cfac52e828986b8851e48.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-11-09/b602d05950013930266794b2ec5eb75b.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/ee7f25ecd1e416ed1822f3e9064097a2.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/c3d364da514cf3c8ff84b2d17566a65e.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/a4699930b644bbbd3d18de2735ecc3aa.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/ef244ab68e01299d213c97fd8249a463.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-11-06/da30e68b8b7cc47ef4f90651be4c0181.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/53052b73a5862e8620e1712ff2b69f82.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/9d2565f6542ddef60ede5395e345ab2e.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/7a2432f4c278b503a74290d3b02cb98d.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/b752f03e83fccce4d93c3854e6e701dc.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/caf53756e7c31dd7585eb19efd004c93.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/420b418af76ea09c33df116b39cf6e9a.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/73ab9d1f1c11e62ccafe61223e107c88.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/0755e711e2a8f45ad11b9a47a289935f.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/844c286cd610ba83bfa80450ee9b4aa1.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/37d9396d38015e296128e8268e73ced3.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/21ea30564c97d8e7707469a1b6badebc.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/3596e64ca8d18fe906f23dccba48b40e.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/0b318db10ac5ca0d3f20f5c72b0ca97b.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/c578ed1e8569dab51e4de602382bd304.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/e11ea1e87b8b8c27d9c5c9e3f0206c5f.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/1985ef1318be0af88cc05078a987af66.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/a85c88aa77cf4e3a49d25ea92b6d5050.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/3faff5390955068fbf054bffd91c4b6e.jpeg@750w_1l_50Q",
    "http://omsproductionimg.yangkeduo.com/images/2017-10-25/7bac2e3d0253f215080621ce00b81459.jpeg@750w_1l_50Q",
]

def test(url,proxies,headers):
    srequest = requests.Session()
    i = 1
    total_s = time.time()
    ok_count = 0
    for i in range(27):
        name = 'pinduoduo%s.jpg' % i
        print name
        res = srequest.get(list[i], headers=headers, proxies=proxies)
        print res.status_code
        if res.status_code == 200:
            data = res.content
            with open("test%s.jpg" % i, 'wb') as f:
                # print '******************',res
                f.write(data)
            ok_count += 1
    total_e = time.time()
    print total_e-total_s
    print ok_count / (total_e-total_s)

test(url,proxies,headers)


# def download_img(self, list_length, list, id, name, category_name, dir_name, *args):
#     k = 0
#     while k < list_length:
#         data = ''
#         self.resp_code = ""
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
#         try:
#             time.sleep(0)
#             response = requests.get(img_url, headers=self.headers, proxies=self.proxy)
#             self.resp_code = response.status_code
#             if self.resp_code == 200:
#                 data = response.content
#
#         except Exception as e:
#             print '数据请求失败...正在重试......', e
#             with open('request.log', 'a') as f:
#                 f.write('%s [代理]请求失败(%s) %s - %s\n' % (img_url, self.resp_code, id, time.ctime()))
#             # # global NETWORK_STATUS
#             NETWORK_STATUS = False  # 请求超时改变状态
#
#             if NETWORK_STATUS == False:
#                 #     '请求超时'
#                 for i in range(1, 11):
#                     time.sleep(0.3)
#                     print '请求失败，第%s次重复请求' % i
#                     if i == 5:
#                         print "[INFO]: 代理睡眠中......"
#                         time.sleep(10)
#                     if i == 7:
#                         print "[INFO]: 代理睡眠中......"
#                         time.sleep(30)
#                     if i == 9:
#                         print "[INFO]: 代理睡眠中......"
#                         time.sleep(60)
#                     self.change_ua()
#
#                     try:
#                         response = requests.get(img_url, headers=self.headers, proxies=self.proxy)
#                         self.resp_code = response.status_code
#                         if self.resp_code == 200:
#                             data = response.content
#                             with open('request.log', 'a') as f:
#                                 f.write('%s 重新请求成功%s - %s\n' % (img_url, id, time.ctime()))
#                             print ('[INFO]:重发请求成功!!!!!!!!!!')
#                             break
#                     except:
#                         with open('request.log', 'a') as f:
#                             f.write('%s 重新请求失败, %s  继续重试...%s - %s\n' % (img_url, self.resp_code, id, time.ctime()))
#                         print ('[INFO]:重发请求失败!!!!!!!!!!')
#                         print '第%s次重复请求失败%s! 继续重试...' % (i, self.resp_code)
#                         continue
#
#                 if self.resp_code == 200:
#                     with open('request.log', 'a') as f:
#                         f.write('%s 最终请求成功!!!!!%s - %s\n' % (img_url, id, time.ctime()))
#                     print ('[INFO]:最终请求成功!!!!!!!!!!')
#                 else:
#                     with open('request.log', 'a') as f:
#                         f.write('%s 最终请求失败%s ! ! ! ! !%s - %s\n' % (img_url, self.resp_code, id, time.ctime()))
#                     print ('[INFO]:最终请求失败%s!!!!!!!!!!') % self.resp_code
#
#         print "正在保存　%s" % img_name
#         with open(path + img_name + format, 'wb') as f:
#             # print '******************',res
#             f.write(data)
#         # --------------------------------------------------------------------------------------
#         print '共%s个　第%s个url: %s' % (list_length, k + 1, img_url)
#         time.sleep(0)
#
#         k += 1
#     print "[INFO]: %s商品%s图片已抓取完成！！\n" % (id, name)
