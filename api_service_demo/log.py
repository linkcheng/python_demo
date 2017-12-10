#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import os.path
import logging.config
from datetime import datetime
from settings import system_config

default_log_path = '/tmp/log/'

default_logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)-8s %(pathname)s[line:%(lineno)d] %(message)s'        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },

    },

    'loggers': {
        'my_module': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': 'no'
        }
    },

    'root': {
        'level': 'INFO',
        'handlers': ['console', 'info_file_handler', 'error_file_handler']
    }
}

info_file_handler = {
    # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失
    # 'class': 'cloghandler.ConcurrentRotatingFileHandler',
    'class': 'logging.handlers.RotatingFileHandler',
    'level': 'INFO',
    'formatter': 'simple',
    # 当达到 10MB 时分割日志
    'maxBytes': 10485760,
    # 最多保留 20 份文件
    'backupCount': 20,
    'encoding': 'utf8'
}

error_file_handler = {
    'class': 'logging.handlers.RotatingFileHandler',
    'level': 'ERROR',
    'formatter': 'simple',
    'maxBytes': 10485760,
    'backupCount': 20,
    'encoding': 'utf8'
}


def configure_logging():
    log_path = system_config.get('log_path') or default_log_path
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    info_file_name = os.path.join(log_path, 'info_'+datetime.now().strftime('%Y%m%d')+'.log')
    error_file_name = os.path.join(log_path, 'error_'+datetime.now().strftime('%Y%m%d')+'.log')

    info_file_handler.update(filename=info_file_name)
    error_file_handler.update(filename=error_file_name)

    default_logging_config['handlers']['info_file_handler'] = info_file_handler
    default_logging_config['handlers']['error_file_handler'] = error_file_handler

    logging.config.dictConfig(default_logging_config)


if __name__ == '__main__':
    configure_logging()
    logger = logging.getLogger('logger')
    logger.info('test logger')
