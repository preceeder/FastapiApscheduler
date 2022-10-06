# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:  __init__.py
    Description:  爬虫任务
    Author:      Chenghu
    Date:       2022/7/25 4:31 下午 
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
]

sin_to_oss = {
    "book": "books",
    "movie": "movies",
    "music": "musics"
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Referer': 'https://movie.douban.com/tag/',
    # 'User-Agent': random.choice(USER_AGENTS),
    # 'Cookie': 'bid=nkRqb7w14xQ; douban-fav-remind=1; ll="118172"; push_noty_num=0; push_doumail_num=0; gr_user_id=86cb43aa-aaff-4fd0-917b-36a1336a10a5; ct=y; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1642583683; dbcl2="253159781:p4VXUjbgx4k"; ck=43IV; ap_v=0,6.0; _pk_ref.100001.4cf6=["","",1643079468,"https://www.douban.com/"]; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=b480c755a678daec.1642487039.7.1643079471.1643019875.',  # 浏览器登录后复制Cookie贴到此处
}

