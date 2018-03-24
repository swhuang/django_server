# -*- coding: utf-8 -*-
from django.test import TestCase
import urllib
import time
import httplib
import datetime
import hashlib
import sys
import json


# Create your tests here.
if __name__ == '__main__':
    _time = datetime.datetime.now()

    checksrc = 'merchantid=' + '100000000000001' + '&' + 'timestamp=' + _time.strftime("%Y%m%d%H%S%M") + '&' + 'key=' + \
               '2Dr80hiqkornQWPk'
    m = hashlib.md5()
    m.update(checksrc)
    _checksum = m.hexdigest()

    params = {'numbers': 'BE303507571DE'}
    params = urllib.urlencode(params)
    #params = json.dumps(params)


    conn = httplib.HTTPSConnection("api.trackingmore.com", timeout=300)
    print params
    print sys.getsizeof(params)
    headers = {"Content-type": "application/json", "Accept": "text/plain",
               "Trackingmore-Api-Key": "d90e3f32-0895-475b-b169-1055eab612ce"}
    conn.request("GET", "/v2/trackings/get", params, headers=headers)
    ri = conn.getresponse()
    print ri.status, ri.reason
    data = ri.read()
    #print data

    output = open('data.html', 'w')
    output.write(data)
    output.close()
