#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from werkzeug.utils import find_modules, import_string


def register_blueprints(instance):
    for name in find_modules('app.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'scorecard_bp'):
            instance.register_blueprint(mod.scorecard_bp)
