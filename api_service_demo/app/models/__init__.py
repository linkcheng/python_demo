#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
from peewee import InternalError
from register import db
from app.models.scorecard_large import ScorecardLargeModel
from app.models.scorecard_large_test import ScorecardLargeTestModel
from app.models.scorecard_small import ScorecardSmallModel
from app.models.scorecard_small_test import ScorecardSmallTestModel

logger = logging.getLogger('init_models')


def init_models():
    models = [
        ScorecardLargeModel,
        ScorecardLargeTestModel,
        ScorecardSmallModel,
        ScorecardSmallTestModel,
    ]
    try:
        db.create_tables(models, safe=True)
    except InternalError as e:
        logger.exception(e)
