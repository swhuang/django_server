# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
from celery import task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
import datetime





@task
def test_celery(x, y):
    from crm.server_utils.base.DQS import SingletonFactory
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    data = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    print data
    SingletonFactory.getCycleQueue().putitem(data)
    print "id:"+str(id(SingletonFactory.getCycleQueue()))
    logger.info('func end -------------------->')


    return x + y


@task
def test_multiply(x, y):
    from crm.server_utils.base.DQS import SingletonFactory
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    data = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    print data
    SingletonFactory.getCycleQueue().putitem(data)
    print "multiply id:" + str(id(SingletonFactory.getCycleQueue()))
    logger.info('func end -------------------->')
    return x * y

@task
def test_do_order(x, y):
    from crm.server_utils.base.DQS import SingletonFactory
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    data = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    print "*****"+str(data)
    SingletonFactory.getCycleQueue().move_pt()
    print "multiply id:" + str(id(SingletonFactory.getCycleQueue()))
    logger.info('func end -------------------->')
    return x * y

@task
def ExpireOrderProc(data):
    from crm.models import RentalOrder
    from crm.server_utils.base import FSM as fsm

    for ele in data:
        assert isinstance(ele, str)
        try:
            mOrder = RentalOrder.objects.get(orderid=ele)
            if mOrder.status == fsm.ORDER_START:
                mOrder.status = fsm.ORDER_CANCELED
                mOrder.save()
        except RentalOrder.DoesNotExist:
            pass

    p = RentalOrder.objects.all()

    print data

#批量导入解析商品文件
@task
def ImportingCSV(file):
    from crm.models import ProductDetail
    import csv
    csv_reader = csv.reader(open('file', encoding='utf-8'))
    for row in csv_reader:
        print(row)