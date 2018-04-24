# -*- coding: utf-8 -*-
# 服务状态机
class State(object):
    def __init__(self):
        pass

START_STATE = 0
RENTAL_CONFIRM = 1
READYFORGOOD_STATE = 2
RENTALPROC_STATE = 3
SELLPROC_STATE = 4
COMPLETE = 5

# 创建等待付款
class Start(State):
    statevalue = START_STATE
    def updatestate(self, w):
        #若生成订单,则可进入下 确认服务 状态
        if w.RentalOrderid != [] or w.RentalOrderid !=[]:
            w.set_state(RentalConfirmed())
        pass


# 确认服务(已生成订单) = 待支付
class RentalConfirmed(State):
    statevalue = RENTAL_CONFIRM
    def updatestate(self, w):
        #if
        pass


# 完成支付 = 待取货
class ReadyForGood(State):
    def updatestate(self, w):
        pass


# 租赁服务进行中
class RentalProcessing(State):
    def updatestate(self, w):
        pass


# 退款进行中
class RefundProcessing(State):
    def updatestate(self, w):
        pass



# 租赁服务逾期进行中
class ExpiredProcessing(State):
    def updatestate(self, w):
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
