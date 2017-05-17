# -*- coding: UTF-8 -*-
# !/usr/bin/python

import web
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time
import sys
from selenium.webdriver.support.ui import Select
import threading

class SDriver:
    def __init__(self):
        #添加自己的phantomjs的路径
        self.driver =  webdriver.PhantomJS(executable_path='/root/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.sync = False
        t = threading.Thread(target=self.d_init, args=())
        t.start()
    def d_init(self):
        while True:
            self.sync = True
            self.driver.get(
                "http://www.codingpy.com/")
            self.driver.find_element_by_id('userInput').send_keys("Singee77")
            self.driver.find_element_by_id('passwordInput').send_keys("codingpy")
            time.sleep(2)
            self.driver.find_element_by_id("login-button").submit()

            try:
                WebDriverWait(self.driver, 10)
            except:
                print '登录失败'
                sys.exit(0)
            self.sync = False
            print  "登陆成功", self.driver.title
            time.sleep(1*60*60)

    def get_context(self, code):
        print  self.sync
        if self.sync == True:
            return {'ret':1,'context':'landing'}
        self.driver.get("http://www.codingpy.com/?code=" + code)
        time.sleep(2)
        print self.driver.title
        element = self.driver.find_element_by_xpath("//td[@style='color:#669999; font-size:10pt']").text
        print code, element
        return  {'ret':0,'context':element}


    # URL 规则
urls = (
    '/app', 'hello'

)
# 应用程序
app = web.application(urls, globals())
sd = SDriver()

class hello:
    def GET(self):
        i = web.input(code='')
        value = sd.get_context(i.code)
        return json.dumps(value)

if __name__ == "__main__":

    print "开始登陆进程"
    app.run()
