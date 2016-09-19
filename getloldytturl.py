# -*- coding: utf-8 -*-

import sys
import requests
import time
from headers import Headers
from config import Config
from lxml import etree
from mysqlpooldao import MysqlDao

reload(sys)
sys.setdefaultencoding('utf8')

urls = [
    {
        'category': u'动作片',
        'id': 1,
        'url': 'http://www.loldytt.com/Dongzuodianying/chart/1.html'
    },
    {
        'category': u'科幻片',
        'id': 2,
        'url': 'http://www.loldytt.com/Kehuandianying/chart/1.html'
    },
    {
        'category': u'恐怖片',
        'id': 3,
        'url': 'http://www.loldytt.com/Kongbudianying/chart/1.html'
    },
    {
        'category': u'喜剧片',
        'id': 4,
        'url': 'http://www.loldytt.com/Xijudianying/chart/1.html'
    },
    {
        'category': u'爱情片',
        'id': 5,
        'url': 'http://www.loldytt.com/Aiqingdianying/chart/1.html'
    },
    {
        'category': u'剧情片',
        'id': 6,
        'url': 'http://www.loldytt.com/Juqingdianying/chart/1.html'
    },
    {
        'category': u'战争片',
        'id': 7,
        'url': 'http://www.loldytt.com/Zhanzhengdianying/chart/1.html'
    },
    {
        'category': u'动漫',
        'id': 8,
        'url': 'http://www.loldytt.com/Anime/chart/1.html'
    },
    {
        'category': u'综艺',
        'id': 9,
        'url': 'http://www.loldytt.com/Zuixinzongyi/chart/1.html'
    },
    {
        'category': u'大陆剧',
        'id': 10,
        'url': 'http://www.loldytt.com/Dianshiju/chart/1.html'
    },
    {
        'category': u'美剧',
        'id': 11,
        'url': 'http://www.loldytt.com/Zuixinmeiju/chart/1.html'
    },
    {
        'category': u'韩剧',
        'id': 12,
        'url': 'http://www.loldytt.com/Zuixinhanju/chart/1.html'
    },
    {
        'category': u'港剧',
        'id': 13,
        'url': 'http://www.loldytt.com/Zuixingangju/chart/1.html'
    },
    {
        'category': u'台剧',
        'id': 14,
        'url': 'http://www.loldytt.com/Ouxiangju/chart/1.html'
    },
    {
        'category': u'日剧',
        'id': 15,
        'url': 'http://www.loldytt.com/Zuixinriju/chart/1.html'
    },
    {
        'category': u'泰剧',
        'id': 16,
        'url': 'http://www.loldytt.com/Taiguodianshiju/chart/1.html'
    }
]


def getUrlLast(url):
    n = 1
    print(url)
    while True:
        try:
            headers = Headers.getHeaders()
            req = requests.get(url, headers=headers, timeout=10)
            break
        except Exception, e:
            print Exception, ":", e
            print('sleep')
            time.sleep(n * 10)
            n = n + 1
    if req.status_code == 200:
        html = req.content
        selector = etree.HTML(html)
        url_lasts = selector.xpath('//div[@class="pagebox"]/descendant::a[last()]/@href')
        url_last = ''
        if len(url_lasts) > 0:
            url_last = url_lasts[0]
        return url_last


def getUrl(url, category_id):
    print(url)
    if url == 'http://www.loldytt.com/Zuixinhanju/chart/26.html':
        url = 'http://www.loldytt.com/Zuixinhanju/chart/25.html'
    mysqlDao = MysqlDao()
    n = 1
    while True:
        try:
            headers = Headers.getHeaders()
            req = requests.get(url, headers=headers, timeout=10)
            break
        except Exception, e:
            print Exception, ":", e
            print('sleep')
            time.sleep(n * 10)
            n = n + 1
    if req.status_code == 200:
        html = req.content
        selector = etree.HTML(html)
        url_contents = selector.xpath('//div[@class="box3"]/descendant::a/@href')
        if len(url_contents) < 0:
            print(1111)
            print(2222)
        for url_content in url_contents:
            sql = 'insert ignore into loldytt_url (`category_id`,`url`,`status`,created_at) VALUES (%s,%s,%s,%s)'
            created_at = time.strftime('%Y-%m-%d %H:%M:%S')
            values = (category_id, url_content, 0, created_at)
            mysqlDao.executeValues(sql, values)
        url_nexts = selector.xpath('//a[contains(text(),"%s")]/@href' % (u'上一页'))
        mysqlDao.close()
        print(url_nexts)
        if len(url_nexts) > 0:
            url_next = Config.url_main + url_nexts[0]
            getUrl(url_next, category_id)
        else:
            print(url_contents)


if __name__ == '__main__':
    for u in urls:
        url = u['url']
        category_id = u['id']
        while True:
            url_last = getUrlLast(url)
            if url_last != '':
                break
        url_last = Config.url_main + url_last
        getUrl(url_last, category_id)
    print('game over')
    sys.exit()
