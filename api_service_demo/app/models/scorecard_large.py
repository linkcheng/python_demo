#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from peewee import *
from app.models.base_model import BaseModel


class ScorecardLargeModel(BaseModel):
    class Meta:
        # the name of the database table this model maps to
        db_table = 'ScorecardLarge'
        # create a non-unique on biz_flow_number
        indexes = (
            (('biz_flow_number', ), False),
        )

    id = PrimaryKeyField()
    biz_flow_number = CharField(max_length=32, default='', help_text='业务流水号')
    id_card_number = CharField(max_length=20, default='', help_text='证件号')
    mobile = CharField(max_length=20, default='', help_text='手机号')
    activation_time = DateTimeField(null=True, help_text='激活时间')

    yys_report_1074 = FloatField(null=True)
    tongdun_58 = IntegerField(null=True)
    phone_number_province = CharField(max_length=32, null=True)
    call_record_2 = IntegerField(null=True)
    gender = SmallIntegerField(null=True)
    source_type = CharField(max_length=8, default='')
    tongdun_7 = IntegerField(null=True)
    hj_1y_xfnl_5 = IntegerField(null=True)
    jd_market_persona_3 = IntegerField(null=True)
    tongdun_121 = IntegerField(null=True)
    qq_length = IntegerField(null=True)
    contact_10 = IntegerField(null=True)
    yys_report_404 = IntegerField(null=True)
    tongdun_125 = IntegerField(null=True)
    jd_shop_persona_9 = CharField(max_length=64, null=True)
    yys_report_793 = IntegerField(null=True)
    tongdun_18 = IntegerField(null=True)
    call_record_452 = IntegerField(null=True)
    monthly_income = CharField(max_length=64, null=True)
    tongdun_85 = BooleanField(null=True)
    tongdun_152 = IntegerField(null=True)

    cashloan_ab_risk_score = DoubleField(default=0.0)
    cashloan_ab_risk_prob = DoubleField(default=0.0)
    n_c_yys_report_1074 = FloatField(default=0.0)
    n_tongdun_58 = IntegerField(default=0)
    n_c_phone_number_province = FloatField(default=0.0)
    n_c_call_record_2 = FloatField(default=0.0)
    n_gender = IntegerField(default=0)
    n_android_callrecord_m = IntegerField(default=0)
    n_c_tongdun_7 = FloatField(default=0.0)
    n_c_hj_1y_xfnl_5 = FloatField(default=0.0)
    n_c_jd_market_persona_3 = FloatField(default=0.0)
    n_c_tongdun_121 = FloatField(default=0.0)
    n_qq_length = IntegerField(default=0)
    n_c_contact_10 = FloatField(default=0.0)
    n_yys_report_404 = IntegerField(default=0)
    n_tongdun_125 = IntegerField(default=0)
    n_high_ind3 = IntegerField(default=0)
    n_yys_report_793 = IntegerField(default=0)
    n_c_tongdun_18 = FloatField(default=0.0)
    n_call_record_452 = IntegerField(default=0)
    n_monthly_income_ind = IntegerField(default=0)
    n_tongdun_85 = IntegerField(default=0)
    n_tongdun_152 = IntegerField(default=0)


if __name__ == '__main__':
    from app.models import db

    db.create_tables([ScorecardLargeModel], safe=True)
    vals = {
        'biz_flow_number': '201802281823441093387',
        'mobile': 1000013,
        'active_time': '2018-02-28 18:23:44',

        'call_record_2': None,
        'call_record_452': None,
        'contact_10': 7,
        'gender': 0,
        'hj_1y_xfnl_5': 4,
        'id_card_number': 1000012,
        'jd_market_persona_3': None,
        'jd_shop_persona_9': None,
        'monthly_income': '>=6,000',
        'phone_number_province': '山西',
        'qq_length': 9,
        'source_type': 'ios',
        'tongdun_121': None,
        'tongdun_125': None,
        'tongdun_152': None,
        'tongdun_18': None,
        'tongdun_58': None,
        'tongdun_7': None,
        'tongdun_85': 0,
        'yys_report_1074': None,
        'yys_report_404': None,
        'yys_report_793': None,

        'cashloan_ab_risk_score': 10.0,
        'cashloan_ab_risk_prob': 11.0,
        'n_c_yys_report_1074': 1.1,
        'n_tongdun_58': 0,
        'n_c_phone_number_province': 2.2,
        'n_c_call_record_2': 3.3,
        'n_gender': 0,
        'n_android_callrecord_m': 0,
        'n_c_tongdun_7': 4.4,
        'n_c_hj_1y_xfnl_5': 5.5,
        'n_c_jd_market_persona_3': 6.6,
        'n_c_tongdun_121': 7.7,
        'n_qq_length': 0,
        'n_c_contact_10': 8.8,
        'n_yys_report_404': 0,
        'n_tongdun_125': 0,
        'n_high_ind3': 0,
        'n_yys_report_793': 0,
        'n_c_tongdun_18': 9.9,
        'n_call_record_452': 0,
        'n_monthly_income_ind': 0,
        'n_tongdun_85': 0,
        'n_tongdun_152': 0,
    }
    ScorecardLargeModel.create(**vals)
    # ScorecardLargeModel.update(id_card_number='11111111').where(ScorecardLargeModel.id == 1).execute()
    # domain = (ScorecardLargeModel.id_card_number == '11111111')
    # query = ScorecardLargeModel.select().where(domain).dicts().execute()
    # ret = ScorecardLargeModel.get_one((ScorecardLargeModel.id_card_number=='11111111')&(ScorecardLargeModel.mobile=='10086'))
    # print(ret)
