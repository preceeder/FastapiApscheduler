# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  hot_top_music.py
    Description:  网易云音乐爬虫
    Author:      Chenghu
    Date:       2022/2/26 6:28 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import time
import traceback
import httpx
from selectolax.parser import HTMLParser
import json
from apps.baseserver import SyncMysqlBaseService, SyncRedisBaseService
from loguru import logger
from datetime import datetime, timedelta
from apps.core.ini_scheduler import scheduler
import random

# 网易云新歌榜根url
# BaseUrl = "https://music.163.com/#"


class RankingUpdate:
    def __init__(self):
        self.BaseUrl = "https://music.163.com"
        self.mysql = SyncMysqlBaseService()

    def get_list(self):
        html = httpx.get(url='https://music.163.com/discover/toplist', timeout=10)
        tree = HTMLParser(html.content.decode('utf-8'))
        all_html = tree.css_first('div[id="toplist"]')
        side_html = all_html.css_first('div[class="g-sd3 g-sd3-1"]')
        bang_list = side_html.css('a[class="avatar"]')
        list_data = []
        for url_l in bang_list:
            list_data.append(url_l.attrs.get('href'))
        return list_data

    def run(self):
        url_list = self.get_list()
        for url in url_list:
            data = self.get_singe_data(f"{self.BaseUrl}{url}")
            will_save_data = self.parsed_data(data)
            for item in will_save_data:
                self.save_data([item])
                time.sleep(2)

    def get_singe_data(self, url):
        data = httpx.get(url=url, timeout=10)
        tree = HTMLParser(data.content.decode('utf-8'))
        all_list = tree.tags('textarea')[0]
        singe_data = json.loads(all_list.text(strip=True))
        return singe_data

    def parsed_data(self, singe_data):
        res_data = []
        for singe in singe_data:
            singer = "/".join([singer_name['name'] for singer_name in singe['artists']])
            res_data.append({
                "name": singe['name'],
                "music_id": singe['id'],
                "singer": singer,
                "album": singe['album']['name'],
                "image_url": singe['album']['picUrl'],
                "oss_img": ''
            })
        return res_data

    def save_data(self, data):
        self.mysql.insert_or_update(table_name='cw_music', values=data,
                               update_name=['name', 'album', 'image_url', 'oss_img', 'singer'])


def start_music():

    try:
        RankingUpdate().run()
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        try:
            next_time = datetime.now() + timedelta(hours=random.randint(10, 24))
            scheduler.reschedule_job(job_id='new_music', trigger='interval', start_date=next_time, days=2)
            logger.info(f'修改下次爬取音乐时间为：{next_time}')
        except Exception as e:
            logger.exception(f"修改 music 定时任务失败： {traceback.format_exc()}")

