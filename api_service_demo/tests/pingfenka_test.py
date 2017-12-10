#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests


def xjd_xyf_app_def_v1_test():
    url = 'http://127.0.0.1:8000/api/scorecard'
    params = {
        'biz_flow_number': '郭自龙|622224198709071515|18209364411',
        'id_card_number': '622224198709071515',
        'name': '郭自龙',
        'mobile': 18209364411,
        'consumption_capacity_score_1y': -1,
        'consumption_capacity_score_3y': 1.0,
        'behaviour_score_1y': -1,
        'behaviour_score_3y': None,
        'jd_bt_credit_score': 651.0,
        'jd_loan_pre_loan_scr': -999.0,
        'jd_market_persona_price_sensitivity_scr': 0,
        'mobile_province': 62,
        'sex': 1,
        'source_type': 'android'
    }
    cnt = requests.post(url=url, json=params)
    print(cnt.text)


if __name__ == '__main__':
    xjd_xyf_app_def_v1_test()
