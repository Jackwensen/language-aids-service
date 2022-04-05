# !/usr/bin/python
# coding = 'utf-8'

# 设置编码格式为utf-8，为了可以打印出中文字符
import sys
import os

# 导入urllib2模块，用于通过url获取网页的内容
import urllib
from flask import jsonify

# 导入BeautifulSoup模块(需要安装)，用于解析网页的内容
import requests
from bs4 import BeautifulSoup as ba

# import correcttext
import maccorrectext
# 导入修改后的文字
# text = correcttext.suggestion['correct_query']
# 测试用的文本
def text2signal(kw):
    keyword = maccorrectext.in_door(kw)
    # keyword = corrected['correct_query']
    # 将中文编码
    # wd = urllib.parse.quote(keyword)

    # 设置爬取的初始url,headers
    base_url = 'http://shouyu.z12345.com/1-' + urllib.parse.quote(keyword) + '.html'
    reponse = requests.get(url=base_url).text
    # 当网页编码为UTF-8，请求为ISO-8859-1时，可用以下办法（ignore为有些不可转换的编码准备）
    reponse = reponse.encode("ISO-8859-1")
    reponse = reponse.decode("utf-8", 'ignore')
    html = ba(reponse,'lxml')
    tmp = html.find('tr', attrs={"align":"center","class":"h"})
    imghtml = tmp.find_all_next('tr')
    list = []
    for i in imghtml:
        data = {}
        img = i.find('td', attrs={'class': 'i'})
        if img:
            # 手语输出
            # 手语图片
            imgsrc = 'http://shouyu.z12345.com' + img.img.get('src')
            data['imgsrc'] = imgsrc
            # print(imgsrc)
            # 手语含义
            imgmeaning = img.img.get('alt').split()[1]
            data['meaning'] = imgmeaning
            # print(imgmeaning)
            # 手语文字解说
            note = img.find_next('td').text
            data['note'] = note
            # print(note)
            list.append(data)
    print({'data': list, 'corrected': keyword})
    return {'data': list, 'corrected': keyword}


# kw = '请给我一支铅笔'
# wd = urllib.parse.quote(kw)
# result = text2signal(wd)
