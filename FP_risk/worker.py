# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread, Event
from base.utils import Singleton
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from abc import abstractmethod

THREADCNT = 10

class ProcessPool:
    __metaclass__ = Singleton

    @property
    def pool(self):
        return self._pool

    def __init__(self):
        self._pool = multiprocessing.Pool(multiprocessing.cpu_count())
        print "init process pool with %s cpu(s)" % multiprocessing.cpu_count()

    def __call__(self, *args, **kwargs):
        print "init process pool with %s cpu(s)" % multiprocessing.cpu_count()
        return self._pool


class ThreadPool(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._pool = ThreadPoolExecutor(THREADCNT)

    def addwork(self, work):
        for i in xrange(THREADCNT):
            self._pool.submit(work)


class ActorExit(Exception):
    pass


class Actor(object):
    def __init__(self):
        self._mailbox = Queue()

    def send(self, msg):
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def start(self):
        self._terminated = Event()
        Pool = ThreadPool()
        Pool.addwork(work=self._bootstrap)
        '''
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()
        '''

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    @abstractmethod
    def run(self):
        """
        Run method to be implemented
        :return:
        """
        raise NotImplementedError
        #while True:
            #msg = self.recv()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print exc_type
        print exc_val
        self.close()
        print "close worker group"


class Result(object):
    def __init__(self):
        self._evt = Event()
        self._result = None

    def set_result(self, value):
        self._result = value
        self._evt.set()

    def result(self):
        self._evt.wait()
        return self._result

class Worker(Actor):
    __metaclass__ = Singleton

    def submit(self, func, *args, **kwargs):
        r = Result()
        self.send((func, args, kwargs, r))
        return r

    def run(self):
        while True:
            func, args, kwargs, r = self.recv()
            r.set_result(func(*args, **kwargs))
