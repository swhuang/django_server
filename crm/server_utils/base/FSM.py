# -*- coding: utf-8 -*-
import logging
import datetime

"""
服务状态机:
使用方法:
    产生相应事件处理完毕后调用:
        service.update_status(event)
    自动完成状态更新和转换,再日终批量处理时,批量处理的业务逻辑为:
        1. 交易入账
        2. 用户账户入账和金额变动
        3. 使用本模块更新服务单状态(包括信用状态)
"""

Logger = logging.getLogger('django')


# 事件
class Event(object):
    def __init__(self):
        pass


class TimeoutEvent(Event):
    desc = '服务单超时未生成订单'
    pass


class PaymentEvent(Event):
    desc = '支付成功'
    #ptype = None
    def __init__(self, ptype):
        self.ptype = ptype
    pass


class PaymentCancelEvent(Event):
    desc = '支付超时/取消'
    pass


class DeliveryCompleteEvent(Event):
    desc = '物流完成(取货、发货)'
    pass


class GenOrderEvent(Event):
    desc = '生成订单'

    def __init__(self, orderNo):
        self._orderid = orderNo

    @property
    def id(self):
        return self._orderid

    pass



class batchEvent(Event):
    desc = '账务变更'

    def __init__(self, requireamount, billingamount):
        r'''

        :param requireamount: 需要入账金额
        :param billingamount: 实际入账金额
        '''
        self.reqAmount = requireamount
        self.billAmount = billingamount

class ConvertCompleteEvent(Event):
    desc = '租转售'
    pass


class OverLimitEvent(Event):
    desc = '超限, 租金押金扣完且不到销售价'
    pass


class CompleteEvent(Event):
    desc = '租赁完成'
    pass


class ManualCompleteEvent(Event):
    desc = '手工完成'
    pass


# ======================================服务状态机=========================================
class State(object):
    class Meta:
        abstract = True

    def __init__(self):
        pass

    def updatestate(self, w, event):
        raise NotImplementedError

    def post_err(self, event):
        if not hasattr(event, 'desc'):
            error = u'错误的事件:' + str(event)
            Logger.error(error)
            raise ValueError(error)
        error = u'错误的事件:' + event.desc + u', 当前事件' + self.desc
        Logger.error(error)
        raise ValueError(error)

START_STATE = 0
RENTAL_CONFIRM = 1
READYFORGOOD_STATE = 2
RENTALPROC_STATE = 3
SELLPROC_STATE = 4
COMPLETE = 5


# 创建等待付款
class Start(State):
    statevalue = START_STATE

    def updatestate(self, w, event):
        # 若生成订单,则可进入下 确认服务 状态
        if isinstance(event, TimeoutEvent):
            w.set_state(Closed())
        elif type(event) == GenOrderEvent:
            w.set_state(RentalConfirmed())
        else:
            self.post_err(event)
        pass


# 确认服务(已生成订单) = 待支付
class RentalConfirmed(State):
    statevalue = RENTAL_CONFIRM

    def updatestate(self, w, event):
        if isinstance(event, PaymentCancelEvent):
            w.set_state(Closed())
        elif isinstance(event, PaymentEvent):
            w.set_state(ReadyForGood())
        else:
            self.post_err(event)


# 完成支付 = 待取货
class ReadyForGood(State):
    def updatestate(self, w, event):
        from crm.models import ProductRental
        if isinstance(event, DeliveryCompleteEvent):
            if isinstance(w, ProductRental):
                w.set_state(RentalProcessing())
            else:
                w.set_state(Completed())
        else:
            self.post_err(event)


# 租赁服务进行中
class RentalProcessing(State):
    def updatestate(self, w, event):
        from crm.models import ProductRental, ComboRental, SellService, Project
        from Accounting.models import BillingTran, BalanceManager
        from siteuser.member.models import SiteUser

        if isinstance(event, batchEvent):
            if isinstance(w , ProductRental):
                if w.residualDeposit < w.initialDeposit and w.creditStatus == '0':# 逾期
                    w.creditStatus = '1'
                T = min(w.product.get('sellingPrice', 0), w.initialRent+w.initialDeposit)
                payedamount = w.initialDeposit+w.initialRent - w.residualDeposit - w.residualRent
                if T != payedamount:
                    return

                if w.product.get('sellingPrice', 0) <= (w.initialRent+w.initialDeposit):
                    amt = w.initialRent + w.initialDeposit - w.product.get('sellingPrice', 0)
                    usr = SiteUser.objects.get(memberId=w.memberId)
                    # 余额充值
                    BalanceManager(acct=usr.account).recharge(amt)
                    w.set_state(RentalForSaleDone())
                else:
                    if event.reqAmount > event.billAmount and w.creditStatus != '2':
                        w.creditStatus = '2' #超限
                        w.set_state(Completed())
                    else:
                        return
            elif isinstance(w, ComboRental):
                if w.productid == '': #当前无在租品
                    if w.rentDueDate == datetime.date.today():
                        w.set_state(Completed())
                elif w.creditStatus == '1': # 逾期
                    if w.rentDueDate == datetime.date.today():
                        w.set_state(Completed())
                        # TODO 增加租赁服务


        elif isinstance(event, ConvertCompleteEvent):
            w.set_state(RentalForSaleDone())
        elif isinstance(event, GenOrderEvent):
            w.set_state(ReadyToPay())
        elif isinstance(event, ManualCompleteEvent):
            if isinstance(w, Project):
                usr = SiteUser.objects.get(memberId=w.memberId)
                servtype = 0
                if type(w) == ProductRental:
                    servtype = 0
                elif type(w) == ComboRental:
                    servtype = 1
                elif type(w) == SellService:
                    servtype = 2
                BillingTran(projid=w.serviceNo, member=usr, serviceType=servtype)
                if w.residualRent > 0:
                    BillingTran.billingrent(w.residualRent)
                if w.residualDeposit > 0:
                    BillingTran.billingdeposit(w.residualDeposit)
                w.set_state(Completed())
        else:
            self.post_err(event)
        pass


# 待支付
class ReadyToPay(State):
    def updatestate(self, w, event):

        if isinstance(event, PaymentCancelEvent):
            w.set_state(RentalProcessing())
        elif isinstance(event, PaymentEvent):
            # TODO
            if event.ptype == 5: # 补差订单
                w.set_state(RentalForSaleDone())
            elif event.ptype == 3: # 赔偿订单
                w.set_state(Completed())
        else:
            self.post_err(event)
        pass
    pass


# 租转售完成
class RentalForSaleDone(State):
    pass


# 退款进行中
class RefundProcessing(State):
    def updatestate(self, w):
        pass


# 租赁服务逾期进行中
class ExpiredProcessing(State):
    pass


# 服务完成
class Completed(State):
    pass


# 服务关闭
class Closed(State):
    pass


# 退款完成
class RefundDone(State):
    pass


# **************订单状态*****************

ORDER_START = 0
ORDER_FINISHED = 1
ORDER_REFUND = 2
ORDER_REFUNDED = 3
ORDER_CANCELED = 4

class OrderState(object):
    def __init__(self):
        pass


# 售卖服务进行中
class SellingProcessing(State):
    pass


#========================
statedict = {
    0: Start,
    1: RentalConfirmed,
    2: ReadyForGood,
    3: RentalProcessing,
    4: ReadyToPay,
    5: RentalForSaleDone,
    6: Completed,
    7: Closed
}
