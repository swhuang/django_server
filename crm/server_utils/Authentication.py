# -*- coding: utf-8 -*-
import random
import time
import urllib2,urllib

class MsgAuthentication(object):
    '''
    短信认证事物处理
    '''
    @staticmethod
    def createPhoneCode(session):
        '''

        :param session: request.session
        :return:
        '''
        chars=['0','1','2','3','4','5','6','7','8','9']
        x = random.choice(chars),random.choice(chars),random.choice(chars),random.choice(chars)
        verifyCode = "".join(x)
        session["phoneVerifyCode"] = {"time":int(time.time()), "code":verifyCode}
        return verifyCode

    @staticmethod
    def sendTelMsg(msg, phoneID):
        SendTelMsgUrl="http://www.810086.com.cn/jk.aspx"
        params = {"zh":"china", "mm":"china@10086",
            "hm":phoneID,"nr":msg,"sms_type":88}
        postData=urllib.urlencode(params)
        req = urllib2.Request(SendTelMsgUrl, postData)
        req.add_header('Content-Type', "application/x-www-form-urlencoded")
        respone = urllib2.urlopen(req)
        res = respone.read()
        return res

    @staticmethod
    def verifyPhoneCode(session, code):
        try:
            if session["phoneVerifyCode"]["time"] > int(time.time()) and \
                    session["phoneVerifyCode"]["code"] == code:
                return True
            else:
                return False
        except:
            return False