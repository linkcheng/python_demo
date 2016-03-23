#!/usr/bin/env python
#coding:utf-8

import logging

infoFormat = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'


infoLogName = '/tmp/gcid.log'

infoFormatter = logging.Formatter(infoFormat)
infoLogger = logging.getLogger("infoLog")

infoLogger.setLevel(logging.DEBUG)

infoHandler = logging.FileHandler(infoLogName, 'a')
infoHandler.setLevel(logging.INFO)
infoHandler.setFormatter(infoFormatter)
 
debugHandler = logging.StreamHandler()
debugHandler.setLevel(logging.DEBUG)
 
infoLogger.addHandler(infoHandler)
infoLogger.addHandler(debugHandler)


infoLogger.debug("debug message")

infoLogger.info("info message")

infoLogger.warn("warn message")


