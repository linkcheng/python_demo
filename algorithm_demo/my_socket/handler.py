#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: handler 
@date: 2020-06-13 
"""


class WriteHandler:

    def __call__(self, data, *args, **kwargs):
        return data.replace("吗", "").replace("?", "!").replace("？", "!")

