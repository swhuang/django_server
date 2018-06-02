# -*- coding: utf-8 -*-

SERVICE_RENTAL = 0
SERVICE_COMBOL = 1
SERVICE_SELL = 2


class serviceinfo(object):
    def __init__(self, **kwargs):
        servtype = kwargs.pop('tp', 0)
        servno = kwargs.pop('no', None)
        if kwargs:
            raise ValueError("argument error")
        if servtype not in [0,1,2]:
            raise ValueError("servtype error expect 0,1,2 but get %s" % servtype)
        self.serviceNo = servno
        self.type = servtype

    def dict(self):
        return {'no': self.serviceNo, 'tp': self.type}