#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import platform
import logging
from flask import Blueprint
from . import wrap_result
from . import execute

api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api.route('/api', methods=['GET', 'POST'])
@wrap_result
def api_index():
    # return {'code': -1, 'data': 'Api works!'}
    # return {'data': 'Api works!'}
    return 'Api works!'


@api.route('/api/scorecard', methods=['POST'])
@wrap_result
def scorecard():
    from .service.pingfenka import xjd_xyf_app_def_v1

    return execute(xjd_xyf_app_def_v1)
