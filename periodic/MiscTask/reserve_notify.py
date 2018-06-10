# -*- coding: utf-8 -*-
from siteuser.functional import send_html_mail as _send_mail
from crm.models import ProductRental
from crm.server_utils.base import FSM
import logging
import datetime


def reservedproductnotify():
    allProductRental = list(ProductRental.objects.filter(serviceStatus=FSM.statedict[2]()))
    dateinfo = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    logging.getLogger('task').info("Reservedproduct Notification task begins: "+ dateinfo)
    notify_list = list()
    for prl in allProductRental:
        notify_list.append(str(prl.reservedProduct.update({'productid': prl.reservedProductid})))
        pass
    _send_mail(to="superhsw@163.com", subject=u"预约商品信息"+ dateinfo, content=','.join(notify_list))
