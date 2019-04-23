#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pandas as pd
from pandas import isna
import pymysql
from DBUtils.PooledDB import PooledDB


def merge():
    df_ret = pd.read_excel('ret.xlsx')
    df_src = pd.read_excel('src.xlsx')

    # df_src = df_src.drop_duplicates()
    result = pd.merge(df_src, df_ret, how='left')

    writer = pd.ExcelWriter('ret_src1.xlsx', engine='xlsxwriter')
    result.to_excel(writer, 'Sheet1')
    writer.save()


def concat(score_field_name='cashloan_ab_risk_score'):
    df_ret = pd.read_excel('ret.xlsx')
    df_src = pd.read_excel('src.xlsx')

    id_nums = df_ret['id_card_number']
    df_src_valid = df_src[df_src['id_card_number'].isin(id_nums)]

    cols = ['id_card_number', 'src', 'ret']
    result = pd.DataFrame(columns=cols)
    result['id_card_number'] = id_nums
    result['src'] = df_src_valid[score_field_name]
    result['ret'] = df_ret[score_field_name]
    result['diff'] = abs(df_src_valid[score_field_name] - df_ret[score_field_name])
    result.set_index('id_card_number')

    # print(result.head())
    writer = pd.ExcelWriter('ret_src2.xlsx', engine='xlsxwriter')
    result.to_excel(writer, 'Sheet1')
    writer.save()


def diff_small():
    df_ret = pd.read_excel('ret.xlsx')
    df_src = pd.read_excel('src.xlsx')

    df_ret.sort_values(by='id_card_number')
    df_ret_cols = list(df_ret.columns.values)
    id_nums = df_ret['id_card_number']

    df_src_valid = df_src[df_src['id_card_number'].isin(id_nums)]
    df_src_valid.sort_values(by='id_card_number')

    exp = 0.00001
    discard_cols = [
        'id_card_number', 'score', 'gender', 'id_number_province',
    ]
    float_cols = [
        'pdl_credit_24'
    ]

    cols_dict = {
        'tongdun': ['tongdun_status', 'tongdun_25', 'tongdun_4', 'tongdun_14', 'tongdun_41',
                    'tongdun_259', 'tongdun_120', 'tongdun_152', 'tongdun_87', 'tongdun_136'],
        'call_record': ['call_record_600', 'call_record_441'],
        'hj': ['hj_3y_xfnl_5', 'hj_3y_xfnl_score'],
        'contact': ['contact_10', 'contact_11'],
        'ei': ['education'],
        'pdl': ['pdl_credit_24'],
    }
    col_data_dict = {col: [] for cols in cols_dict.values() for col in cols}

    for col in df_ret_cols:
        if col in discard_cols:
            continue

        ret_vals = list(df_ret[col])
        src_vals = list(df_src_valid[col])

        for i, id_num in enumerate(id_nums):
            is_ret_vals_na = isna(ret_vals[i])
            is_src_vals_na = isna(src_vals[i])
            if is_ret_vals_na and is_src_vals_na:
                continue

            if is_ret_vals_na or is_src_vals_na:
                col_data_dict.get(col).append(id_num)
            else:
                if col in float_cols:
                    if abs(ret_vals[i] - src_vals[i]) > exp:
                        col_data_dict.get(col).append(id_num)
                else:
                    if ret_vals[i] != src_vals[i]:
                        col_data_dict.get(col).append(id_num)

    for key, cols in cols_dict.items():
        diff_set = set()
        for col in cols:
            diff_set |= set(col_data_dict[col])
        print('ids of %s is %s' % (key, sorted(list(diff_set))))
        print('count of %s is %s' % (key, len(diff_set)))


