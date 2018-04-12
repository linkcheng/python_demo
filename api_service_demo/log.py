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
            'format': '%(asctime)s %(levelname)s %(filename)s line:%(lineno)d %(message)s'}
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
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'level': 'INFO',
    'formatter': 'simple',
    'when': 'D',
    'encoding': 'utf8'
}

error_file_handler = {
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'level': 'ERROR',
    'formatter': 'simple',
    'when': 'D',
    'encoding': 'utf8'
}


def configure_logging():
    log_path = system_config.get('log_path') or default_log_path
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    info_file_name = os.path.join(log_path, 'info.log')
    error_file_name = os.path.join(log_path, 'error.log')

    info_file_handler.update(filename=info_file_name)
    error_file_handler.update(filename=error_file_name)

    default_logging_config['handlers']['info_file_handler'] = info_file_handler
    default_logging_config['handlers']['error_file_handler'] = error_file_handler

    logging.config.dictConfig(default_logging_config)


if __name__ == '__main__':
    configure_logging()
    logger = logging.getLogger('logger')
    logger.info('test logger')
