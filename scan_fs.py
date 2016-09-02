#!/usr/bin/env python
# coding:utf-8  
# @Author: linkcheng
# function：scan a directory which you want.
# If you don't give one , it will sacn the current directory in one level deepth.

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

import platform
import os
import sys
import stat
import getopt

dir_count = 0
file_count = 0
path = '.'
last_dir = []

def usage():  
    print('''Usage: scan_fs [-h] [--help]
            [-d the directory which you want scan, it must be a real directory.]''')

def use_platform():
    sysstr = platform.system()
    if (sysstr == 'Linux'):
        pass
    else:
        print('This must be run on Linux system!')
        sys.exit(1)

def use_version():
    if '2.7' == sys.version[0:3]:
        pass
    else:
        print('This must be run in Python 2.7 version!')
        sys.exit(1)

def is_exe(full_name):
    if '1' == bin(int(oct(os.stat(full_name)[stat.ST_MODE])[-3:-2]))[-1]:
        return True
    else:
        return False

def print_file(fname):
    print('\033[0m'),
    print(fname)

def print_exe(ename):
    print('\033[1;32m'),
    print(ename),
    print('\033[0m')

def print_dir(dname):
    print('\033[1;34m'),
    print(dname),
    print('\033[0m')

def print_soc(sname):
    print('\033[1;35m'),
    print(sname),
    print('\033[0m')

def print_lnk(lname):
    print('\033[1;36m'),
    print(lname),
    print('\033[0m'),
    print('->'),

def separate_dir_file(items, d):
    '''separate dir and files, st: dirs always before files'''
    dir_list = []
    file_list = []

    for item in items:
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

def real_file(full_path, item):
    '''this will show the real file of link file '''
    global dir_count
    global file_count

    mode = os.stat(full_path).st_mode
    if os.path.isdir(full_path) : # dir
        dir_count += 1
        print_dir(item)
    elif os.path.isfile(full_path): # file
        file_count += 1
        if is_exe(full_path): # exe file
            print_exe(item)
        else: # non-exe file
            print_file(item)
    else: # others
        # socket file
        if stat.S_ISSOCK(mode):
            file_count += 1
            print_soc(item)
        else:
            pass

def build_tree(d):
    '''build file system tree'''
    global dir_count
    global file_count
    global last_dir
    b_last = 0

    # get dirs and files in a list.
    # In listdir(d), some conditions, there is a OSError, because of Permission denied
    try:
        items = os.listdir(d) 
    except OSError:
        print(d + ' Permission denied!')
        sys.exit(1)

    items_sum = len(items)

    #delete the '/' of the d if it has, e.g.: './'->'.''
    if d[-1] == '/' and len(d) > 1:
        d = d[:-1]

    # get all files and dirs in the dir
    for index, item in enumerate(sorted(items)): 
        full_path = d + '/'+ item
        mode = os.stat(full_path).st_mode

        # hide file
        if '.' == item[0] :
            continue

        # format the content
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
        if os.path.islink(full_path): # link fle
            print_lnk(item)
            real_file(full_path, item)
        elif os.path.isdir(full_path) : # dir
            dir_count += 1
            print_dir(item)
            # into a dir, so the lenth of the list + 1
            last_dir.append(b_last)
            # build file system tree
            build_tree(full_path)
            # back from a dir, so length - 1
            last_dir.pop()
        elif os.path.isfile(full_path): # file
            file_count += 1
            if is_exe(full_path): # exe file
                print_exe(item)
            else: # non-exe file
                print_file(item)
        else: # others
            # socket file
            if stat.S_ISSOCK(mode):
                file_count += 1
                print_soc(item)
            else:
                pass

def get_dir_cnt_tree(d = '.'):
    '''get dir content'''

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
    # if gives a dir directly
    elif options.has_key('-d'): 
        path = options['-d']
        # if the dir not exsit, exit the process
        if not os.path.isdir(path): 
            print('This is not real directory!');
            usage()
            sys.exit(1)
        else:
            tree()
    # only the default para
    else: 
        tree()
        
if "__main__" == __name__:
    use_platform()
    use_version()
    main()

    if dir_count > 1:
        print(str(dir_count) + ' directories, '),
    else:
        print(str(dir_count) + ' directory, '),

    if file_count > 1:
        print(str(file_count) + 'files')
    else:
        print(str(file_count) + 'file')
    
