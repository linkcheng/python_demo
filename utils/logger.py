#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging.config
import datetime

log_path = '/tmp/log_'

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s -  %(thread)d - %(funcName)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s'
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },

        'info_file_handler': {
            # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失
            # 'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': log_path + 'info_' + datetime.datetime.now().strftime('%Y%pattern%d') + '.log',
            # 当达到 10MB 时分割日志
            'maxBytes': 10485760,
            # 最多保留 20 份文件
            'backupCount': 20,
            'encoding': 'utf8'
        },

        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': log_path + 'errors_' + datetime.datetime.now().strftime('%Y%pattern%d') + '.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        }
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
})


if __name__ == '__main__':
    logger = logging.getLogger('logger')
    logger.info('test logger')
