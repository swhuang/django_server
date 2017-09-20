#encoding=utf-8
import MySQLdb
import csv
import sys
import re
from collections import defaultdict
import copy
import Util


MACROTAG = "TEST1"

class classunit:
    def __init__(self,pmk = 0,teacherid = 0,courseid = 0,classid = 0,grade = 0):
        self.primary_key = pmk
        self.classid = classid
        self.courseid = courseid
        self.teacherid = teacherid
        self.grade = grade
    @property
    def primary_key(self):
        return self.primary_key
    @property
    def courseid(self):
        return self.courseid
    @property
    def classid(self):
        return self.classid
    @property
    def teacherid(self):
        return self.teacherid

def getResourcedata(conn, target_count, MACROTAG='TEST1', grade = 2):
    grade_ = grade
    resourcedata = {}
    cur = conn.cursor()
    n = cur.execute("select * from pikachutest_timetable"+MACROTAG+" where grade = '" + str(grade) +"'")
    info = cur.fetchmany(n)
    cnt = 0
    teacherdict = {}
    for ii in info:
        k = classunit(ii[1],ii[2],ii[3],ii[4],ii[5])
        """
        for space&speed sake
        """
        cnt += 1
        resourcedata[ii[1]] = k
        if teacherdict.has_key(k.teacherid):
            teacherdict[k.teacherid].append(ii[1])
        else:
            teacherdict[k.teacherid] = []
            teacherdict[k.teacherid].append(ii[1])
    """
    Do supply if less than juzhen
    """
    cnt = ii[1]
    if n < target_count:
        k = target_count - n
        v = n*2
        for i in xrange(k):
            resourcedata[cnt] = classunit()
            cnt += 1
            if teacherdict.has_key(k.teacherid):
                teacherdict[k.teacherid].append(ii[1])
            else:
                teacherdict[k.teacherid]=[]
                teacherdict[k.teacherid].append(ii[1])
    cur.close()
    conn.commit()
    return resourcedata,teacherdict

def getTeacherInfo(conn,MACROTAG='TEST1'):
    teacherinf = {}
    cur = conn.cursor()
    n = cur.execute("select * from pikachutest_teacher"+MACROTAG)
    info = cur.fetchmany(n)
    for ii in info:
        teacherinf[ii[2]] = ii[1]
    cur.close()
    conn.commit()
    return teacherinf

def getStudentInfo(conn,MACROTAG='TEST1'):
    studentinf = {}
    cur = conn.cursor()
    n = cur.execute("select * from pikachutest_student"+MACROTAG)
    info = cur.fetchmany(n)
    for ii in info:
        studentinf[ii[1]] = {}
        studentinf[ii[1]]['wuli'] = ii[2]
        studentinf[ii[1]]['huaxue'] = ii[3]
        studentinf[ii[1]]['shengwu'] = ii[4]
        studentinf[ii[1]]['zhengzhi'] = ii[5]
        studentinf[ii[1]]['lishi'] = ii[6]
        studentinf[ii[1]]['dili'] = ii[7]
        data = str(ii[2])+str(ii[3])+str(ii[4])+str(ii[5])+str(ii[6])+str(ii[7])
        data = int(data,2)
        studentinf[ii[1]]['tage'] = data
    cur.close()
    conn.commit()
    return studentinf

if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('gbk')
default_encoding = sys.getdefaultencoding()

def checktable(tablename,conn,cur):
    #cur = conn.cursor()
    sql_show_tbl = 'SHOW TABLES;'
    cur.execute(sql_show_tbl)
    tables = [cur.fetchall()]

    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]

    #cur.close()
    if tablename in table_list:
        sqli = "drop table "+tablename
        cur.execute(sqli)
        return True
    else:
        return False

