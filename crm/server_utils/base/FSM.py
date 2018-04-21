# -*- coding: utf-8 -*-
# 服务状态机
class State(object):
    def __init__(self):
        pass

START_STATE = 0
RENTALPROC_STATE = 1
SELLPROC_STATE = 2
COMPLETE = 3

# 创建等待付款
class Start(State):
    def updatestate(self, w):
        if w.Orderid != []:
            w.set_state(RentalConfirmed())
        pass

    def getstatevalue(self):
        return START_STATE

# 确认服务(生成订单)
class RentalConfirmed(State):
    def updatestate(self, w):
        pass


# 完成支付
class RentalPayed(State):
    def updatestate(self, w):
        pass


# 租赁服务进行中
class RentalProcessing(State):
    def updatestate(self, w):
        pass

# 租赁服务逾期进行中
class ExpiredProcessing(State):
    def updatestate(self, w):
        pass

# 服务完成
class Completed(State):
    pass


class Closed(State):
    pass


# 售卖服务进行中
class SellingProcessing(State):
    pass