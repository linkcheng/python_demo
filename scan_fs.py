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
import sys
import getopt

dir_count = 0
file_count = 0
path = '.'
last_dir = []

def usage():  
    print '''Usage: scan_fs [-h] [--help]
            [-l the deep level you want to scan, it must be bigger than or equal to 0.]
            [-d the directory which you want scan, it must be a real directory.]'''

def print_file(fname):
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

def separate_dir_file(items, d):
    '''separate dir and files, st: dirs always before files'''
    dir_list = []
    file_list = []

    for item in items:
        '''divise dir and file and sort them'''
        p = d+'/'+item

        # separate dir and file
        if os.path.isdir(p) : # dir
            dir_list.append(item)
        elif os.path.isfile(p): # file
            file_list.append(item)
        else:
            pass

    items = sorted(dir_list) + sorted(file_list)
    return items

def build_tree(d):
    '''build file system tree'''
    global dir_count
    global file_count
    global last_dir
    b_last = 0

    # get dirs and files in a list.
    # In listdir(d), some conditions, there is a OSError, because of Permission denied
    items = os.listdir(d)    
    items_sum = len(items)

    #delete the '/' of the d if it has, e.g.: './'->'.''
    if d[-1] == '/' and len(d) > 1:
        d = d[:-1]

    # get all files and dirs in the dir
    for index, item in enumerate(sorted(items)): 
        p = d + '/'+ item

        # format the content, here a bug, watch out!!!
        for i in last_dir:
            if 1 == i:
                print('│   '),
            else:
                print('     '),

        if index == items_sum - 1:
            b_last = 0
            print('└──'),
        else:
            b_last = 1
            print('├──' ),

        # print content
        if os.path.isdir(p) : # dir
            dir_count += 1
            print_dir(item)
            # into a dir, so the lenth of the list + 1
            last_dir.append(b_last)
            # 
            build_tree(p)
            # back from a dir, so length - 1
            last_dir.pop()
        elif os.path.isfile(p): # file
            file_count += 1
            print_file(item)
        else: # others
            pass

def get_dir_cnt_tree(d = '.'):
    '''get dir content'''

    # #delete the '/' of the d if it has, e.g.: './'->'.''
    # if d[-1] == '/' and len(d) > 1:
    #     d = d[:-1]
    # # get dirs and files in a list
    # items = os.listdir(d)
    # # separate dir and files, st: dirs always before files
    # items = separate_dir_file(items, d)
    # # build fs tree
    # build_tree(items, d)
    build_tree(d)



def tree():
    global path
    print_dir(path)

    if path[-1] == '/' and len(path) > 1:
        path = path[:-1]

    get_dir_cnt_tree(path)

def main():
    global path
    opts, args = getopt.getopt(sys.argv[1:], 'd:', ['help', ])
    options = dict(opts)
    
    if options.has_key('-h') or options.has_key('--help'):
        usage()
        sys.exit(1)
    elif options.has_key('-d'): # if gives a dir directly
        path = options['-d']

        if not os.path.isdir(path): # if the dir not exsit, exit the process
            print('This is not real directory!');
            usage()
            sys.exit(1)
        else:
            tree()
    else: # only the default para
        tree()
        

if "__main__" == __name__:
    main()

    if dir_count >= 1:
        print(str(dir_count) + ' directories, '),
    else:
        print(str(dir_count) + ' directory, '),

    if file_count >= 1:
        print(str(file_count) + 'files')
    else:
        print(str(file_count) + 'file')
    
