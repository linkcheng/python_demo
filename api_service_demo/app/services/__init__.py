#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import platform
import logging
from app.services.pingfenka import xjd_xyf_app_def_v1

logger = logging.getLogger(__name__)

platform_system = platform.system()
if platform_system == 'Darwin':
    from app.services.darwin.cashloan_ab_m1 import cashloan_ab_m1
    from app.services.darwin.paydayloan_p import paydayloan_p
else:
    try:
        from app.services.cashloan_ab_m1_20180409 import cashloan_ab_m1
        from app.services.paydayloan_p_20180402 import paydayloan_p
    except ImportError as e:
        logger.error(e)
        logger.error('Import so files error !')
        raise ImportError(e)
