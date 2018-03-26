from __future__ import unicode_literals

from django.db import models
from django.core.cache import cache
from worker import Worker
import redis

# Create your models here.
'''
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.set('gender', 'male')
print(r.get('gender'))

cache.set("foo", "value", timeout=25)
print cache.get("foo")

worker = Worker()
worker.start()
r = worker.submit(pow, 3,3)
print(r.result())
'''