#!/usr/bin/env python
#coding:utf-8

import requests
import re


url = 'http://igerrit/gitweb?p=Doc/17Model/17Cy/21_UI.git;a=commit;h=3f34ceaffe6b4e94d46fa781533ca79b0ffef09c'

headers = {'Cookie':'GerritAccount=aRAqprrpNrRmhO5jQ0hM6dKcbzp08Bek2G'}

r = requests.request('GET', url, headers = headers)

it = re.findall(r'<td><a class="list" href=.+?</a></td>', r.text)

for i in it:
    s = re.findall(r'gitweb.+?;h=|Navi.+?</a>', i)
    print 'http://igerrit/' + s[0][:-3]
    filepath = re.split(r'/', s[1][:-4])
    print filepath[-1]
    print '\n'
