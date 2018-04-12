#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
import dateutil.parser
from datetime import datetime, timedelta
from flask import request

from app.api import wrap_result
from app.controllers.scorecard_base import compute_gender, compute_id_number_province, find_values
from app.controllers.scorecard_small_ol import handle_with_flow_number, handle_no_flow_number
from app.controllers.scorecard_small_ol import create_scorecard_small
from app.controllers.scorecard_small_no_bfn import create_scorecard_small_test
from app.controllers.scorecard_small_no_bfn import find_application_info
from app.controllers.scorecard_small_no_bfn import handle_no_bfn, get_pdl_credit_24
from app.blueprints.scorecard import scorecard_bp
from app.services import paydayloan_p
from common.utils import FMT

logger = logging.getLogger(__name__)


@scorecard_bp.route('/api/scorecard_small', methods=['POST'])
@wrap_result
def scorecard_small():
    """
    小额申请阶段评分接口
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

    gender = compute_gender(id_card_number)
    id_number_province = compute_id_number_province(id_card_number)
    expired_time = datetime.strptime(created_time_str, FMT) + timedelta(days=1)

    value1 = handle_with_flow_number(biz_flow_number)
    value2 = handle_no_flow_number(mobile, expired_time)

    tongdun_value = value1.get('tongdun')
    hangju_value = value1.get('hangju')
    challenge_value = value1.get('challenge')
    contact_value = value2.get('contact')
    call_record_value = value2.get('call_record')

    kwargs = {
        'id_card_number': None,
        'gender': gender,
        'id_number_province': id_number_province,

        'tongdun_status': tongdun_value.get('tongdun_status', 1),
        'tongdun_25': tongdun_value.get('tongdun_25'),
        'tongdun_4': tongdun_value.get('tongdun_4'),
        'tongdun_14': tongdun_value.get('tongdun_14'),
        'tongdun_41': tongdun_value.get('tongdun_41'),
        'tongdun_259': tongdun_value.get('tongdun_259'),
        'tongdun_120': tongdun_value.get('tongdun_120'),
        'tongdun_152': tongdun_value.get('tongdun_152'),
        'tongdun_87': tongdun_value.get('tongdun_87'),
        'tongdun_136': tongdun_value.get('tongdun_136'),

        'hj_3y_xfnl_5': hangju_value.get('hj_3y_xfnl_5'),
        'hj_3y_xfnl_score': hangju_value.get('hj_3y_xfnl_score'),

        'contact_10': contact_value.get('contact_10'),
        'contact_11': call_record_value.get('contact_11'),
        'call_record_600': call_record_value.get('call_record_600'),
        'call_record_441': call_record_value.get('call_record_441'),

        'education': challenge_value.get('education'),
        'pdl_credit_24': req_json.get('pdl_credit_24'),
    }
    logger.info(kwargs)

    try:
        result = paydayloan_p(**kwargs)
    except Exception as e:
        logger.error(str(e))
        ret = {'code': -1, 'data': 'Execute Error !'}
    else:
        logger.info(result)
        ret = {
            'score': result.get('score'),
            'prob': result.get('prob'),
        }

        result.update(kwargs)
        result.update({
            'biz_flow_number': biz_flow_number,
            'id_card_number': id_card_number,
            'mobile': mobile,
            'application_time': created_time_str,
        })
        create_scorecard_small(**result)

    return ret


@scorecard_bp.route('/api/test/scorecard_small', methods=['POST'])
@wrap_result
def scorecard_small_no_bfn():
    """
    小额申请阶段评分接口
    :return:
    """
    req_json = request.json
    logger.info('req_json: %s' % req_json)

    columns = ['mobile', 'name', 'created_time']
    mapper_cols = ['id_card_number', 'mobile', 'name']

    vals = find_values([req_json.get(col) for col in mapper_cols if col in req_json])
    values = {val.get('type'): val.get('key') for val in vals}
    id_num = values.pop('id_no') if 'id_no' in values else None
    if not id_num:
        return {'code': 1, 'data': 'Id card number Error !'}

    info = {
        **{col: req_json.get(col) for col in columns if col in req_json},
        **values,
    }

    search_columns = list(set(columns) - set(info.keys()))
    if search_columns:
        search_info = find_application_info(id_num, search_columns)
        info.update(search_info)

    mobile = info.get('mobile')
    if not mobile:
        return {'code': 2, 'data': 'Mobile can not be found !'}

    logger.info(id_num)
    logger.info(info)
    name = info.get('name')
    created_time = dateutil.parser.parse(str(info.get('created_time')))
    created_time_str = datetime.strftime(created_time, FMT)

    value1 = handle_no_bfn(id_num, mobile, name, created_time)
    gender = compute_gender(id_num)
    id_number_province = compute_id_number_province(id_num)

    pdl_credit_24 = req_json.get('pdl_credit_24')
    if not pdl_credit_24:
        pdl_credit_24 = get_pdl_credit_24(id_num, created_time)

    tongdun_value = value1.get('tongdun')
    logger.info(tongdun_value)
    hangju_value = value1.get('hangju')
    challenge_value = value1.get('challenge')
    contact_value = value1.get('contact')
    call_record_value = value1.get('call_record')

    kwargs = {
        'id_card_number': None,
        'gender': gender,
        'id_number_province': id_number_province,

        'tongdun_status': tongdun_value.get('tongdun_status', 1),
        'tongdun_25': tongdun_value.get('tongdun_25'),
        'tongdun_4': tongdun_value.get('tongdun_4'),
        'tongdun_14': tongdun_value.get('tongdun_14'),
        'tongdun_41': tongdun_value.get('tongdun_41'),
        'tongdun_259': tongdun_value.get('tongdun_259'),
        'tongdun_120': tongdun_value.get('tongdun_120'),
        'tongdun_152': tongdun_value.get('tongdun_152'),
        'tongdun_87': tongdun_value.get('tongdun_87'),
        'tongdun_136': tongdun_value.get('tongdun_136'),

        'hj_3y_xfnl_5': hangju_value.get('hj_3y_xfnl_5'),
        'hj_3y_xfnl_score': hangju_value.get('hj_3y_xfnl_score'),

        'contact_10': contact_value.get('contact_10'),
        'contact_11': contact_value.get('contact_11'),
        'call_record_600': call_record_value.get('call_record_600'),
        'call_record_441': call_record_value.get('call_record_441'),

        'education': challenge_value.get('education'),
        'pdl_credit_24': pdl_credit_24,
    }
    logger.info(kwargs)

    try:
        result = paydayloan_p(**kwargs)
    except Exception as e:
        logger.exception(e)
        # logger.error(str(e))
        result = {'code': -1, 'data': 'Execute Error !'}
    else:
        logger.info(result)
        result.update(kwargs)
        result.update({
            'id_num_mapper_id': req_json.get('id_card_number'),
            'id_card_number': id_num,
            'mobile': mobile,
            'application_time': created_time_str,
        })
        create_scorecard_small_test(**result)

    return result
