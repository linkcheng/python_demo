#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import shutil
import logging
from distutils.core import setup
from Cython.Build import cythonize
import logger

log = logging.getLogger('py2so')


def py2so(modules, build_dir='.', is_clear=True):
    """
    根据 modules 在 build_dir 下生成 .so 文件，
    并且删除中间生成的 .c 文件以及编译用到的 .o 文件，不支持 py 包编译
    :param modules: 要编译的 py 模块，type：list or str
    :param build_dir: 生成文件的目录；
        -b: 生成 .so 文件的目录；
        -t: 生成 .o 文件的目录，相对于要编译的 py 的目录
    :param is_clear: 是否清楚中间文件
    :return: None；
    simples: py2so('hello.py') -> hello.so
    :note: modules is not a valid module name：需要删除调用该接口的模块下 __init__.py 文件
    """
    if not isinstance(modules, (tuple, list)):
        modules = [modules]
    tmp_path = 'build'

    attrs = {
        'ext_modules': cythonize(modules),
        'script_args': ['build_ext', '-b', build_dir, '-t', tmp_path],
    }

    try:
        setup(**attrs)
    except Exception as ex:
        log.error(str(ex))

    # 删除临时文件
    if is_clear:
        cur_path = os.getcwd()
        tmp_dir = os.path.join(cur_path, tmp_path)
        # 删除 .o 文件
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        # 删除 .c 文件
        for py in modules:
            c_name = py[:-2] + 'c'
            if os.path.exists(c_name):
                os.remove(c_name)
