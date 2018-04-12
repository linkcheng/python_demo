#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import timedelta
from flask import Flask
from settings import app_config
from app.models import init_models
from app.blueprints import register_blueprints


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.permanent_session_lifetime = timedelta(minutes=5)
    init_models()
    register_blueprints(app)
    return app
