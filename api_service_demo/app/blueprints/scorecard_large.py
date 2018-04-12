#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
import dateutil.parser
from datetime import datetime, timedelta
from flask import request

from app.api import wrap_result
from app.controllers.scorecard_base import compute_gender, compute_mobile_province, find_value
from app.controllers.scorecard_large_base import find_source_type
from app.controllers.scorecard_large_ol import handle_no_flow_number
from app.controllers.scorecard_large_ol import create_scorecard_large, handle_with_flow_number
from app.controllers.scorecard_large_no_bfn import find_activation_info
from app.controllers.scorecard_large_no_bfn import create_scorecard_large_test, handle_no_bfn
from app.blueprints.scorecard import scorecard_bp
from app.services import cashloan_ab_m1
from common.utils import FMT

logger = logging.getLogger(__name__)


@scorecard_bp.route('/api/scorecard_large', methods=['POST'])
@wrap_result
def scorecard_large():
    """
    大额激活阶段评分接口
    :return:
    """
    req_json = request.json
    logger.info('req_json: %s' % req_json)

    biz_flow_number = req_json.get('biz_flow_number')
    if not biz_flow_number:
        return {'code': 1, 'data': 'biz_flow_number Error !'}
    id_card_number = req_json.get('id_card_number')
    mobile = req_json.get('mobile')
    created_time_str = req_json.get('created_time')
    source_type = find_source_type(id_card_number, created_time_str)
    expired_time = datetime.strptime(created_time_str, FMT) + timedelta(days=1)

    value1 = handle_with_flow_number(biz_flow_number)
    value2 = handle_no_flow_number(id_card_number, mobile, expired_time)

    gender = compute_gender(id_card_number)
    phone_number_province = compute_mobile_province(mobile)

    tongdun_value = value1.get('tongdun')
    jingdong_value = value1.get('jingdong')
    hangju_value = value1.get('hangju')

    challenge_value = value2.get('challenge')
    yys_value = value2.get('yys')
    contact_value = value2.get('contact')
    call_record_value = value2.get('call_record')

    kwargs = {
        'id_card_number': None,
        'gender': gender,
        'source_type': source_type,
        'phone_number_province': phone_number_province,

        'tongdun_7': tongdun_value.get('tongdun_7'),
        'tongdun_18': tongdun_value.get('tongdun_18'),
        'tongdun_58': tongdun_value.get('tongdun_58'),
        'tongdun_85': tongdun_value.get('tongdun_85'),
        'tongdun_121': tongdun_value.get('tongdun_121'),
        'tongdun_125': tongdun_value.get('tongdun_125'),
        'tongdun_152': tongdun_value.get('tongdun_152'),

        'jd_market_persona_3': jingdong_value.get('jd_market_persona_3'),
        'jd_shop_persona_9': jingdong_value.get('jd_shop_persona_9'),
        'hj_1y_xfnl_5': hangju_value.get('hj_1y_xfnl_5'),

        'yys_report_793': yys_value.get('yys_report_793'),
        'yys_report_404': yys_value.get('yys_report_404'),
        'yys_report_1074': yys_value.get('yys_report_1074'),

        'monthly_income': challenge_value.get('monthly_income'),
        'qq_length': challenge_value.get('qq_length'),
        'contact_10': contact_value.get('contact_10'),
        'call_record_2': call_record_value.get('call_record_2'),
        'call_record_452': call_record_value.get('call_record_452'),
    }
    logger.info(kwargs)

    try:
        result = cashloan_ab_m1(**kwargs)
    except Exception as e:
        logger.error(str(e))
        ret = {'code': -1, 'data': 'Execute Error !'}
    else:
        logger.info(result)
        ret = {
            'cashloan_ab_risk_score': result.get('cashloan_ab_risk_score'),
            'cashloan_ab_risk_prob': result.get('cashloan_ab_risk_prob'),
        }

        result.update(kwargs)
        result.update({
            'biz_flow_number': biz_flow_number,
            'id_card_number': id_card_number,
            'mobile': mobile,
            'activation_time': created_time_str,
        })
        create_scorecard_large(**result)

    return ret


@scorecard_bp.route('/api/test/scorecard_large', methods=['POST'])
@wrap_result
def scorecard_large_no_bfn():
    """
    大额激活阶段评分接口，没有 biz_flow_number
    :return:
    """
    req_json = request.json
    logger.info('req_json: %s' % req_json)

    id_num_mapper_id = req_json.get('id_card_number')
    id_num = find_value(id_num_mapper_id)
    if not id_num:
        return {'code': 1, 'data': 'Id card number Error !'}

    mapper_cols = ['mobile', 'name']
    columns = ['mobile', 'name', 'row_crt_ts']
    info = {
        **{col: req_json.get(col) for col in columns if col in req_json},
        **{col: find_value(req_json.get(col)) for col in mapper_cols if col in req_json},
    }

    search_columns = list(set(columns) - set(info.keys()))
    if search_columns:
        search_info = find_activation_info(id_num, search_columns)
        info.update(search_info)

    mobile = info.get('mobile')
    if not mobile:
        return {'code': 2, 'data': 'Mobile can not be found !'}

    name = info.get('name')
    created_time = dateutil.parser.parse(str(info.get('row_crt_ts')))

    created_time_str = datetime.strftime(created_time, FMT)
    source_type = find_source_type(id_num, created_time_str)
    value1 = handle_no_bfn(id_num, mobile, name, created_time)

    gender = compute_gender(id_num)
    phone_number_province = compute_mobile_province(mobile)

    yys_value = value1.get('yys')
    tongdun_value = value1.get('tongdun')
    jingdong_value = value1.get('jingdong')
    hangju_value = value1.get('hangju')
    challenge_value = value1.get('challenge')
    contact_value = value1.get('contact')
    call_record_value = value1.get('call_record')

    kwargs = {
        'id_card_number': None,
        'gender': gender,
        'source_type': source_type,
        'phone_number_province': phone_number_province,

        'tongdun_7': tongdun_value.get('tongdun_7'),
        'tongdun_18': tongdun_value.get('tongdun_18'),
        'tongdun_58': tongdun_value.get('tongdun_58'),
        'tongdun_85': tongdun_value.get('tongdun_85', 0),
        'tongdun_121': tongdun_value.get('tongdun_121'),
        'tongdun_125': tongdun_value.get('tongdun_125'),
        'tongdun_152': tongdun_value.get('tongdun_152'),

        'jd_market_persona_3': jingdong_value.get('jd_market_persona_3'),
        'jd_shop_persona_9': jingdong_value.get('jd_shop_persona_9'),
        'hj_1y_xfnl_5': hangju_value.get('hj_1y_xfnl_5'),

        'yys_report_793': yys_value.get('yys_report_793'),
        'yys_report_404': yys_value.get('yys_report_404'),
        'yys_report_1074': yys_value.get('yys_report_1074'),

        'monthly_income': challenge_value.get('monthly_income'),
        'qq_length': challenge_value.get('qq_length'),
        'contact_10': contact_value.get('contact_10'),
        'call_record_2': call_record_value.get('call_record_2'),
        'call_record_452': call_record_value.get('call_record_452'),
    }
    logger.info(kwargs)

    try:
        result = cashloan_ab_m1(**kwargs)
    except Exception as e:
        logger.error(str(e))
        result = {'code': -1, 'data': 'Execute Error !'}
    else:
        logger.info(result)
        result.update(kwargs)
        result.update({
            'id_num_mapper_id': id_num_mapper_id,
            'id_card_number': id_num,
            'mobile': mobile,
            'activation_time': created_time_str,
        })
        create_scorecard_large_test(**result)

    return result
