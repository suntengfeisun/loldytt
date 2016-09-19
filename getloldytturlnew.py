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
        'url': 'http://www.loldytt.com/Dongzuodianying/chart/'
    },
    {
        'category': u'科幻片',
        'id': 2,
        'url': 'http://www.loldytt.com/Kehuandianying/chart/'
    },
    {
        'category': u'恐怖片',
        'id': 3,
        'url': 'http://www.loldytt.com/Kongbudianying/chart/'
    },
    {
        'category': u'喜剧片',
        'id': 4,
        'url': 'http://www.loldytt.com/Xijudianying/chart/'
    },
    {
        'category': u'爱情片',
        'id': 5,
        'url': 'http://www.loldytt.com/Aiqingdianying/chart/'
    },
    {
        'category': u'剧情片',
        'id': 6,
        'url': 'http://www.loldytt.com/Juqingdianying/chart/'
    },
    {
        'category': u'战争片',
        'id': 7,
        'url': 'http://www.loldytt.com/Zhanzhengdianying/chart/'
    },
    {
        'category': u'动漫',
        'id': 8,
        'url': 'http://www.loldytt.com/Anime/chart/'
    },
    {
        'category': u'综艺',
        'id': 9,
        'url': 'http://www.loldytt.com/Zuixinzongyi/chart/'
    },
    {
        'category': u'大陆剧',
        'id': 10,
        'url': 'http://www.loldytt.com/Dianshiju/chart/'
    },
    {
        'category': u'美剧',
        'id': 11,
        'url': 'http://www.loldytt.com/Zuixinmeiju/chart/'
    },
    {
        'category': u'韩剧',
        'id': 12,
        'url': 'http://www.loldytt.com/Zuixinhanju/chart/'
    },
    {
        'category': u'港剧',
        'id': 13,
        'url': 'http://www.loldytt.com/Zuixingangju/chart/'
    },
    {
        'category': u'台剧',
        'id': 14,
        'url': 'http://www.loldytt.com/Ouxiangju/chart/'
    },
    {
        'category': u'日剧',
        'id': 15,
        'url': 'http://www.loldytt.com/Zuixinriju/chart/'
    },
    {
        'category': u'泰剧',
        'id': 16,
        'url': 'http://www.loldytt.com/Taiguodianshiju/chart/'
    }
]


def getPageCount(url, first_page):
    num = 0
    headers = Headers.getHeaders()
    try:
        url = url + str(first_page) + '.html'
        req = requests.get(url, headers=headers, timeout=30)
        if req.status_code == 200:
            html = req.content
            selector = etree.HTML(html)
            page_counts = selector.xpath('//div[@class="pagebox"]/span/text()')
            if len(page_counts) > 0:
                page_count = page_counts[0]
                page_count_list = page_count.split(u'部')
                if len(page_count_list) >= 2:
                    aaa = page_count_list[1]
                    bbb = aaa.split(u'页')
                    if len(bbb) > 0:
                        page = bbb[0]
                        if page.isdigit() == True:
                            num = page
    except Exception, e:
        print Exception, ":", e
    return num


def getUrl(url, page):
    url = url + str(page) + '.html'
    print(url)
    mysqlDao = MysqlDao()
    try:
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
            for url_content in url_contents:
                sql = 'insert ignore into loldytt_url (`category_id`,`url`,`status`,created_at) VALUES (%s,%s,%s,%s)'
                created_at = time.strftime('%Y-%m-%d %H:%M:%S')
                values = (category_id, url_content, 0, created_at)
                print(values)
                mysqlDao.executeValues(sql, values)
            mysqlDao.close()
    except Exception, e:
        print Exception, ":", e
        mysqlDao.close()


if __name__ == '__main__':
    for u in urls:
        url = u['url']
        print('main_url' + url)
        category_id = u['id']
        n = 0
        while n < 5:
            page_count = getPageCount(url, 1)
            if page_count > 0:
                break
        """
        2016年7月18日 10:09:59
        换一下思路,以前上一个版本翻页总是报错
        这里直接取最后一页的页码然后-1到1为止
        """
        page = page_count
        print('page_count' + page)
        while True:
            if page == 0:
                break
            getUrl(url, page)
            page = int(page) - 1
        print('over one')
    print('game over')
    sys.exit()
