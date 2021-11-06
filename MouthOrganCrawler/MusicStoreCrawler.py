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


music_list_url = "http://www.tenholes.com/tabs/catelist?id=0"
download_path = pathlib.Path().cwd()/'半音阶'

cookie_str = "Hm_lvt_2f7f7866ed2b0addd933476e1018bb2a=1628064871,1629115371,1629186370; 4455941num=1; _csrf-frontend=fe5423196573cad678076b73cded218ede426fcfa3947757fad3655be924117ea%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22x_zme-OxZQJ1rEvdqQTrRDthtW6Tag3I%22%3B%7D; advanced-frontend=peu6e2u1u63jsqr26i8lp7231m; ten_auth1=ph5jqoPqZjlsq7ZJ9ecTZTI2ZWFmZDBiNGYyNDY3ZTFmYzYwOWFmYWQ3MDdmZGNlMDAwOTQzYzkxZDE3YTAyZDAwNDNlYzI4OGY0NWFmNzWVMejZMF6kqmRpSFP%2BDYjEjn4kFfU0z7vlJZTMOfkQx1mb%2BgvsxOceECi95EACQM1AHyNseNt5J6W%2F002%2FRDGk"
cookie_str = "{\"" + cookie_str + "\"}"
cookie_str = cookie_str.replace("rewardsn=;", "").replace(";", "\",\"").replace("=", "\":\"").replace(
    "\":\"\"", "=\"").replace(' ', '')
cookies = json.loads(cookie_str)

pages = 11
for page in range(1, pages):
    response = requests.get(f'{music_list_url}&page={page}',cookies=cookies)
    doc = pq(response.text, parser='html')
    music_list = [f"http://www.tenholes.com/{item.attr('href')}" for item in doc('div.ms-list a').items()]
    for music in music_list:
        response = requests.get(music, cookies=cookies)
        doc = pq(response.text, parser='html')
        music_name = doc('div.mt-tit p').text().replace(" ", "")
        music_store_jpg = doc('div.mt-con img').attr('src')
        music_audio = doc('#audioSrc').attr('value')
        music_bz_audio = doc('#audioBzSrc').attr('value')
        print(music_name, music_store_jpg, music_audio, music_bz_audio)

        dir_path = download_path / music_name
        try:
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True, parents=True)
                r = requests.get(music_store_jpg, cookies=cookies)
                with open(dir_path/f'{music_name}.jpg', 'wb') as f:
                    f.write(r.content)
                r = requests.get(music_bz_audio, cookies=cookies)
                with open(dir_path/f'{music_name}_伴奏.mp3', 'wb') as f:
                    f.write(r.content)
                r = requests.get(music_audio, cookies=cookies)
                with open(dir_path / f'{music_name}_示范.mp3', 'wb') as f:
                    f.write(r.content)
                print(music_name+' done!')
                time.sleep(1)
        except:
            pass