def process_std(name_tag, _file,conn):
    cur = conn.cursor()
    checktable("pikachutest_student"+name_tag,conn,cur)
    sqli = "create table pikachutest_student" + name_tag + "(id int not null primary key auto_increment,studentid int,wuli int,huaxue int,shengwu int,zhengzhi int,lishi int,dili int)CHARACTER SET utf8 COLLATE utf8_general_ci;"
    try:
        cur.execute(sqli)
    except Exception, e:
        print "create table fail"
        print e.message

    sqli = "insert into pikachutest_student" + name_tag + " (studentid,wuli,huaxue,shengwu,zhengzhi,lishi,dili) values(%s,%s,%s,%s,%s,%s,%s)"

    with open(_file, 'rb') as f:
        reader = csv.reader(f)
        ii = 0
        for row in reader:
            if ii == 0:
                pass
            else:
                for m in range(len(row)):
                    if row[m] == '':
                        row[m] = '0'
                cur.execute(sqli, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                #print sqli % (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                # pass
            ii += 1

    cur.close()
    conn.commit()

def process_timetable(name_tag,_file,conn):
    cur = conn.cursor()

    checktable("pikachutest_timetable" + name_tag, conn, cur)
    sqli = "create table pikachutest_timetable" + name_tag + "(id int not null primary key auto_increment,primary_key int,teacherid int,courseid int,classid int,grade int)CHARACTER SET utf8 COLLATE utf8_general_ci;"
    try:
        cur.execute(sqli)
    except Exception, e:
        print "create table fail"
        print e.message

    sqli = "insert into pikachutest_timetable" + name_tag + " (primary_key,teacherid,courseid,classid,grade) values(%s,%s,%s,%s,%s)"
    with open(_file, 'rb') as f:
        reader = csv.reader(f)
        ii = 0
        for row in reader:
            if ii == 0:
                print row
                print row[0].encode('utf-8')
                pass
            else:
                try:
                    cur.execute(sqli, (ii, row[0], row[1], row[3], row[2]))
                    # pass
                except:
                    print "error"
                    # print row
            ii += 1
    cur.close()
    conn.commit()

def process_teacher(name_tag,_file,conn,tst=''):
    cur = conn.cursor()
    checktable("pikachutest_teacher" + name_tag, conn, cur)
    with open(_file, 'rb') as f2:
        reader = csv.reader(f2)
        sqli = "create table pikachutest_teacher"+name_tag+"(id int not null primary key auto_increment,tname varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci,tid int)CHARACTER SET utf8 COLLATE utf8_general_ci;"
        try:
            cur.execute(sqli)
        except Exception,e:
            print "create table fail"
            print e.message
            #exit()
        sqli = "insert into pikachutest_teacher"+name_tag+" (tname,tid) values(\'%s\',%s)"

        for row in reader:
            print sqli % (row[0].encode('gbk'), row[1])
            cur.execute(sqli%(row[0].encode('gbk'),row[1]))
    cur.close()
    conn.commit()

def getclassdes(str):
    pos = str.find(u'班')
    course = str[:pos]#10 class limit
    kind = str[pos+2:]
    return course+kind

@Util.calctime
def getMovingClass(maxnum = 42):
    _obj = {}
    rtdict = defaultdict(list)
    courseclass = defaultdict(list)#d
    courseclassh = defaultdict(list)
    rtvalue = defaultdict(list) #real return value
    with open('coursepick.csv','rb') as f1:
        reader = csv.reader(f1)
        ii = 0
        for row in reader:
            if ii == 0 or ii == 1:

                pass
            else:
                s = ''
                tt = []
                for k in row:
                    if len(k.encode('utf-8')) == 0:
                        k = '0'
                        pass
                    s += k.encode('utf-8') + "#"
                    tt.append(k.encode('utf-8'))
                #print s
                _obj['id'] = tt[0]
                _obj['name'] = tt[1]
                _obj['wuli'] = tt[3]
                _obj['huaxue'] = tt[4]
                _obj['shengwu'] = tt[5]
                _obj['zhengzhi'] = tt[6]
                _obj['lishi'] = tt[7]
                _obj['dili'] = tt[8]
                kd = '0b' + tt[3]+tt[4]+tt[5]+tt[6]+tt[7]+tt[8]
                _obj['kind'] = int(kd,2)
                rtdict[_obj['kind']].append(copy.copy(_obj))
                #print kd
            ii += 1
        for k in rtdict:
            if (k >> 5) == 1:#选择物理
                courseclass['wuli'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 4) & 1 == 1:#选择化学
                courseclass['huaxue'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 3) & 1 == 1: #选择生物
                courseclass['shengwu'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 2) & 1 == 1: #选择政治
                courseclass['zhengzhi'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 1) & 1 == 1: #历史
                courseclass['lishi'] += rtdict[k]#copy.copy(rtdict[k])
            if k & 1 == 1:
                courseclass['dili'] += rtdict[k]#copy.copy(rtdict[k])

        for k in rtdict:
            if (k >> 5) == 0:#选择物理
                courseclassh['wuli'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 4) & 1 == 0:#选择化学
                courseclassh['huaxue'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 3) & 1 == 0: #选择生物
                courseclassh['shengwu'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 2) & 1 == 0: #选择政治
                courseclassh['zhengzhi'] += rtdict[k]#copy.copy(rtdict[k])
            if (k >> 1) & 1 == 0: #历史
                courseclassh['lishi'] += rtdict[k]#copy.copy(rtdict[k])
            if k & 1 == 0:
                courseclassh['dili'] += rtdict[k]#copy.copy(rtdict[k])
        tm = 1
        icount = 0

        for k in courseclass:
            m = 1
            #lllen += len(courseclass[k])
            icount = 0
            for i in courseclass[k]:
                tm += 1
                i[k + u"班"] = m
                if k == 'wuli':
                    pass
                icount += 1
                if icount == maxnum:
                    m += 1
                    icount = 0

        for k in courseclassh:
            m = 1
            #lllen += len(courseclass[k])
            for i in courseclassh[k]:
                tm += 1
                i[k + u"班"+"H"] = m
                icount += 1
                if icount == maxnum:
                    m += 1
                    icount = 0

        for k in rtdict:
            l = defaultdict(int)
            for m in rtdict[k]:
                m['attendence'] = []
                if m.has_key(u"wuli班"):
                    l[u"wuli班"+str(m[u"wuli班"])] = 0
                    m['attendence'].append(u"wuli班"+str(m[u"wuli班"])+'D')
                else:
                    l[u"wuli班" + str(m[u"wuli班H"])] = 1
                    m['attendence'].append(u"wuli班" + str(m[u"wuli班H"]) + 'H')

                if m.has_key(u"huaxue班"):
                    l[u"huaxue班"+str(m[u"huaxue班"])] = 0
                    m['attendence'].append(u"huaxue班"+str(m[u"huaxue班"]) + 'D')
                else:
                    l[u"huaxue班" + str(m[u"huaxue班H"])] = 1
                    m['attendence'].append(u"huaxue班" + str(m[u"huaxue班H"]) + 'H')

                if m.has_key(u"shengwu班"):
                    l[u"shengwu班"+str(m[u"shengwu班"])] = 0
                    m['attendence'].append(u"shengwu班"+str(m[u"shengwu班"]) + 'D')
                else:
                    l[u"shengwu班" + str(m[u"shengwu班H"])] = 1
                    m['attendence'].append(u"shengwu班" + str(m[u"shengwu班H"]) + 'H')

                if m.has_key(u"zhengzhi班"):
                    l[u"zhengzhi班"+str(m[u"zhengzhi班"])] = 0
                    m['attendence'].append(u"zhengzhi班"+str(m[u"zhengzhi班"]) + 'D')
                else:
                    l[u"zhengzhi班" + str(m[u"zhengzhi班H"])] = 1
                    m['attendence'].append(u"zhengzhi班" + str(m[u"zhengzhi班H"]) + 'H')

                if m.has_key(u"lishi班"):
                    l[u"lishi班"+str(m[u"lishi班"])] = 0
                    m['attendence'].append(u"lishi班"+str(m[u"lishi班"]) + 'D')
                else:
                    l[u"lishi班" + str(m[u"lishi班H"])] = 1
                    m['attendence'].append(u"lishi班" + str(m[u"lishi班H"]) + 'H')

                if m.has_key(u"dili班"):
                    l[u"dili班"+str(m[u"dili班"])] = 0
                    m['attendence'].append(u"dili班"+str(m[u"dili班"]) + 'D')
                else:
                    l[u"dili班" + str(m[u"dili班H"])] = 1
                    m['attendence'].append(u"dili班" + str(m[u"dili班H"]) + 'H')

            for key in l:
                m = {}
                m['class'] = copy.copy(key)
                if l[key] == 0:
                    m['kind'] = 'D'
                else:
                    m['kind'] = 'H'

                m['id'] = key + m['kind']
                rtvalue[k].append(copy.copy(m))
            l.clear()

        tmpct = defaultdict(int)
        for mk in rtvalue:
            for i in rtvalue[mk]:
                tmpct[i['id']] = 0
        '''
        for k in tmpct:
            print k
        print len(tmpct)
        '''

        rtstdDic = {}
        for l in rtdict:
            for ele in rtdict[l]:
                #silly dude
                tmp = ''
                if ele.has_key(u'dili班'):
                    tmp += str(ele[u'dili班'])
                else:
                    tmp += str(ele[u'dili班H'])

                if ele.has_key(u'huaxue班'):
                    tmp += str(ele[u'huaxue班'])
                else:
                    tmp += str(ele[u'huaxue班H'])

                if ele.has_key(u'lishi班'):
                    tmp += str(ele[u'lishi班'])
                else:
                    tmp += str(ele[u'lishi班H'])

                if ele.has_key(u'shengwu班'):
                    tmp += str(ele[u'shengwu班'])
                else:
                    tmp += str(ele[u'shengwu班H'])

                if ele.has_key(u'wuli班'):
                    tmp += str(ele[u'wuli班'])
                else:
                    tmp += str(ele[u'wuli班H'])

                if ele.has_key(u'zhengzhi班'):
                    tmp += str(ele[u'zhengzhi班'])
                else:
                    tmp += str(ele[u'zhengzhi班H'])

                ele['spec'] = str(ele['kind'])+tmp
                if not rtstdDic.has_key(ele['spec']):
                    rtstdDic[ele['spec']] = {}
                    rtstdDic[ele['spec']]['course'] = []
                    rtstdDic[ele['spec']]['course'] = copy.copy(ele['attendence'])

        #
        tmpjudge = defaultdict(int)
        tmpjudge['huaxueD'] = 2
        tmpjudge['huaxueH'] = 3
        tmpjudge['wuliD'] = 3
        tmpjudge['wuliH'] = 3
        tmpjudge['zhengzhiD'] = 3
        tmpjudge['zhengzhiH'] = 0
        tmpjudge['lishiD'] = 3
        tmpjudge['lishiH'] = 0
        tmpjudge['diliD'] = 4
        tmpjudge['diliH'] = 0
        tmpjudge['shengwuD'] = 4
        tmpjudge['shengwuH'] = 0

        for k in rtstdDic:
            for m in copy.copy(rtstdDic[k]['course']):
                cnt = tmpjudge[getclassdes(m)]
                if cnt == 0:
                    rtstdDic[k]['course'].remove(m)
                if cnt > 1:
                    for s in xrange(cnt - 1):
                        rtstdDic[k]['course'].append(m)

        return rtstdDic,tmpct,rtdict

class MovingClass(object):
    def __init__(self):
        self.std, self.classnum, self.stddict = getMovingClass()
        self.num = 0

    def delcourse(self,_c = u""):
        for k in copy.copy(self.std):
            if _c in self.std[k]['course']:
                self.std[k]['course'].remove(_c)
                if len(self.std[k]['course']) == 0:
                    del self.std[k]


    def pick_course(self,_n,maxn = 9):
        #test sort
        retlist = []
        totlen = 0
        for k in self.std:
            self.std[k]['selectable'] = True

        l = len(bin(len(self.std)).replace('0b',""))
        _index1 = (self.num & ((1<<l) -1)) % len(self.std)
        self.num = self.num >> l
        totlen += l
        l = len(bin(len(self.std[self.std.keys()[_index1]]['course'])).replace('0b',""))
        try:
            _index2 = (self.num & ((1<<l) -1)) % len(self.std[self.std.keys()[_index1]]['course'])
        except ZeroDivisionError,e:
            _index2 = 0
            print self.num
        self.num = self.num >> l
        totlen += l

        m = self.std[self.std.keys()[_index1]]['course'][_index2]
        if m == u'lishi班2D':
            pass
        _Falselist = {}
        for kk in self.std:
            if kk == '41121111':
                pass
            if m in self.std[kk]['course']:
                for ii in self.std[kk]['course']:
                    _Falselist[ii] = True

        _kdict = copy.deepcopy(self.std)
        for i in range(maxn):
            retlist.append(m)
            tmp = m
            if m == u'lishi班2D':
                pass
            icnt = 0
            for k in copy.copy(_kdict):
                if k == '14143332':
                    pass
                if m in _kdict[k]['course'] and _kdict[k]['selectable']:
                    _kdict[k]['selectable'] = False
                    for ii in _kdict[k]['course']:
                        _Falselist[ii] = True
                    _kdict[k]['course'].remove(m)
                    if len(_kdict[k]['course']) == 0:
                        del _kdict[k]

                elif _kdict[k]['selectable']:
                    for _i in copy.copy(_kdict[k]['course']):
                        if _i in _Falselist.keys():
                            _kdict[k]['course'].remove(_i)
                    if len(_kdict[k]['course']) != 0:
                        icnt += 1
                    else:
                        _kdict[k]['selectable'] = False
                        del _kdict[k]
            self.delcourse(m)

            if icnt == 0:
                #print "pick end!"+str(i)
                break
            if icnt == 1:
                _index1 = 0
            else:
                l = len(bin(icnt).replace('0b', ""))
                _index1 = (self.num & ((1 << l) - 1)) % icnt
                self.num = self.num >> l
                totlen += l

            '''
            l = len(bin(len(self.std[self.std.keys()[_index1]]['course'])).replace('0b', ""))
            _index2 = self.num & ((1 << l) - 1)
            self.num = self.num >> l
            '''
            icnt = 0
            for k2 in _kdict:
                if _kdict[k2]['selectable'] == True and len(_kdict[k2]['course']) > 0:

                    if icnt == _index1:
                        l = len(bin(len(_kdict[k2]['course'])).replace('0b', ""))
                        if l == 1:
                            _index2 = 0
                        else:
                            _index2 = (self.num & ((1 << l) - 1)) % len(_kdict[k2]['course'])
                            self.num = self.num >> l
                            totlen += l
                        m = _kdict[k2]['course'][_index2]
                        for ii in _kdict[k2]['course']:
                            _Falselist[ii] = True
                        #break
                    icnt += 1
                    '''
                    if m in _kdict[k2]['course']:
                        for ii in _kdict[k2]['course']:
                            _Falselist[ii] = True
                    '''
                else:
                    pass
            if tmp == m:
                print "enderror!"
            else:
                for km in _kdict:
                    if m in _kdict[km]['course'] and _kdict[km]['selectable']:
                        _kdict[km]['selectable'] = False
                        for im in _kdict[km]['course']:
                            _Falselist[im] = True

        return retlist,totlen

    def run(self,n):
        a = []
        self.num = n
        _len = 0
        ist = 0
        tmp = copy.deepcopy(self.std)
        while len(self.std) != 0:
            k,lens = self.pick_course(2)
            _len += lens
            a.append(k)
            ist+=1

        #print "长度："+str(_len)
        if ist <= 20:
            print "success! "+ str(ist)
            if self.validation(a):
                print a
        self.std = tmp
        self.num = n

    def validation(self,result):
        _m = {}
        for i in range(len(result)):
            for j in range(len(result[i])):
                _m[result[i][j]] = i

        _kcount = 0
        p = []
        for o in result:
            if len(o) == 8:
                p = o

        for km in self.stddict:
            tmp = [val for val in self.stddict[km][0]['attendence'] if val in p]
            print tmp
            if len(tmp) >0:
                _kcount += 1
            else:
                pass

        if _kcount != 17:
            pass
        print "test string:"+str(_kcount)

        for k in self.stddict:
            for std in self.stddict[k]:
                judge = defaultdict(int)
                for cs in std['attendence']:
                    if _m.has_key(cs):
                        judge[_m[cs]]+=1
                        if judge[_m[cs]] > 1:
                            print "strong error"
                            return False
        return True




if __name__ == '__main__':
    conn = MySQLdb.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='vq8612VQE',
                           db='mysql',
                           charset="utf8")
    cur = conn.cursor()
    name_tag = 0#sys.argv[1]

    #getMovingClass()
    a = MovingClass()
    #a.pick_course(2)
    _range = (1 << 704)
    import random
    for i in range(100000):
        key = random.randint(0, _range)
        #a.run(636746597678)
        a.run(key)
    cur.close()
    conn.commit()
    conn.close()
    exit()
    """
    Insert Student data
    """

    sqli = "create table pikachutest_student" + name_tag + "(id int not null primary key auto_increment,studentid int,wuli int,huaxue int,shengwu int,zhengzhi int,lishi int,dili int)CHARACTER SET utf8 COLLATE utf8_general_ci;"
    try:
        cur.execute(sqli)
    except Exception, e:
        print "create table fail"
        print e.message

    sqli="insert into pikachutest_student"+name_tag+" (studentid,wuli,huaxue,shengwu,zhengzhi,lishi,dili) values(%s,%s,%s,%s,%s,%s,%s)"

    with open('student.csv', 'rb') as f:
        reader = csv.reader(f)
        ii = 0
        for row in reader:
            if ii == 0:
                print row
                print row[0].encode('utf-8')
                pass
            else:
                for m in range(len(row)):
                    if row[m] == '':
                        row[m] = '0'
                cur.execute(sqli,(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                print sqli%(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    #pass
            ii += 1
    #===============================

    sqli = "create table pikachutest_timetable" + name_tag + "(id int not null primary key auto_increment,primary_key int,teacherid int,courseid int,classid int,grade int)CHARACTER SET utf8 COLLATE utf8_general_ci;"
    try:
        cur.execute(sqli)
    except Exception, e:
        print "create table fail"
        print e.message

    sqli="insert into pikachutest_timetable"+name_tag+" (primary_key,teacherid,courseid,classid,grade) values(%s,%s,%s,%s,%s)"
    with open('eggtmp.csv', 'rb') as f:
        reader = csv.reader(f)
        ii = 0
        for row in reader:
            if ii == 0:
                print row
                print row[0].encode('utf-8')
                pass
            else:
                try:
                    cur.execute(sqli,(ii,row[0],row[1],row[3],row[2]))
                    #pass
                except:
                    print "error"
                #print row
            ii += 1

    with open('eggte2.csv', 'rb') as f2:
        reader = csv.reader(f2)
        sqli = "create table pikachutest_teacher"+name_tag+"(id int not null primary key auto_increment,tname varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci,tid int)CHARACTER SET utf8 COLLATE utf8_general_ci;"
        try:
            cur.execute(sqli)
        except Exception,e:
            print "create table fail"
            print e.message
            #exit()
        sqli = "insert into pikachutest_teacher"+name_tag+" (tname,tid) values(\'%s\',%s)"

        for row in reader:
            print sqli % (row[0].encode('utf-8'), row[1])
            cur.execute(sqli%(row[0].encode('utf-8'),row[1]))

    #cur.execute(sqli,('2','2','2','9','2'))
    #cur.execute("insert into pikachutest_timetable values('2','2','2','9','2')")
    cur.close()
    conn.commit()
    conn.close()