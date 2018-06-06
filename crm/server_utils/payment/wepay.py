# -*- coding: utf-8 -*-
from weixin import Weixin, WeixinError
import logging
from pikachu import settings
from crm.models import PaymentOrder, ProductRental, ComboRental, SellService
from django.db import transaction
from crm.server_utils.customerField import structure
from crm.server_utils.base import FSM as fsm
from siteuser.member.models import SiteUser
from Accounting.models import BalanceManager

config = dict(WEXIN_APP_ID='wx1c88e225b036f07a', WEIXIN_APP_SECRET='6fd6d2e8e7b3df81361d7bfb5521a9de',
              WEIXIN_NOTIFY_URL=settings.NOTIFY_URL)
weixin = Weixin(config)

logger = logging.getLogger('transaction')


def pay_jsapi(amount, out_trade_no, fail=False):
    if settings.TESTMODE:
        try:
            payinst = PaymentOrder.objects.get(pay_id=out_trade_no)
        except PaymentOrder.DoesNotExist:
            logger.error(u"支付结果通知未找到支付订单号:%s" % out_trade_no)
            return False
        if fail:
            payfail(payinst=payinst)
            return False
        else:
            paysuccess(payinst=payinst)
            return True
    try:
        # out_trade_no = weixin.nonce_str
        raw = weixin.jsapi(openid="openid", body=u"测试", out_trade_no=out_trade_no, total_fee=amount)
        return raw
    except WeixinError, e:
        logger = logging.getLogger('django')
        logger.error(e.message)
        return False


def paysuccess(payinst):
    assert type(payinst) == PaymentOrder
    acct = SiteUser.objects.get(memberId=payinst.memberId).account
    with transaction.atomic():
        payinst.status = 1
        payinst.save()
        for order in payinst.order.all():
            if order.payedamount < order.amount:
                if not BalanceManager(acct=acct).defreeze(orderno=order.orderNo, isbill=True):
                    #发起退款
                    weixin.refund(out_trade_no=payinst.pay_id, out_refund_no=weixin.nonce_str, total_fee=payinst.payedamount, refund_fee=payinst.payedamount)
                    order.orderStatus =fsm.ORDER_START
                    if order.payment_status != 1:  # 支付中
                        logger.error(u"订单支付状态不正确 订单号: [%s] 状态码: [%s]" % (order.orderNo, order.payment_status))
                    order.payment_status = 0
                    order.save()
                    continue

            if order.orderStatus == fsm.ORDER_START or order.orderStatus == fsm.ORDER_CANCELED:  # 待支付
                order.orderStatus = fsm.ORDER_FINISHED  # 已支付

                if order.payment_status != 1:  # 支付中
                    logger.error(u"订单支付状态不正确 订单号: [%s] 状态码: [%s]" % (order.orderNo, order.payment_status))
                order.payment_status = 2
                order.save()

            else:
                logger.error(u"订单状态不正确 订单号: [%s] 状态码: [%s]" % (order.orderNo, order.orderStatus))
                continue
            if order.serviceType == structure.SERVICE_RENTAL:
                SERVICE_CLASS = ProductRental
            elif order.serviceType == structure.SERVICE_COMBOL:
                SERVICE_CLASS = ComboRental
            elif order.serviceType == structure.SERVICE_SELL:
                SERVICE_CLASS = SellService
            servinst = SERVICE_CLASS.objects.get(serviceNo=order.serviceNo)
            servinst.updatestate(fsm.PaymentEvent(ptype=order.type))
            servinst.save()

def payfail(payinst):
    assert type(payinst) == PaymentOrder
    payinst.status = 2  # 支付失败
    acct = SiteUser.objects.get(memberId=payinst.memberId).account
    with transaction.atomic():
        payinst.save()
        for order in payinst.order.all():
            if order.orderStatus == fsm.ORDER_START:  # 待支付
                if order.payedamount < order.amount:
                    BalanceManager(acct=acct).defreeze(orderno=order.orderNo, isbill=True)
                if order.payment_status != 1:  # 支付中
                    logger.error(u"订单支付状态不正确 订单号: [%s] 状态码: [%s]" % (order.orderNo, order.payment_status))
                order.payment_status = 0  # 未支付
                order.save()
            else:
                logger.error(u"订单状态不正确 订单号: [%s] 状态码: [%s]" % (order.orderNo, order.orderStatus))
                continue


def pay_notify(request):
    """
        微信异步通知
        """
    data = weixin.to_dict(request.data)
    if not weixin.check(data):
        return weixin.reply("签名验证失败", False)
    # 处理业务逻辑
    payid = data['out_trade_no']
    try:
        payinst = PaymentOrder.objects.get(pay_id=payid)
    except PaymentOrder.DoesNotExist:
        logger.error(u"支付结果通知未找到支付订单号:%s" % payid)
        return weixin.reply("参数格式校验错误", False)
        # TODO
    if payinst.status == 0:  # 支付中
        if data['result_code'] == 'SUCCESS':
            if data['total_fee'] != payinst.payedamount:
                logger.error(u"金额错误不等于原始金额")
                logger.info(data)
            else:
                paysuccess(payinst)

            return weixin.reply("OK", True)
        else:
            # 支付失败
            payfail(payinst=payinst)
            return weixin.reply("OK", True)
    else:
        return weixin.reply("交易不存在", False)
