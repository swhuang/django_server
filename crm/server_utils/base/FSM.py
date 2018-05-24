# -*- coding: utf-8 -*-
import logging

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
    pass


class PaymentCancelEvent(Event):
    desc = '支付超时/取消'
    pass


class DeliveryCompleteEvent(Event):
    desc = '物流完成(取货、发货)'
    pass


class GenOrderEvent(Event):
    desc = '生成订单'

    def __init__(self, orderid):
        self._orderid = orderid

    @property
    def orderId(self):
        return self._orderid

    pass


class SaleOrderEvent(GenOrderEvent):
    desc = '生成转售订单'
    pass


class CompensationEvent(GenOrderEvent):
    desc = '生成赔偿订单'
    pass


class AutoCompleteEvent(Event):
    desc = '自动服务完成'
    pass


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
            error = '错误的事件:' + str(event)
            Logger.error(error)
            raise ValueError(error)
        error = '错误的事件:' + event.desc
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
        if isinstance(event, DeliveryCompleteEvent):
            w.set_state(RentalProcessing())
        else:
            self.post_err(event)


# 租赁服务进行中
class RentalProcessing(State):
    def updatestate(self, w, event):
        if isinstance(event, AutoCompleteEvent):
            w.set_state(RentalForSaleDone())
        elif isinstance(event, ConvertCompleteEvent):
            w.set_state(RentalForSaleDone())
        elif isinstance(event, SaleOrderEvent):
            w.set_state(ConvertToPay())
        elif isinstance(event, CompensationEvent):
            w.set_state(RentalToPay())
        elif isinstance(event, OverLimitEvent):
            w.set_state(Completed())
        elif isinstance(event, ManualCompleteEvent):
            w.set_state(Completed())
        else:
            self.post_err(event)
        pass


# 转售待支付
class ConvertToPay(State):
    def updatestate(self, w, event):
        if isinstance(event, PaymentCancelEvent):
            w.set_state(RentalProcessing())
        elif isinstance(event, PaymentEvent):
            w.set_state(RentalForSaleDone())
        else:
            self.post_err(event)
        pass
    pass


# 租赁待支付
class RentalToPay(State):
    def updatestate(self, w, event):
        if isinstance(event, PaymentEvent):
            w.set_state(Completed())
        elif isinstance(event, PaymentCancelEvent):
            w.set_state(RentalProcessing())
        else:
            self.post_err(event)
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
ORDER_CANCELED = 2


class OrderState(object):
    def __init__(self):
        pass


# 售卖服务进行中
class SellingProcessing(State):
    pass
