# -*- coding: utf-8 -*-

import time
import threading
import requests
from lxml import etree
import simplejson
from mysqlpooldao import MysqlDao
from headers import Headers
import sys
from config import Config

reload(sys)
sys.setdefaultencoding('utf-8')


class Worker(threading.Thread):
    def run(self):
        while True:
            print(self.name)
            mysqlDao = MysqlDao()
            sql = 'select * from loldytt_url WHERE `status`=0 limit 0,1'
            ret = mysqlDao.execute(sql)
            if len(ret) == 0:
                mysqlDao.close()
                """
                不用睡眠直接退出等crontab唤醒
                """
                print('game over')
                sys.exit()
            else:
                res = ret[0]
                id = res[0]
                category_id = res[1]
                url = res[2]
                sql = 'update loldytt_url set `status`=2 where `id`=' + str(id)
                mysqlDao.execute(sql)
                headers = Headers.getHeaders()
                n = 0
                while n < 5:
                    req = requests.get(url, headers=headers)
                    req.encoding = "gbk"
                    if req.status_code == 200:
                        html = req.text.encode(encoding="utf-8", errors="ignore").decode("utf-8", errors="ignore")
                        try:
                            selector = etree.HTML(html)
                        except:
                            print 333
                        titles = selector.xpath('//div[contains(@class,"lm")]/h1/a/text()')
                        if len(titles) > 0:
                            break
                    n = n + 1
                if len(titles) > 0:
                    title = titles[0]
                else:
                    continue
                casts = selector.xpath('//div[contains(@class,"zhuyan")]/ul[1]/li/text()')
                imgs = selector.xpath('//div[contains(@class,"haibao")]/a[1]/img/@src')
                cast = ''
                img = ''
                content = ''
                if len(casts) > 0:
                    cast = casts[0].split('：')[1]
                if len(imgs) > 0:
                    img = imgs[0]
                contents = selector.xpath('//div[@class="neirong"]/descendant::text()')
                if len(contents) > 0:
                    content = simplejson.dumps(contents)
                created_at = time.strftime('%Y-%m-%d %H:%M:%S')
                xunlei_download_keys = selector.xpath(
                        '//*[contains(@id,"jishu")]/descendant::a[contains(@href,"thunder")]/text()')
                xunlei_download_values = selector.xpath(
                        '//*[contains(@id,"jishu")]/descendant::a[contains(@href,"thunder")]/@href')
                bt_download_keys = selector.xpath(
                        '//*[contains(@id,"bt")]/descendant::a[contains(@href,"thunder")]/text()')
                bt_download_values = selector.xpath(
                        '//*[contains(@id,"bt")]/descendant::a[contains(@href,"thunder")]/@href')
                magnet_download_keys = selector.xpath('//a[contains(@href,"magnet")]/text()')
                magnet_download_values = selector.xpath('//a[contains(@href,"magnet")]/@href')
                xunlei_download = []
                bt_download = []
                magnet_download = []
                try:
                    xn = 0
                    for x in xunlei_download_keys:
                        xunlei_download.append({xunlei_download_keys[xn]: xunlei_download_values[xn]})
                        xn = xn + 1
                    bn = 0
                    for b in bt_download_keys:
                        bt_download.append({bt_download_keys[bn]: bt_download_values[bn]})
                        bn = bn + 1
                    mn = 0
                    for m in magnet_download_keys:
                        magnet_download.append({magnet_download_keys[mn]: magnet_download_values[mn]})
                        mn = mn + 1
                except Exception, e:
                    print Exception, ":", e
                xunlei_download_json = simplejson.dumps(xunlei_download)
                bt_download_json = simplejson.dumps(bt_download)
                magnet_download_json = simplejson.dumps(magnet_download)
                sql_pattern = 'insert ignore INTO `loldytt_content`(`category_id`, `title`,`cast`,`img`,`xunlei_download`, `bt_download`, `magnet_download`, `content`, `url`,`created_at`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                sql_values = (
                    category_id, title, cast, img, xunlei_download_json, bt_download_json, magnet_download_json,
                    content, url, created_at)
                print(title)
                mysqlDao.executeValues(sql_pattern, sql_values)
                sql = 'update loldytt_url set `status`=1 where `id`=' + str(id)
                mysqlDao.execute(sql)
                mysqlDao.close()


if __name__ == '__main__':
    worker_num = 1
    threads = []
    for x in xrange(0, worker_num):
        threads.append(Worker())
    for t in threads:
        t.start()
        time.sleep(5)
    for t in threads:
        t.join()
