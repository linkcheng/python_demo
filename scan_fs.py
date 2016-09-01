#!/usr/bin/env python
# coding:utf-8  
# @Author: linkcheng
# function：scan a directory which you want.
# If you don't give one , it will sacn the root directory in one level deepth.

 #  格式：\033[显示方式;前景色;背景色m
 # 说明：
 # 前景色            背景色           颜色
 # ---------------------------------------
 # 30                40              黑色
 # 31                41              红色
 # 32                42              绿色
 # 33                43              黃色
 # 34                44              蓝色
 # 35                45              紫红色
 # 36                46              青蓝色
 # 37                47              白色
 # 显示方式           意义
 # -------------------------
 # 0                终端默认设置
 # 1                高亮显示
 # 4                使用下划线
 # 5                闪烁
 # 7                反白显示
 # 8                不可见
  
 # 例子：
 # \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
 # \033[0m          <!--采用终端默认设置，即取消颜色设置-->

import os
import re
import sys
import subprocess
import getopt
import logging
import requests
import time
from multiprocessing import Process, Queue 
from functools import wraps

def usage():  
    print '''Usage: scan_fs [-h] [--help]
            [-l the deep level you want to scan, it must be bigger than or equal to 0.]
            [-d the directory which you want scan, it must be a real directory.]'''

def print_txt(fname):
    print('\033[0m'),
    print(fname)

def print_dir(dname):
    print('\033[1;34m'),
    print(dname),
    print('\033[0m')

def print_exe(ename):
    print('\033[1;32m'),
    print(ename),
    print('\033[0m')

def print_only_files_in_dir(fnames):
        sum = len(fnames)
        for index, fname in enumerate(fnames): # 输出文件信息
            if index == sum - 1:
                print(' └──'),
            else:
                print(' ├──' ),

            print_txt(fname)

def print_only_dirs_in_dir(dnames):
        sum = len(dnames)
        for index, dname in enumerate(dnames): # 输出文件信息
            if index == sum - 1:
                print(' └──'),
            else:
                print(' ├──' ),

            print_dir(dname)

def get_dir_cnt(d = '.'):
    # os.system("tree " + d)
    print_dir(d)
    items = os.listdir(d) 

    for item in os.listdir(d): # get all files and dirs in the dir
        print item,
        if isdir(item) :
            print ' is a dir'
        elif isfile(item):
            print ' is a file'
        elif islink(item):
            print ' is a link'
        else:
            print ' is others'


    # for parent,dirnames,filenames in os.walk(d): # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    #     print_only_dirs_in_dir(dirnames)
    #     print_only_files_in_dir(filenames)


def main():
    opts, args = getopt.getopt(sys.argv[1:], 'd:', ['help', ])
    options = dict(opts)
    
    if options.has_key('-h') or options.has_key('--help'):
        usage()
        sys.exit(1)
    elif options.has_key('-d'): # if gives a dir directly
        d = options['-d']

        if not os.path.isdir(d): # if the dir not exsit, exit the process
            print('This is not real directory!');
            usage()
            sys.exit(1)
        else:
            get_dir_cnt(d)
    else: # only the default para
        get_dir_cnt()

if "__main__" == __name__:
    main()
