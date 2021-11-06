#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: BENULL
@time: 2021/11/6 上午12:20
"""

import requests
import pathlib
import json
from pyquery import PyQuery as pq
import time
import re


lessons_url = "http://www.tenholes.com/lessons/list?cid=12"
download_path = pathlib.Path().cwd()/'教程'/'半音阶口琴上的音阶'

cookie_str = "Hm_lvt_2f7f7866ed2b0addd933476e1018bb2a=1628064871,1629115371,1629186370; 4455941num=1; _csrf-frontend=fe5423196573cad678076b73cded218ede426fcfa3947757fad3655be924117ea%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22x_zme-OxZQJ1rEvdqQTrRDthtW6Tag3I%22%3B%7D; advanced-frontend=peu6e2u1u63jsqr26i8lp7231m; ten_auth1=ph5jqoPqZjlsq7ZJ9ecTZTI2ZWFmZDBiNGYyNDY3ZTFmYzYwOWFmYWQ3MDdmZGNlMDAwOTQzYzkxZDE3YTAyZDAwNDNlYzI4OGY0NWFmNzWVMejZMF6kqmRpSFP%2BDYjEjn4kFfU0z7vlJZTMOfkQx1mb%2BgvsxOceECi95EACQM1AHyNseNt5J6W%2F002%2FRDGk"
cookie_str = "{\"" + cookie_str + "\"}"
cookie_str = cookie_str.replace("rewardsn=;", "").replace(";", "\",\"").replace("=", "\":\"").replace(
    "\":\"\"", "=\"").replace(' ', '')
cookies = json.loads(cookie_str)

response = requests.get(lessons_url, cookies=cookies)
doc = pq(response.text, parser='html')
lessons_list = [f"http://www.tenholes.com/{item.attr('href')}" for item in doc('div.ls-list .ls-item a').items()]

for lesson in lessons_list:
    try:
        response = requests.get(lesson, cookies=cookies)
        doc = pq(response.text, parser='html')
        lesson_name = doc('div.lt-byte p').text().replace(" ", "")
        video = re.search(r'http://authcdn.tenholes.com/videoAll/(.*);', response.text).group()[:-2]
        # video = doc('video#myVideo_html5_api').attr('src')
        print(lesson_name, video)
        dir_path = download_path / lesson_name
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True, parents=True)
            r = requests.get(video, cookies=cookies)
            with open(dir_path / f'{lesson_name}.mp4', 'wb') as f:
                f.write(r.content)
            print(lesson_name+' done!')
            time.sleep(1)
    except:
        pass






