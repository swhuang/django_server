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
    print "id:" + str(id(SingletonFactory.getCycleQueue()))
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
    print "*****" + str(data)
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
            mOrder = RentalOrder.objects.get(orderNo=ele)
            if mOrder.status == fsm.ORDER_START:
                mOrder.status = fsm.ORDER_CANCELED
                mOrder.save()
        except RentalOrder.DoesNotExist:
            pass

    p = RentalOrder.objects.all()

    print data


# 批量导入解析商品文件
@task
def ImportCSV(file):
    from crm.models import ProductDetail
    import csv
#    csv_reader = csv.reader(open(file, encoding='utf-8'))
    CATEGORY = {}
    CATEGORY['ALL'] = 0
    CATEGORY['项链'] = 1
    CATEGORY['戒指'] = 2
    CATEGORY['手镯'] = 3
    CATEGORY['耳饰'] = 4
    CATEGORY['手链'] = 5
    CATEGORY['脚饰'] = 6
    CATEGORY['胸针&领针'] = 7
    CATEGORY['摆件'] = 8

    with open(file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            for ii, xi in enumerate(row):
                row[ii] = xi.decode('gbk')
            if i == 0:
                print(row)
                continue
            IsPub = False
            if row[15] == '1':
                IsPub = True

            if not CATEGORY.has_key(str(row[2])):
                print "error!!"

            pd = ProductDetail(model=row[0], title=row[1], category=CATEGORY[str(row[2])], brand=row[3], series=row[4],
                               certificate=row[5], goldType=row[6], goldContent=row[7], diamondWeight=float(row[8]),
                               size=row[9], sellingPrice=float(row[10]), rent=float(row[11]), rentcycle=int(row[12]),
                               reletcycle=int(row[13]), deposit=float(row[14]), releaseStatus=IsPub, remark=row[16])
            pd.save()