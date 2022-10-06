# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  new_movie.py
    Description:  豆瓣影视信息爬虫
    Author:      Chenghu
    Date:       2022/2/26 2:17 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import json
import re
import time
import traceback
from selectolax.parser import HTMLParser
import httpx
import random
from datetime import datetime, timedelta
from apps.baseserver import SyncMysqlBaseService, SyncRedisBaseService
import logging
from . import USER_AGENTS
from loguru import logger
from apps.core.ini_scheduler import scheduler


class get_lasted_tv:

    def __init__(self):

        self._DOUBAN = 'https://movie.douban.com/j/new_search_subjects'
        self._proxies = {}
        self._headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://movie.douban.com/tag/',
            'User-Agent': random.choice(USER_AGENTS),
            'Cookie': 'bid=nkRqb7w14xQ; douban-fav-remind=1; ll="118172"; gr_user_id=86cb43aa-aaff-4fd0-917b-36a1336a10a5; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1650851341; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1650851341; ap_v=0,6.0; viewed="35795043_35668939_4913064_1082154"; _pk_ref.100001.4cf6=["","",1650938342,"https://cn.bing.com/"]; _pk_ses.100001.4cf6=*; dbcl2="253159781:3Eo4RTRA0kc"; ck=SsLF; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=b480c755a678daec.1642487039.17.1650940102.1650936089.',
            # 浏览器登录后复制Cookie贴到此处
        }
        self._MovieBaseUrl = "https://movie.douban.com/j/search_subjects?type=movie&tag=最新&page_limit=20&page_start={page}"
        self._TvBaseUrl = "https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=time&page_limit=20&page_start={page}"
        self.mysql = SyncMysqlBaseService()

    def get_movie_info(self, url):
        if url:
            req = httpx.get(url, headers=self._headers, timeout=10)
            logging.info(f"get_movie_info url: {url}")
            if req.status_code == 200:
                res = {"directors": '', "casts": '', "image_url": '',
                       'url': url, 'movie_type': '', 'public_date': '', 'city':''}
                tree = HTMLParser(req.content)
                res['title'] = tree.css_first('h1 span[property="v:itemreviewed"]').text(strip=True)
                details = tree.css_first('div[class="subject clearfix"]')
                cover = details.css_first('a[class="nbgnbg"] img')
                if cover:
                    res['image_url'] = cover.attrs.get('src')

                movie_info = details.css_first('div[id="info"]')
                movie_info = movie_info.text(strip=True, separator=' ')  # .replace(':;', ':@').replace(';:', ":")
                movie_info = re.findall(r"\S+\s*:\s*\S+", movie_info)
                if movie_info:
                    for bo in movie_info:
                        data = bo.split(':')
                        da = data[0].strip()
                        value = data[1].strip()
                        if da == '导演':
                            res.update({'directors': value})
                        elif da == '主演':
                            res.update({'casts': value})
                        elif data[0].strip() == '类型':
                            res.update({"movie_type": value})
                        elif re.match('制片|国家|地区', da):
                            res.update({'city': value})
                        elif da == '上映日期':
                            res.update({'public_date': value})
                        elif public_date := re.match('\d{4}-\d{2}-\d{2}|\d{4}-\d{2}', value):
                            res.update({'public_date': public_date[0]})

                return res
        else:
            raise

    def get_tv_list(self, type: str = 'movie', page=1):
        if type == 'movie':
            base_url = self._MovieBaseUrl.format(page=page)
        else:
            base_url = self._TvBaseUrl.format(page=page)
        req = httpx.get(base_url, headers=self._headers, timeout=10)
        if req.status_code == 200:
            return req.json()['subjects']
        logger.error(f'爬取豆瓣电影信息失败： {req.status_code}')
        raise

    def save_db(self, data):
        # MysqlCnn.save_data(data, table='cw_movie')

        self.mysql.insert_or_update(table_name='cw_movie', values=data,
                               update_name=['directors', 'casts', 'image_url', 'url', 'movie_type', 'public_date', 'city', 'special_id', 'oss_img'])

    def run(self):
        for ty in ["movie", "tv"]:
            logger.info(f'start {ty}')
            pages = 10
            for page in range(0, pages):
                try:
                    data = self.get_tv_list(type=ty, page=page)
                    save_list = []
                    for li in data:
                        movie_info = self.get_movie_info(li['url'])
                        movie_info['special_id'] = li.get('id', '0')
                        save_list.append(movie_info)
                        time.sleep(random.randint(1,3))
                    self.save_db(save_list)

                except Exception as e:
                    time.sleep(10)


def start_movie():
    try:
        get_lasted_tv().run()
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        # trigger = scheduler._create_trigger(trigger='interval', trigger_args={"days": 2})
        # next_time = datetime.now() + timedelta(hours=random.randint(10, 24))
        # scheduler.modify_job('new_movie', trigger=trigger, next_run_time=next_time)
        # logger.info(f"修改下次爬取电影时间为：{next_time}")

        try:
            next_time = datetime.now() + timedelta(hours=random.randint(10, 24))
            scheduler.reschedule_job(job_id='new_movie', trigger='interval', start_date=next_time, days=2)
            logger.info(f'修改下次爬取音乐时间为：{next_time}')
        except Exception as e:
            logger.exception(f"修改 music 定时任务失败： {traceback.format_exc()}" )
