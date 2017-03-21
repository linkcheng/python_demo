# -*- coding: utf-8 -*-
import top.api

appkey = "appkey"
secret = "secret"
req = top.api.AlibabaAliqinFcSmsNumSendRequest()
req.set_app_info(top.appinfo(appkey, secret))

req.sms_type = "normal"
req.rec_num = "****"
req.sms_template_code = "****"
req.sms_free_sign_name = "风轻扬"
req.sms_param = {"name": "Link", "number": "123456"}
resp = req.getResponse()
print(resp)
