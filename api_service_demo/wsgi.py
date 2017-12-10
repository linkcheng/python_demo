# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from instance import app, run
# 导入 app 是必须的，在 gunicorn 中启动需要

if __name__ == '__main__':
    run()
