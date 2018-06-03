# -*- coding: utf-8 -*-
# 该模块用于构建环形队列,以便实现订单超时功能
from FP_risk.base.utils import synchronized
from django.utils import timezone
from FP_risk.worker import Worker
import threading
import datetime
import copy
from periodic.tasks import ExpireOrderProc, ExpiredService
import logging
from django.core.cache import cache

MAXMINUTE = 15  # 15 minutes


class Singleton(object):
    objs = {}

    objs_locker = threading.Lock()

    def __new__(cls, *args, **kwargs):

        if cls in cls.objs:
            return cls.objs[cls]

        cls.objs_locker.acquire()

        try:

            if cls in cls.objs:  ## double check locking

                return cls.objs[cls]

            cls.objs[cls] = object.__new__(cls, *args, **kwargs)
            cls.objs[cls].__Singleton_Init__(*args, **kwargs)

        finally:

            cls.objs_locker.release()
        return cls.objs[cls]

    def __Singleton_Init__(self):
        print("__Singleton_Init__")

    def __init__(self, *args, **kwargs):
        pass


class SingletonFactory(Singleton):
    @staticmethod
    def getCycleQueue():
        cQueue = CycleQueue(MAXMINUTE * 2)  # 每两秒钟走一格的情况下 30 = 15分钟
        return cQueue

    @staticmethod
    def getServiceQueue():
        return ServiceQueue(MAXMINUTE * 2)


#
def TreatOrder(orderlist):
    # 处理过期订单
    pass
    # print orderlist
    # print "time: " + str(timezone.now())


class CycleQueue(Singleton):
    def __Singleton_Init__(self, maxsize):
        print "init cyclequeue"
        self.current_point = 0
        self.maxcount = MAXMINUTE * 60 * 100  # 总交易数
        self.maxnode = maxsize  # MAXMINUTE*60
        self.__queue = [{'data': [], 'np': -1} for i in range(self.maxnode)]
        self.curitem = 0

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("CycleQueue should use int!")
        return self.queue[item]

    @synchronized
    def move_pt(self):
        dk = []
        p = []
        for i, ele in enumerate(self.__queue[self.current_point]['data']):
            try:
                if ele and ele['ctag'] == 1:
                    dk.append(i)
                    p.append(ele['v'])
                    # self.mWorker.submit(TreatOrder, p)  # 考虑用celery worker去做

                    self.curitem -= 1
                    self.__queue[self.current_point]['data'][i] = None
            except AttributeError, e:
                print "============debuging============"
                print self.__queue[self.current_point]['data']
                print i
                print ele
                print "==========debugingend==========="
                break
        try:
            if self.__class__.__name__ == 'CycleQueue':
                r = ExpireOrderProc.delay(p)
            elif self.__class__.__name__ == 'ServiceQueue':
                r = ExpiredService.delay(p)
        except Exception, e:
            logging.getLogger('django').error(e)
            print str(e)
        if len(dk) != 0:  # delete keywords
            self.__queue[self.current_point]['np'] = dk[0]
            self.LogInfo()
        else:
            self.__queue[self.current_point]['np'] = -1

        self.current_point += 1
        self.current_point %= self.maxnode
        for e in self.__queue[self.current_point]['data']:
            if e and e['ctag'] == 0:
                e['ctag'] = 1

    @synchronized
    def putitem(self, v):
        cur_pos = copy.copy(self.current_point)
        if self.curitem == self.maxcount:
            raise RuntimeError("CycleQueue full")
        data = dict()
        data['v'] = v
        data['ctag'] = 0
        store_pos = self.__queue[cur_pos]['np']
        if store_pos == -1:
            self.__queue[cur_pos]['data'].append(data)
        else:
            self.__queue[cur_pos]['data'][store_pos] = data
        self.curitem += 1

    def LogInfo(self):
        logging.getLogger('task').info(self.__class__.__name__ + "change info is: " + self.__queue)


class ServiceQueue(CycleQueue):
    @synchronized
    def putitem(self, v):
        if type(v) != tuple and len(v) != 2:
            raise ValueError(u"参数必须为tuple")
        return super(ServiceQueue, self).putitem(v)


class PaymentQueue(CycleQueue):
    pass


def Order_timer():
    SingletonFactory.getCycleQueue().move_pt()
    SingletonFactory.getServiceQueue().move_pt()
    global timer
    timer = threading.Timer(2.0, Order_timer)
    timer.start()


if __name__ == '__main__':
    print str(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))[-5:-1]
    a = CycleQueue(MAXMINUTE * 30)
    b = CycleQueue(MAXMINUTE * 30)
    print id(a)
    print id(b)
    SingletonFactory.getCycleQueue()
    print "id:" + str(id(SingletonFactory.getCycleQueue()))
    SingletonFactory.getCycleQueue()
    print "id:" + str(id(SingletonFactory.getCycleQueue()))
    # cache.set("foo", "value", timeout=25)
    # print cache.get("foo")
