#encoding=utf-8
import math
import operator
import time
from fractions import Fraction
from collections import defaultdict
from itertools import combinations, permutations
import copy
import random
import sys
sys.path.append("..")
import Util

def calctime(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        rt = fn(*args, **kwargs)
        end = time.time()
        print fn.__name__ + " cost time: "+str(end-start)
        return rt
    return wrapper

#全组合映射
class hsw_comb(object):
    def __init__(self, M, l = []):
        self.N = len(l)
        self.M = M
        self._list = l

    def X(self,lst):
        if len(lst) != self.M:
            return -1
        result = 0

        b = 0
        for i in range(self.M):
            b = b ^ (1 << (self.N-1-lst[i]))

        l = 1
        for k in range(self.N):
            m = (1 << k)&b
            if m != 0:
                result += hsw_comb.combine(k,l)
                l += 1
        print bin(b)
        return result

    def An(self,x):
        #print "======AN======"
        v = 0
        ret = x
        for i in range(self.M):
            rt = self.__b(ret,self.M-i)
            if rt != 0:
                ret -= rt[1]
                v = v ^ (1<<rt[0])
                #print bin(v)
        m = (bin(v).replace('0b',''))[::-1]
        ret = []
        for i in xrange(len(m)):
            if m[i] == '1':
                ret.append(self._list[i])

        return ret

    def __b(self,n,m):
        if m == 0:
            return 0
        t = 1
        i = m
        while n >= t:
            tmp = t
            t *= Fraction(i + 1,i - m + 1)
            if t > n:
                return (i,tmp)
            else:
                i += 1
        return (i-1,0)

    @staticmethod
    def combine(n,m):
        return reduce(operator.mul, range(n - m +1, n+1),1) / reduce(operator.mul, range(1, m + 1),1)
    @staticmethod
    def perm(n,m):
        return math.factorial(n) / math.factorial(n - m)

'''
从1开始
KTN（4）0,1,2,3   4个数字全排列
康托展开
'''
class KTN():
    def __init__(self,N):
        self.maxn = N
        self.fablist = []
        self.fablist.append(1)
        for i in range(N):
            self.fablist.append(math.factorial(i + 1))
        self.listdict = {}

    def X(self,list):
        lens = len(list)
        ans = 0
        for i in xrange(lens):
            x = 0
            for j in xrange(i+1,lens):
                if list[j] < list[i]:
                    x += 1
            #ans += x * math.factorial(lens-i-1)
            ans += x * self.fablist[lens-i-1]
        ans += 1

        return ans

    def An(self,X):
        if self.listdict.has_key(X):
            print "reduced!"
            return self.listdict[X]
        n = self.maxn
        showed = []
        ans = []
        for i in xrange(n+1):
            showed.append(False)
        for i in xrange(n):
            ans.append(0)
        tmp = X
        X -= 1
        for i in xrange(n):
            #numOfMin = X / math.factorial(n-1-i)
            numOfMin = X / self.fablist[n-1-i]
            #X = X % math.factorial(n - 1 - i)
            X = X % self.fablist[n - 1 - i]
            j = 0
            k = 0
            while j<=numOfMin:
                try:
                    if showed[k] == False:
                        j += 1
                except IndexError,e:
                    print e.message
                    print "kkk:"+str(n)
                    print "errornumber:"+str(tmp)
                    print "K value:"+str(k)
                    exit()
                k += 1
            k -= 1
            ans[i] = k;
            showed[ans[i]] = True
        '''
        for i in xrange(n):
            ans[i] += 1
        '''
        self.listdict[X] = ans
        return ans


class HSW_code(object):
    def __init__(self,keylist,weekday,lesson,classn, courseflg = False):
        self.count = weekday*lesson
        self.nlesson = lesson
        self.nweekday = weekday
        self.orig_code = []
        self.keylist = keylist
        self.mut_keylist = copy.deepcopy(keylist)
        self.classn = classn

        basecnt = len(self.mut_keylist)
        self.cdrange = hsw_comb.combine(basecnt, self.classn)
        self._headlen = len(bin(self.cdrange).replace('0b',''))
        self._taillen = len(bin(math.factorial(self.classn)).replace('0b',''))
        self.phaselen = self._headlen+self._taillen

        self.ktn = KTN(self.classn)

        #如果一个老师可以教多个不同课程，或者一个老师不同课程之间存在区分
        self._courselen = 0
        self.courseflg = courseflg #区分老师课程标志
        self.coursecodelen = 0 #老师课程全排列二进制长度
        self.coursel_dic = {} #每个老师的所有课程的全排列二进制长度
        if courseflg:
            maxlen = 0
            for v in self.mut_keylist:
                l = len(bin(math.factorial(len(self.mut_keylist[v]))).replace('0b',''))
                maxlen += + l
                self.coursel_dic[v] = l
            self.coursecodelen = maxlen

        self.morelen = 138#for test
        self.decode(123467)#探测一次多余的长度

        self.wholelen = self.phaselen*self.count - self.morelen
        self.mfclassn = math.factorial(self.classn)

        #print self.morelen


    def generatecode(self):
        _range = (1 << self.phaselen * self.count) -1
        return random.randint(0,_range)

    def generatecode2(self):
        _range = (1<<self.wholelen)
        return random.randint(0,_range)

    def code_length(self):
        return self.phaselen*self.count

    def code_length2(self):
        return self.wholelen

    def decode2(self,_n):
        totallen = self.wholelen
        entry_n = _n
        # ================================need further test=================
        course_pick_list = {}
        if self.courseflg:
            course_pick = _n #& (1 << self.coursecodelen - 1)
            entry_n = _n >> self.coursecodelen
            for v in self.mut_keylist:
                _ktn = KTN(len(self.mut_keylist[v]))
                m = course_pick #& ((1 << self.coursel_dic[v]) - 1)
                course_pick_list[v] = _ktn.An(m)
                course_pick = course_pick >> self.coursel_dic[v]
        # ==================================================================
        _mut_keylist = copy.deepcopy(self.mut_keylist)  # 每次解码都复制一份keylist
        randomslot = copy.copy(_mut_keylist.keys())
        theline = []
        theWeekline = []
        sicencelen = 0  #
        for i in xrange(self.count):
            if len(randomslot) != 0 and len(randomslot) < self.classn:
                # print "error"
                nnn = 0
                for ll in randomslot:
                    for value in _mut_keylist[ll]:
                        nnn += 1
                print nnn
                return None
            m = []
            m3 = []  # 排序好的老师选取列表
            v = Util.sort_by_value(_mut_keylist)
            judge = self.count - i  # (WEEKDAY - ii) * LESSON - jj
            m_i = 0
            randomslot = []
            for a in v:
                randomslot.append(a[1])
                if a[0] == judge:
                    m.append(m_i)
                m_i += 1

            if self.classn >= len(m):
                _comb = hsw_comb(self.classn - len(m), range(len(m), len(randomslot)))
                tmp_cmb = hsw_comb.combine(len(randomslot) - len(m), self.classn - len(m))
                sicencelen += self._headlen - len(bin(tmp_cmb).replace('0b', ''))
                '''
                new way here
                '''
                _headpick = entry_n >> (totallen - len(bin(tmp_cmb).replace('0b', '')))
                entry_n = entry_n &((1<<(totallen - len(bin(tmp_cmb).replace('0b', '')))) - 1)
                totallen -= len(bin(tmp_cmb).replace('0b', ''))
                combnumber = _headpick % tmp_cmb

                _tailpick = entry_n >> (totallen - self._taillen)
                entry_n = entry_n & ((1<<(totallen - self._taillen)) - 1)
                totallen -= self._taillen
                permnumber = _tailpick % self.mfclassn

                m += _comb.An(combnumber)
                m2 = self.ktn.An(permnumber + 1)

                for _i in m2:
                    m3.append(m[_i])

            else:
                print "This is error!"
                exit()

            onelinecourse = []
            for k in m3:
                try:
                    # tindex = random.randrange(0, len(_mut_keylist[randomslot[k]]) - 1)
                    if self.courseflg:
                        tindex = course_pick_list[randomslot[k]].pop()
                        for vi in range(len(course_pick_list[randomslot[k]])):
                            if course_pick_list[randomslot[k]][vi] > tindex:
                                course_pick_list[randomslot[k]][vi] -= 1
                    else:
                        tindex = 0
                except IndexError, e:
                    print e.message
                except ValueError, e:
                    tindex = 0
                except KeyError, e:
                    print e.message
                try:
                    onelinecourse.append(_mut_keylist[randomslot[k]][tindex])
                except IndexError, e:
                    pass
                del _mut_keylist[randomslot[k]][tindex]
                if len(_mut_keylist[randomslot[k]]) == 0:
                    del _mut_keylist[randomslot[k]]
            theline.append(onelinecourse)
            if i % self.nlesson == (self.nlesson - 1):
                theWeekline.append(copy.copy(theline))
                theline = []
        #print "多余的长度: " + str(sicencelen) + "总长度: " + str(self.phaselen * self.count)
        return theWeekline


    def setdecode3(self,kdict,classflg):
        self.keydict = kdict
        self.classflg = classflg
#分班走班排法
    def decode_3(self,_n):
        totallen = self.wholelen
        entry_n = _n
        #_mut_keylist = copy.deepcopy(self.mut_keylist)  # 每次解码都复制一份keylist
        _mut_keylist = copy.deepcopy(self.keydict)
        randomslot = copy.copy(_mut_keylist.keys())
        theline = []
        theWeekline = []
        sicencelen = 0  #
        for i in xrange(self.count):
            if len(randomslot) != 0 and len(randomslot) < self.classn:
                # print "error"
                nnn = 0
                for ll in randomslot:
                    for value in _mut_keylist[ll]:
                        nnn += 1
                print nnn
                return None
            m = []
            m3 = []  # 排序好的老师选取列表
            v = Util.sort_by_value(_mut_keylist) #长度，老师，值列表
            judge = self.count - i  # (WEEKDAY - ii) * LESSON - jj
            m_i = 0
            randomslot = []
            for a in v:
                randomslot.append(a[1])
                if a[0] == judge:
                    m.append(m_i)
                m_i += 1

            if self.classn >= len(m):
                _comb = hsw_comb(self.classn - len(m), range(len(m), len(randomslot)))
                tmp_cmb = hsw_comb.combine(len(randomslot) - len(m), self.classn - len(m))
                sicencelen += self._headlen - len(bin(tmp_cmb).replace('0b', ''))
                '''
                new way here
                '''
                _headpick = entry_n >> (totallen - len(bin(tmp_cmb).replace('0b', '')))
                entry_n = entry_n &((1<<(totallen - len(bin(tmp_cmb).replace('0b', '')))) - 1)
                totallen -= len(bin(tmp_cmb).replace('0b', ''))
                combnumber = _headpick % tmp_cmb

                _tailpick = entry_n >> (totallen - self._taillen)
                entry_n = entry_n & ((1<<(totallen - self._taillen)) - 1)
                totallen -= self._taillen
                permnumber = _tailpick % self.mfclassn

                m += _comb.An(combnumber)
                m2 = self.ktn.An(permnumber + 1)

                for _i in m2:
                    m3.append(m[_i])
            else:
                print "This is error!"
                exit()

            onelinecourse = []
            for k in m3:
                try:
                    tindex = 0
                except IndexError, e:
                    print e.message
                except ValueError, e:
                    tindex = 0
                except KeyError, e:
                    print e.message
                try:
                    onelinecourse.append(_mut_keylist[randomslot[k]][tindex])
                except IndexError, e:
                    pass
                del _mut_keylist[randomslot[k]][tindex]
                if len(_mut_keylist[randomslot[k]]) == 0:
                    del _mut_keylist[randomslot[k]]
            theline.append(onelinecourse)
            if i % self.nlesson == (self.nlesson - 1):
                theWeekline.append(copy.copy(theline))
                theline = []
        #print "多余的长度: " + str(sicencelen) + "总长度: " + str(self.phaselen * self.count)
        return theWeekline

    def decode(self,_n):
        #totallen = len(bin(self.alrange ** self.count).replace('0b',''))
        phaselen = self.phaselen
        totallen = phaselen*self.count
        phasek = (1<<phaselen) -1
        entry_n = _n

        #================================
        course_pick_list = {}
        if self.courseflg:
            course_pick = _n&(1<<self.coursecodelen -1)
            entry_n = _n >> self.coursecodelen
            for v in self.mut_keylist:
                _ktn = KTN(len(self.mut_keylist[v]))
                m = course_pick & ((1 << self.coursel_dic[v]) - 1)
                course_pick_list[v] = _ktn.An(m)
                course_pick = course_pick >> self.coursel_dic[v]
        #================================
        _mut_keylist  = copy.deepcopy(self.mut_keylist)#每次解码都复制一份keylist
        randomslot = copy.copy(_mut_keylist.keys())
        theline = []
        theWeekline = []
        sicencelen = 0#
        for i in xrange(self.count):
            current_pick = (entry_n>>(phaselen*(self.count - (i+1)))) & phasek
            _headpick = (current_pick >> (self._taillen)) & ((1<<self._headlen) -1)
            _tailpick = (current_pick) & ((1<<self._headlen) -1)
            permnumber = _tailpick % math.factorial(self.classn)
            if len(randomslot) != 0 and len(randomslot) < self.classn:
                # print "error"
                nnn = 0
                for ll in randomslot:
                    for value in _mut_keylist[ll]:
                        nnn += 1
                print nnn
                return None
            m = []
            m3 = [] #排序好的老师选取列表
            v = Util.sort_by_value(_mut_keylist)
            judge = self.count - i#(WEEKDAY - ii) * LESSON - jj
            m_i = 0
            randomslot = []
            for a in v:
                randomslot.append(a[1])
                if a[0] == judge:
                    m.append(m_i)
                m_i += 1

            if self.classn >= len(m):
                _comb = hsw_comb(self.classn - len(m),range(len(m), len(randomslot)))

                #m += random.sample(range(len(m), len(randomslot)), self.classn - len(m))
                tmp_cmb = hsw_comb.combine(len(randomslot) - len(m), self.classn-len(m))
                combnumber = _headpick % tmp_cmb
                sicencelen += self._headlen - len(bin(tmp_cmb).replace('0b',''))
                m += _comb.An(combnumber)
                m2 = self.ktn.An(permnumber+1)

                for _i in m2:
                    m3.append(m[_i])

            else:
                print "This is error!"
                exit()

            onelinecourse = []
            for k in m3:
                try:
                    #tindex = random.randrange(0, len(_mut_keylist[randomslot[k]]) - 1)
                    if self.courseflg:
                        tindex = course_pick_list[randomslot[k]].pop()
                        for vi in range(len(course_pick_list[randomslot[k]])):
                            if course_pick_list[randomslot[k]][vi] > tindex:
                                course_pick_list[randomslot[k]][vi] -= 1
                    else:
                        tindex = 0
                except IndexError, e:
                    print e.message
                except ValueError, e:
                    tindex = 0
                except KeyError, e:
                    print e.message
                try:
                    onelinecourse.append(_mut_keylist[randomslot[k]][tindex])
                except IndexError, e:
                    pass
                del _mut_keylist[randomslot[k]][tindex]
                if len(_mut_keylist[randomslot[k]]) == 0:
                    del _mut_keylist[randomslot[k]]
            theline.append(onelinecourse)
            if i % self.nlesson == (self.nlesson-1):
                theWeekline.append(copy.copy(theline))
                theline = []
        print "多余的长度: "+str(sicencelen) + "总长度: "+ str(self.phaselen*self.count)
        self.morelen = sicencelen
        return theWeekline




class HSW_encoding(object):
    def __init__(self, keylist):
        pass

def lnchoose(n, m):
    if m > n:
        return 0
        pass
    if m < n / 2.0:
        m = n - m
    s1 = 0
    for x in xrange(m + 1, n + 1):
        s1 += math.log(x)

    s2 = 0
    ub = n - m
    for x in xrange(2, ub + 1):
        s2 += math.log(x)

    return s1 - s2

def choose(n, m):
    if m > n:
        return 0
    return math.exp(lnchoose(n, m))

#全组合映射
class hsw_comb2(object):
    def __init__(self, l, M = 0):
        self.list = l
        self.set = combinations(l,M)
        self.perm = permutations(l,M)

    def An(self,x):
        #print self.set
        k = 0
        for i in self.set:
            if k == x:
                return [v for v in i]
            k += 1
        #return self.set[x]


@calctime
def mtest():
    a = permutations([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],5)

if __name__ == '__main__':
    a = hsw_comb(5,[0,1,2,3,4,5,6,7,8,9])
    print a.An(0)
    print "sssssssssßś"
    b = hsw_comb2([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13,12,5],[14],[15]],5)
    print b.An(3000)

    print choose(15,5)
    print hsw_comb.combine(15,5)

    print bin(hsw_comb.perm(10,5)**3)
    print len(bin(hsw_comb.perm(10, 5) ** 40))

    print bin(hsw_comb.perm(10, 5))

    print len(bin(hsw_comb.perm(10, 5)))

    print "-----------------------------------"

    mktn = KTN(4)
    print mktn.An(1)
