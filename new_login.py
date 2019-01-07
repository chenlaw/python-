# -*- coding: utf-8 -*-

"""
@author: lwj
@file: new_login.py
@time: 2019/1/4 21:30
"""

import requests
import base64
import time
import re
import json
import jsonpath
from bs4 import BeautifulSoup
import patentScratching as ruokuai
from PIL import Image

# ----------------------------------------------------------------------------------#
'''专利网注册的账号'''
strName = 'tiger1575344246'
strPass = 'Tiger06191027'
# ----------------------------------------------------------------------------------#


##构造请求头##
# ----------------------------------------------------------------------------------#
checkHeader = {
    "Host": "www.pss-system.gov.cn",
    "Proxy-Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Origin": "http://www.pss-system.gov.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8"
}

header = {
    "Accept": "text / html, * / *;q = 0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}

searchHeader = {
    'Origin': 'http://www.pss-system.gov.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

baseUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml'
checkUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check'
# ------------------------------------------------------------------------------------#


# 构造网址需要的基本字符串
# ----------------------------------------------------------------------------------#
findUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/paramRewriter-paramEncode.shtml'
BASEurl = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/portal2HomeSearch-portalSearch.shtml?params='
show_list_url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml'
codeUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml'  # 验证码
personUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchHistory-showMyHistory.shtml'  # 个人中心
utl_search_url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeSmartSearch1207-executeSmartSearch.shtml'  # 执行搜索的网页


# ----------------------------------------------------------------------------------#

# 暂时命名而已
# =============打码平台===============#
def validation_result():
    client = ruokuai.APIClient()
    paramDict = {}
    ''' 以下参数请勿修改'''
    paramDict['username'] = 'Rollingegg'
    paramDict['password'] = 'LWJsteve98'
    paramDict['typeid'] = '7100'
    paramDict['timeout'] = '30'
    paramDict['softid'] = '115489'
    paramDict['softkey'] = 'b7369eb491a54c60bce17d2c6ba09e41'
    paramKeys = ['username',
                 'password',
                 'typeid',
                 'timeout',
                 'softid',
                 'softkey'
                 ]
    # 验证码图片的路径，请保存在与本文件同一文件夹下
    imagePath = 'valcode.png'
    img = Image.open(imagePath)
    if img is None:
        print('get file error!')
        return
    img.save("upload.gif", format="gif")
    filebytes = open("upload.gif", "rb").read()
    result = client.http_upload_image("http://api.ruokuai.com/create.xml", paramKeys, paramDict, filebytes)
    # print(result)
    # 返回计算结果
    pattern = '(<Result>)([0-9]+)(</Result>)'
    return str(re.search(pattern, str(result)).group(2))


# ----------------------------------------------------------------------------------#
def login():
    key = 'CN201610477192'  # 随意修改
    # ---------- ---登陆请求--------------------------#
    ##base64编码解码##
    base64Name = str(base64.b64encode(bytes(strName, encoding='utf-8')), 'utf-8')
    base64Pass = str(base64.b64encode(bytes(strPass, encoding='utf-8')), 'utf-8')

    data = {
        "j_loginsuccess_url": "",
        "j_validation_code": "",
        "j_username": base64Name,
        "j_password": base64Pass
    }
    session = requests.Session()  # 会话保持
    valcode = session.get(codeUrl, headers=header)
    f = open('valcode.png', 'wb')
    f.write(valcode.content)
    f.close()
    code = input('请输入验证码：')  # 手动输入
    # code = validation_result() # 打码平台补充
    start_time = time.time()  # 记录起始时间
    data["j_validation_code"] = str(code)
    # print( session.utils.dict_from_cookiejar(valcode.cookies))
    resp = session.post(checkUrl, headers=checkHeader, cookies=requests.utils.dict_from_cookiejar(valcode.cookies),
                        data=data)
    if str(resp.status_code) == '200':  # 正确的网页响应码
        print("登陆成功!")
    end1_time = time.time()
    print('登陆成功需时间为' + str(end1_time - start_time) + 's')
    # print(BeautifulSoup(resp.content,'lxml').prettify())
    my_cookies = resp.cookies
    # --------------用关键词来构造表单提交请求之后返回参数-----------#
    data1 = {
        'params': 'searchExpFromIndex=' + key + '@==@searchCondition_scope=@==@searchCondition_type=AI'
    }
    resp = session.post(findUrl, cookies=my_cookies, data=data1)
    soup1 = BeautifulSoup(resp.content, 'lxml')
    params_text = soup1.text
    re_params = r'[0-9A-Z]+'
    params = re.findall(re_params, params_text)
    # print(params[0])
    print('############################################')
    search_url = BASEurl + params[0]  # 应该是这个网址了吧
    # ========================
    data2 = {
        'searchCondition.searchExp': key,
        'search_scope': '',
        'searchCondition.dbId': 'VDB',
        'resultPagination.limit': '12',
        'searchCondition.searchType': 'Sino_foreign',
        'wee.bizlog.modulelevel': '0200101'
    }
    # new_params = [('params',params[0])]
    # res_search = session.get(search_url)
    # print(session.get(personUrl).text)  # 测试是否能进入个人中心
    resp = session.get(search_url)
    print('===========================')
    resp = session.post(utl_search_url, cookies=my_cookies, data=data2)
    # print(BeautifulSoup(resp.content, 'lxml').prettify())
    myJson = json.loads(resp.text, encoding='utf-8')
    # with open('record.json','w',encoding='utf-8') as f:  # 写入json文件测试
    #     json.dump(myJson,f,ensure_ascii=False,indent=4)
    # print(myJson)
    # 从根节点开始，匹配result节点
    result_list = jsonpath.jsonpath(myJson, '$..searchResultRecord[*].fieldMap.DESC')
    with open(key + '.txt', 'w', encoding='utf-8') as fp:
        text = list()
        re_search = r'<[^>]+>'
        for con in result_list:
            txt = str(con)
            a = re.sub(re_search, '', txt)
            txt = "".join(a.split())
            if txt != 'None':
                # fp.write(txt)
                text.append(txt)
        # fp.write(content)
        print(text)
    end2_time = time.time()
    print('从登陆成功到下载文本时间为' + str(end2_time - end1_time) + 's')


if __name__ == '__main__':
    login()
