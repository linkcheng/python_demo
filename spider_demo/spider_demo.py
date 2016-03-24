#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: IcySun
# 脚本功能：爬妹子
import urllib2,re
import os,time,socket

def getJpgurl(weburl):
    request = urllib2.Request(weburl)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11') 
    response = urllib2.urlopen(request,timeout=20)
    html_doc = response.read()
    rejpgurl = r'"><img src="(.*?).jpg" /></a>'
    jpgurl = re.findall(rejpgurl, html_doc)
    for jpg in jpgurl:
        jpg_url = jpg + '.jpg'
        name = jpg.split('/')[-1]
        try:
            request = urllib2.Request(jpg_url)
            request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11') 
            f = urllib2.urlopen(request,timeout=20)
            try:
                data = f.readlines()
                response = urllib2.urlopen(request,timeout=20)
                f = open(name+'.jpg','wb')
                file_size_dl = 0
                block_sz = 512
                while True:
                    buffer = response.read(block_sz)
                    if not buffer:
                        break
                    file_size_dl += len(buffer)
                    f.write(buffer)
                f.close()
            except urllib2.URLError, e:
                continue
            except socket.timeout,e:
                continue
        except urllib2.URLError, e:
            continue
        except socket.timeout,e:
            continue
def main():
    for i in xrange(1,10):#循环多少页
        url = 'http://xinlang.sinaapp.com/weibo/wall/girl/'+str(i)
        #print url
        getJpgurl(url)
        time.sleep(1)
if __name__ == '__main__':
    main()
