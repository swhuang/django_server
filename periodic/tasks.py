# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
from celery import task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
import datetime
from .BillingBatch.tasks import DailyBatch

@task
def daily_batch(mcht=''):
    DailyBatch(mcht)


@task
def test_do_order(x, y):
    from crm.server_utils.base.DQS import SingletonFactory
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    data = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    print "*****" + str(data)
    SingletonFactory.getCycleQueue().move_pt()
    print "multiply id:" + str(id(SingletonFactory.getCycleQueue()))
    logger.info('func end -------------------->')
    return x * y


# 过期订单处理
@task
def ExpireOrderProc(data):
    from crm.models import RentalOrder, ProductRental, ComboRental, SellService
    from crm.server_utils.base import FSM as fsm
    import logging
    from Accounting.models import BalanceManager
    from siteuser.member.models import SiteUser

    logger = logging.getLogger('task')
    for ele in data:
        assert isinstance(ele, str)
        try:
            mOrder = RentalOrder.objects.get(orderNo=ele)
            if mOrder.orderStatus == fsm.ORDER_START:
                if mOrder.payedamount < mOrder.amount:
                    acct = SiteUser.objects.get(memberId=mOrder.memberId).account
                    BalanceManager(acctid=acct.id, memberId=mOrder.memberId).defreeze(orderno=mOrder.orderNo)
                mOrder.orderStatus = fsm.ORDER_CANCELED
                mOrder.save()
                if mOrder.serviceType == 0:
                    SERVICE_CLASS = ProductRental
                elif mOrder.serviceType == 1:
                    SERVICE_CLASS = ComboRental
                elif mOrder.serviceType == 2:
                    SERVICE_CLASS = ComboRental
                else:
                    logger.error("ServiceType error %s" % str(mOrder.serviceType))
                    break
                mService = SERVICE_CLASS.objects.get(serviceNo=mOrder.serviceNo)
                mService.updatestate(fsm.PaymentCancelEvent())
        except RentalOrder.DoesNotExist:
            pass


@task
def ExpiredService(data):
    import logging
    from crm.server_utils.customerField import structure
    from crm.models import RentalOrder, ProductRental, ComboRental, SellService
    from crm.server_utils.base import FSM as fsm

    logging.getLogger('task').info(msg="serviceno: " + str(data))

    for ele in data:
        assert isinstance(ele, tuple)
        if ele[1] == structure.SERVICE_RENTAL:
            SERVICE_CLASS = ProductRental
        elif ele[1] == structure.SERVICE_COMBOL:
            SERVICE_CLASS = ComboRental
        elif ele[1] == structure.SERVICE_SELL:
            SERVICE_CLASS = SellService

        try:
            mService = SERVICE_CLASS.objects.get(serviceNo=ele[0])
        except SERVICE_CLASS.DoesNotExist:
            logging.getLogger('task').warn("error service no %s" % ele[0])
            continue
        mService.updatestate(fsm.TimeoutEvent())


@task
def ExpiredPayment(data):
    import logging
    from crm.server_utils.customerField import structure
    from crm.models import RentalOrder, ProductRental, ComboRental, SellService, PaymentOrder
    from crm.server_utils.base import FSM as fsm
    from django.db.transaction import atomic
    from crm.server_utils.payment import wepay
    logger = logging.getLogger('task')

    def revertpayment(payinst):
        refundinst = wepay.weixin.refund(out_trade_no=payinst.pay_id, out_refund_no=wepay.weixin.nonce_str,
                                         total_fee=payinst.payedamount, refund_fee=payinst.payedamount, )
        with atomic:
            payinst.status = 2  # 支付失败
            payinst.save()
            logger.info(refundinst)
            for order in payinst.order.all():
                if order.payment_status == 1: # 待支付
                    order.payment_status = 0 # 未支付
                order.save()

    for ele in data:
        assert isinstance(ele, str)
        try:
            payinst = PaymentOrder.objects.get(pay_id=ele)
        except PaymentOrder.DoesNotExist:
            logger.error(u'支付订单不存在')
            continue
        else:
            if payinst.status == 0:  # 支付中
                # 查询订单
                try:
                    querydict = wepay.weixin.order_query(out_trade_no=payinst.pay_id)
                except Exception, e:
                    logger.error(e)
                    revertpayment(payinst=payinst)
                else:
                    if querydict.get('trade_state') == 'SUCCESS':
                        wepay.paysuccess(payinst)
                    else:
                        wepay.payfail(payinst)


@task
def PostReservedInfo():
    pass