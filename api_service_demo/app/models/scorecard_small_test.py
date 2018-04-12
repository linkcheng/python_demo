#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from peewee import *
from app.models.base_model import BaseModel


class ScorecardSmallTestModel(BaseModel):
    class Meta:
        db_table = 'ScorecardSmallTest'
        indexes = (
            (('id_card_number', ), False),
            (('mobile', ), False),
        )

    id = PrimaryKeyField()
    id_num_mapper_id = BigIntegerField(default=0, help_text='证件号')
    id_card_number = CharField(max_length=20, default='', help_text='证件号')
    mobile = CharField(max_length=20, default='', help_text='手机号')
    application_time = DateTimeField(null=True, help_text='申请时间')

    tongdun_status = SmallIntegerField(null=True)
    tongdun_25 = IntegerField(null=True)
    tongdun_4 = IntegerField(null=True)
    tongdun_14 = IntegerField(null=True)
    tongdun_41 = IntegerField(null=True)
    tongdun_259 = IntegerField(null=True)
    tongdun_120 = SmallIntegerField(null=True)
    tongdun_152 = IntegerField(null=True)
    tongdun_87 = SmallIntegerField(null=True)
    tongdun_136 = IntegerField(null=True)
    education = CharField(max_length=64, null=True)
    id_number_province = CharField(max_length=32, null=True)
    gender = SmallIntegerField(null=True)
    hj_3y_xfnl_5 = IntegerField(null=True)
    hj_3y_xfnl_score = IntegerField(null=True)
    contact_11 = SmallIntegerField(null=True)
    contact_10 = SmallIntegerField(null=True)
    call_record_600 = IntegerField(null=True)
    call_record_441 = IntegerField(null=True)
    pdl_credit_24 = DoubleField(null=True)

    score = DoubleField(default=0.0)
    prob = DoubleField(default=0.0)
    app_exception = TextField(null=True)
    n_tongdun_25 = IntegerField(default=0)
    n_education = FloatField(default=0.0)
    n_tongdun_4 = IntegerField(default=0)
    n_pdl_credit_24 = IntegerField(default=0)
    n_tongdun_120 = IntegerField(default=0)
    n_gender = SmallIntegerField(default=0)
    n_tongdun_41 = IntegerField(default=0)
    n_mobile_province_woe = FloatField(default=0.0)
    n_hj_3y_xfnl_5 = IntegerField(default=0)
    n_tongdun_87 = IntegerField(default=0)
    n_tongdun_259 = IntegerField(default=0.0)
    n_tongdun_152 = IntegerField(default=0)
    n_contact_11 = IntegerField(default=0)
    n_tongdun_136 = IntegerField(default=0)
    n_call_record_600 = IntegerField(default=0)
    n_call_record_441 = IntegerField(default=0)
    n_contact_10 = IntegerField(default=0)
    n_tongdun_14 = IntegerField(default=0)
