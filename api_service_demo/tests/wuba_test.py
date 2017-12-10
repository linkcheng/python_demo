#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests


def score_test():
    url = 'http://127.0.0.1:8000/api/score'
    params = {
        'aaa114': '58_APP',
        'aaa14': 0,
        'aaa20': 1,
        'aaa40': 7,
        'aaa57': 5,
        'aaa77': 1000,
        'aaa78': 50,
        'aaa79': 50,
        'aaa8': 10,
        'aaa80': 50,
        'aaa81': 50,
        'applist_score': 1,
        'car_profile_1': 0,
        'house_profile_1': 0,
        'jl_education': '本科',
        'jl_nowsalary': '1000以下',
        'jl_salary': '1000-2000',
        'mamababy_profile_1': 0,
        'wantcar_profile_0': 0,
        'wantcar_profile_1': 0,
        'wanthouse_profile_0': 1,
        'wanthouse_profile_1': 1,
        'wantloan_profile_0': 1,
        'wantloan_profile_1': 0
    }
    cnt = requests.post(url=url, json=params)
    print(cnt.text)


if __name__ == '__main__':
    score_test()

