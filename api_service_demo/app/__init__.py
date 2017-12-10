#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
from functools import wraps
from datetime import timedelta
from flask import Flask
from flask import jsonify
from flask import request
from settings import app_config

logger = logging.getLogger(__name__)


def create_app(config_name):
    app = Flask(__name__)

    from .service_api import api

    app.register_blueprint(api)
    app.config.from_object(app_config[config_name])
    app.permanent_session_lifetime = timedelta(minutes=5)

    return app


def wrap_result(fn):
    """
    返回 json 类型格式数据
    :return: {code: 0, data {}}
    """

    @wraps(fn)
    def _wrap(*args, **kwargs):
        ret = fn(*args, **kwargs)
        if isinstance(ret, (dict, )):
            if 'code' in ret:
                data = ret
            else:
                data = {'code': 0, 'data': ret}
        else:
            data = {'code': 0, 'data': ret}
        return jsonify(data)

    return _wrap


def execute(fun):
    logger.info('function name = '+fun.__name__)
    logger.info(request.json)

    try:
        ret = fun(**request.json)
    except Exception as e:
        logger.error(str(e))
        ret = {'code': -1, 'data': 'Execute Error !'}

    logger.info(ret)
    return ret
