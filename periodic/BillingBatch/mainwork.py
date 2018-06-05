# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
from celery import task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
import datetime


@task
def DailyBatch(mcht=''):
    from crm.models import ProductRental
    from crm.models import ComboRental
    from crm.models import ProductDetail
    from Accounting.models import *
    from siteuser.member.models import SiteUser
    from django.db import transaction
    from crm.server_utils.base import FSM
    logger = logging.getLogger('batch')
    logger.info("batch for:" + mcht + " merchantid:" + str(datetime.datetime.date()) + ':start')
    AllProductRental = list(ProductRental.objects.filter(serviceStatus=FSM.statedict[3]))  # rental processing
    # TODO
    for prl in AllProductRental:
        try:
            pd = ProductDetail.objects.get(productid=prl.product)
        except Exception, e:
            logger.error(e)
            continue

        try:
            member = SiteUser.objects.get(memberId=prl.memberId)
        except Exception, e:
            logger.error(e)
            continue

        if prl.daily_amount != 0.0:
            requiredamt = prl.daily_amount
        else:
            requiredamt = prl.initialRent / prl.rentPeriod

        if prl.payed_amount != 0.0:
            payedAmt = prl.payed_amount
        else:
            payedAmt = prl.initialRent + prl.initialDeposit - prl.residualDeposit - prl.residualRent
            prl.payed_amount = payedAmt

        if prl.product['sellingPrice'] - payedAmt < requiredamt:
            requiredamt = prl.product['sellingPrice'] - payedAmt


        dailyAmt = requiredamt
        if requiredamt > (prl.residualRent + prl.residualDeposit):
            dailyAmt = prl.residualRent + prl.residualDeposit
        with transaction.atomic:
            if dailyAmt > 0:  # 实际入账金额
                # TODO
                billobj = BillingTran(projid=prl.serviceNo, member=member, serviceType=0)

                # 服务单金额变化
                v = prl.residualRent - dailyAmt
                if v >= 0:
                    prl.residualRent -= dailyAmt
                    billobj.billingrent(dailyAmt)
                else:
                    prl.residualRent = 0.0
                    if v * (-1) <= prl.residualDeposit:
                        prl.residualDeposit -= v * (-1)
                        billobj.billingrent(prl.residualRent)
                        billobj.billingdeposit(v * (-1))
                    else:
                        logger.error(
                            "Invalid amount-- serviceNo:{%s}, dailyamt:{%s}, residualRent:{%s}, residualDeposit:{%s}" % (
                                prl.serviceNo, dailyAmt, prl.residualRent, prl.residualDeposit))
                        raise ValueError("服务单金额错误v{%s}" % (v))

                # 初始化租赁日期
                if not prl.rentStartDate:
                    prl.rentStartDate = datetime.date.today()
                if not prl.rentDueDate:
                    prl.rentDueDate = datetime.date.today() + datetime.timedelta(days=prl.rentPeriod)

            prl.updatestate(FSM.batchEvent(requireamount=requiredamt, billingamount=dailyAmt))
            prl.save()
