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
import re
import getopt
import argparse

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

def print_file(name):
    print('\033[0m'),
    print(name)

def print_exe(name):
    print('\033[1;32m'),
    print(name),
    print('\033[0m')

def print_blk(name):
    print('\033[1;33;40m'),
    print(''+name+''),
    print('\033[0m')

def print_dir(name):
    print('\033[1;34m'),
    print(name),
    print('\033[0m')

def print_soc(name):
    print('\033[1;35m'),
    print(name),
    print('\033[0m')

def print_lnk(name):
    print('\033[1;36m'),
    print(name),
    print('\033[0m'),
    print('->'),

def print_result():
    global dir_count
    global file_count

    if dir_count > 1:
        print('\n' + str(dir_count) + ' directories,'),
    else:
        print(str(dir_count) + ' directory,'),

    if file_count > 1:
        print(str(file_count) + ' files')
    else:
        print(str(file_count) + ' file')

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

def get_real_file_name(full_path, item):
    '''get the real file name of the link file'''
    global path
    # print("")

    # get the real file abs path of the link file
    abs_path = os.path.realpath(full_path) 
    # get the relate path, there is bug!!
    rel_path = os.path.relpath(abs_path, full_path)[3:]
    # print(abs_path)
    # print(rel_path)
    # if the real file in the dir is the same as the link file
    if re.match(path, rel_path):
        item = rel_path[len(path) + 1:]
    else:
        item = rel_path

    return abs_path, item

def real_file(full_path, item):
    '''If from a link file, this will show the real file of link file;
      If from a non-link file, will go normal '''
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
        # block file
        elif stat.S_ISBLK(mode) or stat.S_ISCHR(mode):
            file_count += 1
            print_blk(item)
        else:
            print(full_path)

def build_tree(d = '.'):
    '''build file system tree'''
    global dir_count
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
            full_path, item = get_real_file_name(full_path, item)
            # get_real_file_name(full_path, item)
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
        else:
            real_file(full_path, item)

def tree():
    global path
    print_dir(path)

    if path[-1] == '/' and len(path) > 1:
        path = path[:-1]

    build_tree(path)

def detail():
    pass

def start(p = '.', option = 't'):
    global path

    if not os.path.isdir(p): 
        print('This is not real directory!');
        usage()
        sys.exit(1)
    
    path = p

    if 'l' == option:
        detail()
    else:
        tree()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], ' t:hl:', ['help', ])
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(1)
    options = dict(opts)

    if options.has_key('-h') or options.has_key('--help'):
        usage()
        sys.exit(0)
    # if gives a dir directly
    elif options.has_key('-l'): 
        start(options['-l'], 'l')
        # if gives a dir directly
    elif options.has_key('-t'): 
        start(options['-t'], 't')
    # only the default para
    else: 
        start(sys.argv[1:][0])
        
if "__main__" == __name__:
    use_platform()
    use_version()

    main()
    
    print_result()
