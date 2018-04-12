# -*- coding: utf-8 -*-
# 服务状态机
class State(object):
    def __init__(self):
        pass


# 创建等待付款
class Start(State):
    pass


# 租赁服务进行中
class RentalProcessing(State):
    pass


# 售卖服务进行中
class SellingProcessing(State):
    pass


# 服务完成
class Completed(State):
    pass
