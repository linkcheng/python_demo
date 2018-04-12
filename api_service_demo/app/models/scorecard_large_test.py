#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from peewee import *
from app.models.base_model import BaseModel


class ScorecardLargeTestModel(BaseModel):
    class Meta:
        db_table = 'ScorecardLargeTest'
        indexes = (
            (('id_card_number', ), False),
            (('mobile', ), False),
        )

    id = PrimaryKeyField()
    id_num_mapper_id = BigIntegerField(default=0, help_text='证件号')
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
