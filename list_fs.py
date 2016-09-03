#!/usr/bin/env python
# coding:utf-8  

import os  
import re  
import sys  
 
def get_file_size(path):  
    return os.path.getsize(path)  

def format_file_size(byte):  
    if byte <= 2**12:  # B  
        size = byte
        unit = ' B'
    elif byte < 2**21:  # KB
        size = float(byte)/2**10
        unit = ' KB'
    elif byte < 2**30:  # MB
        size = float(byte)/2**20
        unit = ' MB'
    else:  # GB
        size = float(byte)/2**30
        unit = ' GB'

    return size,unit

if "__main__" == __name__:
    path = os.getcwd()  
    total_size = 0  
    file_list = os.listdir(path)  

    for file_name in file_list:  
        abs_path = os.path.join(path, file_name)  
        file_size = get_file_size(abs_path)  
  
        total_size += file_size  
        fmt_size, unit = format_file_size(file_size)

        print((str(float('%.2f' % fmt_size)).rjust(7) + unit).ljust(12) + file_name)

    fmt_size, unit = format_file_size(total_size)
    print('\ntotal size: ' + str(float('%6.2f' % fmt_size)) + unit)
