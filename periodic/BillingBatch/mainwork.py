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
    from Accounting.models import Account, Baseacct, AccountClassifaction
    from siteuser.member.models import SiteUser
    from django.db import transaction
    logger = logging.getLogger('batch')
    logger.info("batch for:" + mcht + " merchantid:" + str(datetime.datetime.date()) + ':start')
    AllProductRental = list(ProductRental.objects.filter(isCompleted=False))

    for prl in AllProductRental:
        try:
            pd = ProductDetail.objects.get(productid=prl.product)
        except Exception, e:
            logger.error(e)
            continue

        try:
            member = SiteUser.objects.get(memberId=prl.memberId)
            acct = Account.objects.get(user=member)
        except Exception, e:
            logger.error(e)
            continue

        dailyAmt = pd.rent
        if pd.rent > (prl.residualRent + prl.residualDeposit):
            dailyAmt = prl.residualRent + prl.residualDeposit
        if dailyAmt > 0:
            # TODO
            with transaction.Atomic:
                DailyBilling = Baseacct(debit_credit=True, acid='DAILYBILL001', projid=prl.serviceNo, merchantid=mcht,
                                    balance=acct.balance, billingamt=dailyAmt, seq=acct.acctid)
                DailyBilling.save(force_insert=True)
                acct.balance -= dailyAmt
                acct.save()

            pass

        pass