def diff():
    df_ret = pd.read_excel('ret.xlsx')
    df_src = pd.read_excel('src.xlsx')

    df_ret.sort_values(by='id_card_number')
    df_ret_cols = list(df_ret.columns.values)
    id_nums = df_ret['id_card_number']

    df_src_valid = df_src[df_src['id_card_number'].isin(id_nums)]
    df_src_valid.sort_values(by='id_card_number')

    exp = 0.0000001
    discard_cols = [
        'id_card_number', 'activation_time', 'cashloan_ab_risk_score', 'cashloan_ab_risk_prob',
        'application_time', 'gender',
    ]
    float_cols = [
        'yys_report_404', 'call_record_452', 'n_c_yys_report_1074', 'n_c_phone_number_province',
        'n_c_call_record_2', 'n_c_tongdun_7', 'n_c_hj_1y_xfnl_5', 'n_c_jd_market_persona_3',
        'n_c_tongdun_121', 'n_c_contact_10', 'n_c_tongdun_18',
    ]

    cols_dict = {
        'yys_report': ['yys_report_404', 'yys_report_793', 'yys_report_1074'],
        'tongdun': ['tongdun_7', 'tongdun_18', 'tongdun_58', 'tongdun_85', 'tongdun_121',
                    'tongdun_125', 'tongdun_152'],
        'phone_number_province': ['phone_number_province'],
        'source_type': ['source_type'],
        'call_record': ['call_record_2', 'call_record_452'],
        'jd': ['jd_market_persona_3', 'jd_shop_persona_9'],
        'hj': ['hj_1y_xfnl_5'],
        'contact': ['contact_10'],
        'ei': ['qq_length', 'monthly_income'],
    }
    col_data_dict = {col: [] for cols in cols_dict.values() for col in cols}
    jd_ids_set = set()
    for col in df_ret_cols:
        if col in discard_cols:
            continue

        ret_vals = list(df_ret[col])
        src_vals = list(df_src_valid[col])

        for i, id_num in enumerate(id_nums):
            is_ret_vals_na = isna(ret_vals[i])
            is_src_vals_na = isna(src_vals[i])
            if is_ret_vals_na and is_src_vals_na:
                continue

            if is_ret_vals_na or is_src_vals_na:
                col_data_dict.get(col).append(id_num)
            else:
                if col in float_cols:
                    if abs(ret_vals[i] - src_vals[i]) > exp:
                        col_data_dict.get(col).append(id_num)
                else:
                    if ret_vals[i] != src_vals[i]:
                        if col in cols_dict.get('jd'):
                            # print('id_num=%s' % id_num)
                            jd_ids_set.add(id_num)
                            # print('ret=%s' % ret_vals[i])
                            # print('src=%s' % src_vals[i])
                        col_data_dict.get(col).append(id_num)

    # print('len of jd_ids_set = %s' % len(jd_ids_set))

    for key, cols in cols_dict.items():
        diff_set = set()
        for col in cols:
            diff_set |= set(col_data_dict[col])
        # print('ids of %s is %s' % (key, sorted(list(diff_set))))
        print('count of %s is %s' % (key, len(diff_set)))


def get_id_nums():
    f_name = 'ret.xlsx'
    df = pd.read_excel(f_name)
    id_nums = df['id_card_number']
    print(id_nums.head())
    s = df['id_card_number'].rolling(5).mean()
    print(s)


def dbutils_test():

    V2_CONFIG = {
        'host': '12.34.12.34',
        'port': 3306,
        'user': 'root',
        'password': '12341234',
        'db': 'v2',
        'charset': 'utf8',
    }

    pool = PooledDB(pymysql, 50, **V2_CONFIG)
    conn = pool.connection()
    cur = conn.cursor()

    sql = "select * from User where id=1"
    cur.execute(sql)
    r = cur.fetchall()
    print(r)
    cur.close()
    conn.close()
    pool.close()


def try_test():
    try:
        ret = 1 / 0
    except ZeroDivisionError as e:
        print(e)
        return None
    else:
        print('Correct')
    finally:
        print('End')

    return ret


if __name__ == '__main__':
    # diff()
    # concat()
    # get_id_nums()
    # dbutils_test()
    # print(try_test())

    concat('score')
    diff_small()
