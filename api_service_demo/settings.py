#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '338329e337970b6c7f5828367dc8bc11'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


def load_system_config():
    sys_config = {}

    try:
        config_file = open('config.yaml')
    except FileNotFoundError as e:
        pass
    else:
        sys_config = yaml.load(config_file)

        config_file.close()

    return sys_config


app_config = {
    # 'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,
    'default': Config,
}

system_config = load_system_config()
