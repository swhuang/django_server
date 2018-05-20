# -*- coding: utf-8 -*-
from weixin import Weixin, WeixinError
import logging

config = dict(WEXIN_APP_ID='wx1c88e225b036f07a', WEIXIN_APP_SECRET='6fd6d2e8e7b3df81361d7bfb5521a9de')
weixin = Weixin(config)

def pay_jsapi(amount):

    try:
        out_trade_no = weixin.nonce_str
        raw = weixin.jsapi(openid = "openid", body=u"测试", out_trade_no = out_trade_no, total_fee=amount)
        return raw
    except WeixinError, e:
        logger = logging.getLogger('django')
        logger.error(e.message)
        return False


def pay_notify(request):
    """
        微信异步通知
        """
    data = weixin.to_dict(request.data)
    if not weixin.check(data):
        return weixin.reply("签名验证失败", False)
    # 处理业务逻辑
    return weixin.reply("OK", True)