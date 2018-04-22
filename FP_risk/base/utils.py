# -*- coding: utf-8 -*-
import threading


def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return synced_func


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class InpInterface(object):
    pass
