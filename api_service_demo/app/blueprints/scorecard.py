#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Blueprint

from app.api import wrap_result, execute
from app.services import xjd_xyf_app_def_v1


scorecard_bp = Blueprint('scorecard', __name__)


@scorecard_bp.route('/api', methods=['GET', 'POST'])
@wrap_result
def api_index():
    # return {'code': -1, 'data': 'Api works!'}
    # return {'data': 'Api works!'}
    return 'Api works!'


@scorecard_bp.route('/api/<int:version>', methods=['GET', 'POST'])
@scorecard_bp.route('/api/<float:version>', methods=['GET', 'POST'])
@wrap_result
def api_version(version):
    return {'version': version}


@scorecard_bp.route('/api/scorecard', methods=['POST'])
@wrap_result
def scorecard_pingfenka():
    return execute(xjd_xyf_app_def_v1)
