from django.test import TestCase
import urllib
import time
import datetime
import hashlib
import sys
import json


# Create your tests here.
if __name__ == '__main__':
    import httplib
    _time = datetime.datetime.now()


    checksrc = 'merchantid=' + '100000000000001' + '&' + 'timestamp=' + _time.strftime("%Y%m%d%H%S%M") + '&' + 'key=' + \
               '2Dr80hiqkornQWPk'
    m = hashlib.md5()
    m.update(checksrc)
    _checksum = m.hexdigest()

    params = {'merchantid': '100000000000001', 'timestamp': _time.strftime("%Y%m%d%H%S%M"),
                               'username': 'xyn2', 'password': '12345',
                               'checksum': _checksum}
    #params = urllib.urlencode(params)
    params = json.dumps(params)


    conn = httplib.HTTPConnection("127.0.0.1:8000", timeout=300)
    print params
    print sys.getsizeof(params)
    headers = {"Content-type": "application/json", "Accept": "text/plain", "Content-Length": len(params)}
    conn.request("POST", "/userform/getsessiontoken/", params, headers=headers)
    ri = conn.getresponse()
    print ri.status, ri.reason
    data = ri.read()
    #print data

    output = open('data.html', 'w')
    output.write(data)
    output.close()

    #print "get data: "+str(data['sessiontoken'])

    _token = 'MTUwNzgwMzc3Ni4yOTphOGQyOTlhZmYwY2FjNjA0MzYwZDE3ZmZhZmE4M2EwMTY5NzI0OGNh'
    params = urllib.urlencode({'merchantid': '100000000000001', 'sessiontoken': _token,
                               'username': 'xyn2'})

    params2 = {'merchantid': '100000000000001', 'sessiontoken': _token,
                               'username': 'xyn2'}
    params2 = json.dumps(params2)

    conn = httplib.HTTPConnection("127.0.0.1:8000", timeout=300)
    headers = {"Content-type": "application/json", "Accept": "text/plain", "Content-Length":sys.getsizeof(params2)}
    conn.request("POST", "/userform/getuserdata/", params2, headers=headers)
    ri = conn.getresponse()
    print ri.status, ri.reason
    data = ri.read()
    print data