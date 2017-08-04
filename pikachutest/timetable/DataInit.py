
import MySQLdb
import csv
import sys
import re

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

if __name__ == '__main__':
    conn = MySQLdb.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='vq8612VQE',
                           db='mysql',
                           charset="utf8")
    cur = conn.cursor()
    name_tag = sys.argv[1]

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