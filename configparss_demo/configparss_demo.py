#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import sys,os
import ConfigParser

def config_parse(file_name):
    ini_dict = {}
    with open(file_name) as f:
        for line in f.readlines():
            if line.strip() is not '' and '[' not in line:
                v = line.strip().split('=')
                ini_dict[v[0].strip()] = v[1].strip()

    return ini_dict


class Connector:  
  def __init__(self, config_file_path):  
    cf = ConfigParser.ConfigParser()  
    cf.read(config_file_path)  
  
    s = cf.sections()  
    print 'section:', s  
  
    o = cf.options("baseconf")  
    print 'options:', o  
  
    v = cf.items("baseconf")  
    print 'items:', v  
  
    host = cf.get("baseconf", "host")  
    port = cf.getint("baseconf", "port")  
    user = cf.get("baseconf", "user")  
    pwd = cf.get("baseconf", "password")  
  
    print host, port, user, pwd  
  
    cf.set("baseconf", "db_pass", "12345678")  
    with open(config_file_path, "w") as f:
        cf.write(f) 

if __name__ == '__main__':
    d = config_parse('./config.ini')
    print(d)
    
    Connector("./config.ini")
