#!/usr/bin/env python
#coding:utf-8

import requests
import re

def getUrl(session, cookie):
    commit_id = '68926df060ac7cad1dfcf78c794f261ceb1effad'
    url = 'http://igerrit/gitweb?string=Doc/17Model/17Cy/21_UI.git;a=commit;h=' + commit_id
    headers = {'Cookie':cookie}

    r = session.request('GET', url, headers = headers)

    it = re.findall(r'<td><a class="list" href=.+?</a></td>', r.text)

    for i in it:
        s = re.findall(r'gitweb.+?;h=|Navi.+?</a>', i)
        print 'http://igerrit/' + s[0][:-3]
        filepath = re.split(r'/', s[1][:-4])
        print filepath[-1]
        
def getCookie(session):
    url = 'http://igerrit/login/#/q/status:open'
    data = {
        'username':'zhenglong',
        'password':'zl5026177'}
    
    r = session.post(url, data = data)
    return  r.request.headers.get('Cookie')

    

if __name__ == '__main__':
    session = requests.Session()
    cookie = getCookie(session)
    getUrl(session, cookie)
    
