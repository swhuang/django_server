# encoding=utf-8

import math
import random
import operator
import copy
import DataInit
import sys
import MySQLdb
import time
import Util
import os
from collections import defaultdict
import GA_encoding.GA_ENCODE as GA_encode

conn = MySQLdb.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='vq8612VQE',
                       db='mysql',
                       charset="utf8")

if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('gbk')
default_encoding = sys.getdefaultencoding()

CLASSN = 5  # 14
COURSE = 9
LESSON = 3  # 8
WEEKDAY = 1  # 5
# GRADE = 3

RANGEWHAT = 0  # 0:排合格；1:排等级

resourcedata, teacherclsdict = DataInit.getResourcedata(conn, WEEKDAY * LESSON * CLASSN)
reslist = []
for key in resourcedata:
    reslist.append(key)

coursedict = {}
coursedict[2] = u"数学"
coursedict[1] = u"语文"
coursedict[3] = u"英语"
coursedict[5] = u"物理"
coursedict[6] = u"化学"
coursedict[10] = u"政治"
coursedict[7] = u"生物"
coursedict[8] = u"历史"
coursedict[9] = u"地理"
coursedict[4] = u"体育"
coursedict[11] = u"信息"
coursedict[12] = u"校"
coursedict[13] = u"技"
coursedict[14] = u"艺术"
coursedict[15] = u"班"
coursedict[16] = u"社"
coursedict[17] = u"加"

teacherdict = DataInit.getTeacherInfo(conn)

MACROTAG = ""

MAXROOM = 40
'''
语	1
数	2
英	3
体	4
物	5
化	6
生	7
历	8
地	9
政	10
信	11
校	12
技	13
艺	14
班	15
社	16
加	17
	18
	19
	20
	21
	22
	23
	24
	25
'''

"""
id -> classunit
"""


def getClassUnit(id):
    return resourcedata[id]


def moduleInit(macrotag):
    resourcedata, teacherclsdict = DataInit.getResourcedata(conn, WEEKDAY * LESSON * CLASSN, macrotag)
    teacherdict = DataInit.getTeacherInfo(conn, macrotag)
    MACROTAG = macrotag


#
# chromosome int array
# chromosome -> tablematrix
#
# @Util.calctime
def generatedata(chromosome):
    tablematrix = []
    n = 0
    for i in range(WEEKDAY):
        weekday = []
        for j in range(LESSON):
            lesson = []
            for k in range(CLASSN):
                try:
                    lesson.append(chromosome[n])
                    n = n + 1
                except IndexError, e:
                    lesson.append(0)
            weekday.append(lesson)
        tablematrix.append(weekday)
    return tablematrix


#
# tablematrix -> chromosome
#
def processdata(tablematrix):
    chromosome = []
    for i in range(WEEKDAY):
        for j in range(LESSON):
            for k in range(CLASSN):
                try:
                    chromosome.append(tablematrix[i][j][k])
                except IndexError, e:
                    chromosome.append(0)
    return chromosome


'''
从1开始
KTN（4）0,1,2,3   4个数字全排列
康托展开
'''


class KTN():
    def __init__(self, N):
        self.maxn = N
        self.fablist = []
        self.fablist.append(1)
        for i in range(N):
            self.fablist.append(math.factorial(i + 1))
        self.listdict = {}

    def X(self, list):
        lens = len(list)
        ans = 0
        for i in xrange(lens):
            x = 0
            for j in xrange(i + 1, lens):
                if list[j] < list[i]:
                    x += 1
            # ans += x * math.factorial(lens-i-1)
            ans += x * self.fablist[lens - i - 1]
        ans += 1

        return ans

    # @Util.calctime
    def An(self, X):
        if self.listdict.has_key(X):
            print "reduced!"
            return self.listdict[X]
        n = self.maxn
        showed = []
        ans = []
        for i in xrange(n + 1):
            showed.append(False)
        for i in xrange(n):
            ans.append(0)
        tmp = X
        X -= 1
        for i in xrange(n):
            # numOfMin = X / math.factorial(n-1-i)
            numOfMin = X / self.fablist[n - 1 - i]
            # X = X % math.factorial(n - 1 - i)
            X = X % self.fablist[n - 1 - i]
            j = 0
            k = 0
            while j <= numOfMin:
                try:
                    if showed[k] == False:
                        j += 1
                except IndexError, e:
                    print e.message
                    print "kkk:" + str(n)
                    print "errornumber:" + str(tmp)
                    print "K value:" + str(k)
                    exit()
                k += 1
            k -= 1
            ans[i] = k;
            showed[ans[i]] = True
        for i in xrange(n):
            ans[i] += 1
        self.listdict[X] = ans
        return ans


"""
软约束函数列表
"""


####################
def ContinousClass(tablematrix, ii=WEEKDAY, jj=LESSON, kk=CLASSN):
    marks = 0
    for i in xrange(ii):
        for k in xrange(kk):
            cls_dict = {}
            for j in xrange(jj):
                if j > 1:
                    if getClassUnit(tablematrix[i][j][k]).courseid == getClassUnit(tablematrix[i][j - 1][k]).courseid:
                        marks += 1
    return marks


def majorCourse(tablematrix, ii=WEEKDAY, jj=LESSON, kk=CLASSN):
    marks = 0
    for i in xrange(ii):
        for k in xrange(kk):
            cls_dict = {}
            for j in xrange(jj):
                if j > 1:
                    if getClassUnit(tablematrix[i][j][k]).courseid == getClassUnit(tablematrix[i][j - 1][k]).courseid:
                        marks += 1
    return marks


####################
class staticcoursedic(object):
    def __init__(self):
        self.dict = defaultdict(int)

    def addele(self, cs, pos):
        self.dict[cs] = pos

    @property
    def dict(self):
        assert isinstance(self.dict, object)
        return self.dict


#####################
# 获取课程基础算法
@Util.calctime
def gen_coursematrix(TclsList):
    keylist = copy.deepcopy(TclsList)
    choromosome = []
    randomslot = copy.deepcopy(keylist.keys())
    for ii in xrange(WEEKDAY):
        weekday = []
        for jj in xrange(LESSON):
            theline = []

            if len(randomslot) != 0 and len(randomslot) < CLASSN:
                # print "error"
                nnn = 0
                for ll in randomslot:
                    for value in keylist[ll]:
                        nnn += 1
                print nnn
                return None
            # 稀少物种保护政策
            m = []
            v = Util.sort_by_value(keylist)
            judge = (WEEKDAY - ii) * LESSON - jj
            m_i = 0
            randomslot = []
            for a in v:
                randomslot.append(a[1])
                if a[0] == judge:
                    m.append(m_i)
                m_i += 1

            if CLASSN >= len(m):
                m += random.sample(range(len(m), len(randomslot)), CLASSN - len(m))
            else:
                print "This is error!"
                exit()
            for k in m:
                try:
                    tindex = random.randrange(0, len(keylist[randomslot[k]]) - 1)
                except IndexError, e:
                    print e.message
                except ValueError, e:
                    tindex = 0
                except KeyError, e:
                    print e.message
                try:
                    theline.append(keylist[randomslot[k]][tindex])
                except IndexError, e:
                    pass
                del keylist[randomslot[k]][tindex]
                if len(keylist[randomslot[k]]) == 0:
                    del keylist[randomslot[k]]
            # randomslot = copy.deepcopy(keylist.keys())
            random.shuffle(theline)
            weekday.append(theline)
        random.shuffle(weekday)
        choromosome.append(weekday)
    # random.shuffle(choromosome)

    return choromosome


def generate_coursematrix(TclsList):
    # mlist = 排序好的【课程个数，老师id,课程列表】
    keylist = copy.deepcopy(TclsList)
    choromosome = []
    # mlist = Util.sort_by_value(keylist)
    for ii in xrange(WEEKDAY):
        weekday = []
        for jj in xrange(LESSON):
            mlist = Util.sort_by_value(keylist)
            if len(mlist) < CLASSN:
                print "actually error"
                for i in xrange(CLASSN - len(mlist)):
                    mlist.append([0, 0, []])

            pcurrent = mlist[CLASSN - 1][0]
            n1 = 1  # 最后一位老师种类的个数
            n2 = 0
            while mlist[CLASSN - n1 - 1][0] == pcurrent:
                n1 += 1
                if n1 == CLASSN:
                    break

            try:
                while mlist[CLASSN + n2][0] == pcurrent:
                    n2 += 1
                    if CLASSN + n2 == len(mlist):
                        break
            except IndexError, e:
                print e.message
                pass

            theline = []

            if mlist[0][0] == 2:
                pass

            if n2 == 0:
                for i in xrange(CLASSN):
                    tindex = random.randrange(0, len(mlist[i][2]))
                    theline.append(mlist[i][2][tindex])
                    del mlist[i][2][tindex]
                    if len(mlist[i][2]) == 0:
                        del keylist[mlist[i][1]]
                        del mlist[i]
            else:
                try:
                    mindex = random.sample(range(CLASSN - n1, CLASSN + n2), n1)
                except ValueError, e:
                    print e.message
                    exit()

                if n1 != CLASSN:
                    for i in xrange(CLASSN - n1):
                        tindex = random.randrange(0, len(mlist[i][2]))
                        theline.append(mlist[i][2][tindex])
                        del mlist[i][2][tindex]
                        if len(mlist[i][2]) == 0:
                            del keylist[mlist[i][1]]
                            del mlist[i]

                for k in mindex:
                    try:
                        tindex = random.randrange(0, len(mlist[k][2]))
                    except ValueError, e:
                        tindex = 0
                    except IndexError, e:
                        pass
                    try:
                        theline.append(mlist[k][2][tindex])
                    except IndexError, e:
                        pass
                    try:
                        del mlist[k][2][tindex]
                    except IndexError, e:
                        pass
                    if len(mlist[k][2]) == 0:
                        del keylist[mlist[k][1]]
                        del mlist[k]
            random.shuffle(theline)
            weekday.append(theline)
            # keylist = mlist
        random.shuffle(weekday)
        choromosome.append(weekday)
    random.shuffle[choromosome]

    return choromosome


class Ctablematrix:
    def __init__(self, mtb):
        self.qtb = copy.deepcopy(mtb)
        self.tb = copy.deepcopy(mtb)
        self.countdict = defaultdict(int)

        cdict = {}
        for i in xrange(WEEKDAY):
            for j in xrange(LESSON):
                for k in xrange(CLASSN):
                    ele = getClassUnit(self.tb[i][j][k])

                    mm = 0
                    if cdict.has_key(ele.courseid):
                        cdict[ele.courseid] += 1
                        mm = cdict[ele.courseid]
                    else:
                        cdict[ele.courseid] = 1
                        mm = 1

                    self.tb[i][j][k] = (self.tb[i][j][k], mm)

    def fetchcourse(self, courseid, student):
        IsOK = True
        for i in xrange(WEEKDAY):
            for j in xrange(LESSON):
                for k in xrange(CLASSN):
                    ele = getClassUnit(self.tb[i][j][k][0])
                    if ele.courseid == courseid:
                        if self.countdict.has_key(self.tb[i][j][k][0]):
                            if self.countdict[self.tb[i][j][k][0]] < MAXROOM:
                                IsOK = True
                                '''
                                check redundencey course
                                '''
                                for iq in range(len(student["attendence"])):
                                    if student["attendence"][iq] in self.qtb[i][j]:
                                        IsOK = False
                                        break
                                if IsOK == True:
                                    self.countdict[self.tb[i][j][k][0]] += 1
                                    student['attendence'].append(self.tb[i][j][k][0])
                                    # student["desc"].append((coursedict[courseid] + str(self.tb[i][j][k][1]) + u"班").encode("utf-8"))
                                    return (ele, self.tb[i][j][k][1])
                        else:
                            IsOK = True
                            for iq in range(len(student["attendence"])):
                                if student["attendence"][iq] in self.qtb[i][j]:
                                    IsOK = False
                                    break
                            if IsOK == True:
                                self.countdict[self.tb[i][j][k][0]] = 1
                                student['attendence'].append(self.tb[i][j][k][0])
                                # student["desc"].append(
                                #    (coursedict[courseid] + str(self.tb[i][j][k][1]) + u"班").encode("utf-8"))
                                return (ele, self.tb[i][j][k][1])
                                #        print self.qtb
                                #        print str(student).decode('string_escape')
        if len(student["attendence"]) == 2:
            rst = []
            for m in range(len(self.qtb[0])):
                try:
                    k1 = self.qtb[0][m].index(student["attendence"][0])
                    rst.append((k1, m))
                except:
                    k1 = -1
                try:
                    k1 = self.qtb[0][m].index(student["attendence"][1])
                    rst.append((k1, m))
                except:
                    k1 = -1
            rest = 3 - rst[0][1] - rst[1][1]  # 获取空行
            _i = 0

            tmpcsid = getClassUnit(self.qtb[0][rst[0][1]][rst[0][0]]).courseid
            for mi in self.qtb[0][rest]:
                if getClassUnit(mi).courseid == tmpcsid and self.countdict[mi] < MAXROOM:
                    for mj in self.qtb[0][rst[0][1]]:
                        if courseid == getClassUnit(mj).courseid and self.countdict[mj] < MAXROOM:
                            student['attendence'].append(mj)
                            self.countdict[mj] += 1
                            student['attendence'].remove(self.qtb[0][rst[0][1]][rst[0][0]])
                            self.countdict[self.qtb[0][rst[0][1]][rst[0][0]]] -= 1
                            student['attendence'].append(mi)
                            self.countdict[mi] += 1
                            # student["desc"].append(
                            #    (coursedict[courseid] + str(self.tb[0][rst[0][1]][_i][1]) + u"班").encode("utf-8"))
                            return (getClassUnit(mj), self.tb[0][rst[0][1]][_i][1])
                        _i += 1

            tmpcsid = getClassUnit(self.qtb[0][rst[1][1]][rst[1][0]]).courseid
            _i = 0
            for mi in self.qtb[0][rest]:
                if getClassUnit(mi).courseid == tmpcsid and self.countdict[mi] < MAXROOM:
                    for mj in self.qtb[0][rst[1][1]]:
                        if courseid == getClassUnit(mj).courseid and self.countdict[mj] < MAXROOM:
                            student['attendence'].append(mj)
                            self.countdict[mj] += 1
                            student['attendence'].remove(self.qtb[0][rst[1][1]][rst[1][0]])
                            self.countdict[self.qtb[0][rst[1][1]][rst[1][0]]] -= 1
                            student['attendence'].append(mi)
                            self.countdict[mi] += 1
                            # student["desc"].append(
                            #    (coursedict[courseid] + str(self.tb[0][rst[1][1]][_i][1]) + u"班").encode("utf-8"))
                            return (getClassUnit(mj), self.tb[0][rst[1][1]][_i][1])
                        _i += 1
            pass
        return None


class GA():
    def __init__(self, count, softorderlist, MAXCOUNT):
        # 康托展开
        # 将课程全排列映射成数字作为染色体
        self.kt_chromosome = KTN(WEEKDAY * LESSON * CLASSN)
        # 染色体长度
        self.length = 0  # len(bin(math.factorial(WEEKDAY*LESSON*CLASSN)))-2#length
        # 种群中的染色体数量
        self.count = count

        self.allkindcnt = 0  # math.factorial(WEEKDAY*LESSON*CLASSN)
        # 软约束列表
        self.softorderlist = softorderlist

        self.evolvecnt = 0

        self.allkindlist = []

        self.badlist = []

        self.basepopulation = []

        self.remarks = 0

        self.population = []

        self.tmpk = defaultdict(int)  # 课程班级字典

        self.studentdict = DataInit.getStudentInfo(conn)

        mteacherdict = copy.deepcopy(teacherclsdict)
        self.teacherkeylist = {}
        for k in mteacherdict:
            self.teacherkeylist[k] = len(mteacherdict[k])

        self.init_basepopulation(MAXCOUNT)
        # 随机生成初始种群
        # self.population = self.gen_population(self.length, count)

    @Util.calctime
    def evolve(self, retain_rate=0.2, random_select_rate=0.5, mutation_rate=0.01):
        """
        进化
        对当前一代种群依次进行选择、交叉并生成新一代种群，然后对新一代种群进行变异
        """
        parents = self.selection(retain_rate, random_select_rate)
        self.crossover(parents)
        self.mutation(mutation_rate)

        self.evolvecnt += 1
        print "evolving times: " + str(self.evolvecnt)

    # @Util.calctime
    def init_chromosome(self, teacherclsdict):

        mteacherdict = copy.deepcopy(teacherclsdict)
        keylist = mteacherdict.keys()

        rt = gen_coursematrix(teacherclsdict)

        chrom = rt
        marks = self.fitness(chrom, self.softorderlist)

        # ret = self.kt_chromosome.X(processdata(chrom))
        return (chrom, marks)

    def furtherprocess(self, tb_matrix):
        studentdict = copy.deepcopy(self.studentdict)  # DataInit.getStudentInfo(conn)
        judgedata = {}
        mtbl = Ctablematrix(tb_matrix)
        for k in studentdict:
            if k == 180538:
                pass
            if judgedata.has_key(studentdict[k]['tage']):
                judgedata[studentdict[k]['tage']].append(k)
            else:
                judgedata[studentdict[k]['tage']] = []
                judgedata[studentdict[k]['tage']].append(k)

            # studentdict[k]["desc"] = []
            studentdict[k]["attendence"] = []
            if studentdict[k]['wuli'] == RANGEWHAT:  # 0表示合格考
                course = mtbl.fetchcourse(5, studentdict[k])
                if course == None:
                    # print "fetchcourse error"
                    return -1
                    # studentdict[k]["desc"].append((u"物理"+str(course[1])+u"班").encode("utf-8"))
                    # studentdict[k]["attendence"].append(course[0].primary_key)
            if studentdict[k]['huaxue'] == RANGEWHAT:  # 0表示合格考
                course = mtbl.fetchcourse(6, studentdict[k])
                if course == None:
                    # print "fetchcourse error"
                    return -1
                    # studentdict[k]["desc"].append((u"化学"+str(course[1])+u"班").encode("utf-8"))
                    # studentdict[k]["attendence"].append(course[0].primary_key)
            if studentdict[k]['shengwu'] == RANGEWHAT:  # 0表示合格考
                course = mtbl.fetchcourse(7, studentdict[k])
                if course == None:
                    # print "fetchcourse error"
                    return -1
                    # studentdict[k]["desc"].append((u"生物"+str(course[1])+u"班").encode("utf-8"))
                    # studentdict[k]["attendence"].append(course[0].primary_key)
            if studentdict[k]['zhengzhi'] == RANGEWHAT:  # 0表示合格考
                course = mtbl.fetchcourse(10, studentdict[k])
                if course == None:
                    # print "fetchcourse error"
                    return -1
                    # studentdict[k]["desc"].append((u"政治"+str(course[1])+u"班").encode("utf-8"))
                    # studentdict[k]["attendence"].append(course[0].primary_key)
            if studentdict[k]['lishi'] == RANGEWHAT:  # 0表示合格考
                course = mtbl.fetchcourse(8, studentdict[k])
                if course == None:
                    # print "fetchcourse error"
                    return -1
                    # studentdict[k]["desc"].append((u"历史"+str(course[1])+u"班").encode("utf-8"))
                    # studentdict[k]["attendence"].append(course[0].primary_key)
            if studentdict[k]['dili'] == RANGEWHAT:  # 0表示合格考
                course = mtbl.fetchcourse(9, studentdict[k])
                if course == None:
                    # print "fetchcourse error"
                    return -1
                    # studentdict[k]["desc"].append((u"地理"+str(course[1])+u"班").encode("utf-8"))
                    # studentdict[k]["attendence"].append(course[0].primary_key)

                    # tt= []
                    # tt.append("物理"+str(course[1])+"班")
                    # print str(tt).decode('string_escape')
        return studentdict

    def furtherprocess2(self):
        studentdict = copy.deepcopy(self.studentdict)  # DataInit.getStudentInfo(conn)
        judgedata = {}
        # mtbl = Ctablematrix(tb_matrix)
        tmptbl = []
        lesson1 = []
        lesson2 = []
        lesson3 = []
        tmptbl.append(lesson1)
        tmptbl.append(lesson2)
        tmptbl.append(lesson3)
        for k in studentdict:
            if k == 180538:
                pass
            if judgedata.has_key(studentdict[k]['tage']):
                judgedata[studentdict[k]['tage']].append(k)
            else:
                judgedata[studentdict[k]['tage']] = []
                judgedata[studentdict[k]['tage']].append(k)

        return studentdict

    def exportstudent(self, studentdict):
        import csv
        import codecs
        if not os.path.isdir("data/" + MACROTAG + "/result/student"):
            os.makedirs("data/" + MACROTAG + "/result/student")
        with open("data/" + MACROTAG + "/result/student/" + 'std' + str(
                time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.csv', 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for k in studentdict:
                colname = []
                colname.append(str(k))
                studentdict[k]['desc'] = []
                for lk in studentdict[k]["attendence"]:
                    ele = getClassUnit(lk)
                    studentdict[k]['desc'].append(
                        (coursedict[ele.courseid] + str(self.tmpk[lk]) + u"班").encode("utf-8"))
                for mk in studentdict[k]:
                    if mk == 'desc':
                        colname.append(str(studentdict[k][mk]).decode('string_escape'))
                spamwriter.writerow(colname)
        print str(studentdict).decode('string_escape')
        return 0

    @Util.calctime
    def init_basepopulation(self, count):
        self.basepopulation = []
        k = 0
        kk = 0
        cnt = 0
        tmpstudent = object
        store = object
        # self.furtherprocess2()
        for i in xrange(count):
            kk += 1
            cnt += 1
            if kk == 1000:
                print kk
                kk = 0
            m = self.init_chromosome(teacherclsdict)
            tmpstudent = self.furtherprocess(m[0])
            if tmpstudent == -1:
                # m[1] -=100
                continue

            if cnt == 10000:
                print "score: " + str(m[1])
                self.exportresult(m[0])

            if m[1] >= k:
                k = m[1]
                print "get answer +++++++++++++"
                self.basepopulation = m[0]
                store = tmpstudent

        self.exportresult(self.basepopulation)
        self.exportstudent(store)
        print "get higher:" + str(k)
        """
        for i in xrange(count):
            self.basepopulation.append(self.init_chromosome(teacherclsdict))
            k += 1
            if k == 1000:
                k = 0
                print i
        self.length = len(bin(count)) - 2  # length
        self.allkindcnt = count
        """

    def gen_chromosome(self, length):
        """
        随机生成长度为length的染色体，每个基因的取值是0或1
        这里用一个bit表示一个基因
        """
        index = random.randint(0, self.allkindcnt - 1)
        if index in self.allkindlist:
            index = self.gen_chromosome(length)
        else:
            self.allkindlist.append(index)

        return index
        elem = self.kt_chromosome.An(index)
        if 561 in elem:
            print "working!:" + str(elem)
            print "wocao error!" + str(index)
        if self.strongjudge(generatedata(elem)) == False:
            self.allkindlist.append(index)
            return self.gen_chromosome(length)
        else:
            # tmpk = self.kt_chromosome.X(chromosome_)
            # print "getcurrent chromosome: " + str(elem)
            return index

    @Util.calctime
    def gen_population(self, length, count):
        """
        获取初始种群（一个含有count个长度为length的染色体的列表）
        对初始种群进行筛选以免过早陷入局部最优解
        """

        population = []

        for i in xrange(count):
            population.append(self.gen_chromosome(length))

        return population
        return self.basepopulation

    def chromosome2data(self, chromosome):

        pass

    def fitness(self, chromosome, rule=[]):
        """
        计算适应度，将染色体解码为0~9之间数字，代入函数计算
        因为是求最大值，所以数值越大，适应度越高
        """
        if chromosome in self.badlist:
            #    print "get duplicated number"
            #    print chromosome
            return -100
        """
        if chromosome > self.allkindcnt:
            print "error chromosome:"+str(chromosome)
            exit()
        x = self.decode(chromosome)
        """
        x = chromosome
        remarks = 0
        """
        硬约束评分规则
        """
        if self.strongjudge(x) == False:
            remarks -= 100
        """
        软约束评分规
        """
        for func in rule:
            remarks += func(x)
        # print "getpoints: "+ str(remarks)
        if remarks < 0:
            self.badlist.append(chromosome)
        return remarks
        # return x + 10*math.sin(5*x) + 7*math.cos(4*x)

    @Util.calctime
    def selection(self, retain_rate, random_select_rate):
        """
        选择
        先对适应度从大到小排序，选出存活的染色体
        再进行随机选择，选出适应度虽然小，但是幸存下来的个体
        """
        # 对适应度从大到小进行排序
        graded = [(self.fitness(chromosome, self.softorderlist), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)]
        # 选出适应性强的染色体
        retain_length = int(len(graded) * retain_rate)
        parents = graded[:retain_length]
        # 选出适应性不强，但是幸存的染色体
        for chromosome in graded[retain_length:]:
            if random.random() < random_select_rate:
                parents.append(chromosome)
        return parents

    def crossover(self, parents):
        """
        染色体的交叉、繁殖，生成新一代的种群
        """
        # 新出生的孩子，最终会被加入存活下来的父母之中，形成新一代的种群。
        children = []
        # 需要繁殖的孩子的量
        target_count = len(self.population) - len(parents)
        # 开始根据需要的量进行繁殖
        while len(children) < target_count:
            male = random.randint(0, len(parents) - 1)
            female = random.randint(0, len(parents) - 1)
            if male != female:
                # 随机选取交叉点
                cross_pos = random.randint(0, self.length)
                # 生成掩码，方便位操作
                mask = 0
                for i in xrange(cross_pos):
                    mask |= (1 << i)
                male = parents[male]
                female = parents[female]
                # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
                child = ((male & mask) | (female & ~mask)) & ((1 << self.length) - 1)
                if child > self.allkindcnt:
                    child = child >> 1
                    print "HIT!"
                children.append(child)
        # 经过繁殖后，孩子和父母的数量与原始种群数量相等，在这里可以更新种群。
        self.population = parents + children

    def mutation(self, rate):
        """
        变异
        对种群中的所有个体，随机改变某个个体中的某个基因
        """
        for i in xrange(len(self.population)):
            if random.random() < rate:
                j = random.randint(0, self.length - 1)
                self.population[i] ^= 1 << j
                if self.population[i] > self.allkindcnt:
                    self.population[i] = self.population[i] >> 1
                    print "Hit mutation"

    def decode(self, chromosome):
        """
        解码染色体，将二进制转化为三维数组
        """
        return generatedata(self.kt_chromosome.An(self.basepopulation[chromosome]))
        # return chromosome * 9.0 / (2**self.length-1)

    def run(self):
        """
        解码染色体，讲二进制转化为10进制数
        :param chromosome:
        :return:
        """
        return 0

    @Util.calctime
    def result(self):
        """
        获得当前代的最优值，这里取的是函数取最大值时x的值。
        """
        graded = [(self.fitness(chromosome, self.softorderlist), chromosome) for chromosome in self.population]
        graded2 = [x[1] for x in sorted(graded, reverse=True)]
        marks = [x[0] for x in sorted(graded, reverse=True)]
        print "highest: " + str(marks[0])
        rest = self.decode(graded2[0])
        self.exportresult(rest)

    def printinfo(self):
        for k in self.population:
            print bin(k)

    def strongjudge(self, tablematrix):
        j_dict = {}
        for i in range(WEEKDAY):
            for j in range(LESSON):
                j_dict.clear()
                for k in range(CLASSN):
                    km = getClassUnit(tablematrix[i][j][k])
                    # same teacher same time different classrroom
                    if j_dict.has_key(km.teacherid):
                        # print "sametime error"
                        # return False
                        return False
                    else:
                        j_dict[km.teacherid] = 0
                    '''
                    # major subject course teacher teaches the fixed class
                    if km.courseid == 1 or km.courseid == 2 or km.courseid == 3:
                        if km.classid != k:
                            print "major subject error"
                            return False

                    # class 3,4 xuanxiuke

                    if j != 3 and j != 4:
                        if km.courseid not in [1,2,3]:
                            print "xuanke error"
                            return False
                            '''
        return True

    def exportresult(self, tablematrix):
        import csv
        import codecs
        if not os.path.isdir("data/" + MACROTAG + "/result/timetable"):
            os.makedirs("data/" + MACROTAG + "/result/timetable")
        with open("data/" + MACROTAG + "/result/timetable/" + 'timetable' + str(
                time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.csv', 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            colname = []
            colname.append(" ")
            for i in xrange(CLASSN):
                colname.append("Class " + str(i + 1))
            spamwriter.writerow(colname)
            for i in xrange(WEEKDAY):
                if i == 0:
                    day = "周一"
                elif i == 1:
                    day = "周二"
                elif i == 2:
                    day = "周三"
                elif i == 3:
                    day = "周四"
                elif i == 4:
                    day = "周五"
                else:
                    day = "周六"

                spamwriter.writerow([day])

                m_courseidct = {}
                for j in xrange(LESSON):
                    lesson = "Lesson " + str(j + 1)
                    row_ = []
                    row_.append(lesson)
                    for k in xrange(CLASSN):
                        ele = getClassUnit(tablematrix[i][j][k])
                        # print coursedict[ele.courseid] + teacherdict[ele.teacherid]
                        mm = 0
                        if m_courseidct.has_key(ele.courseid):
                            m_courseidct[ele.courseid] += 1
                            mm = m_courseidct[ele.courseid]
                        else:
                            m_courseidct[ele.courseid] = 1
                            mm = 1
                        self.tmpk[tablematrix[i][j][k]] = mm
                        strele = coursedict[ele.courseid].encode("utf-8") + str(mm) + "班 " + teacherdict[
                            ele.teacherid].encode("utf-8")
                        # row_.append(tablematrix[i][j][k])
                        row_.append(strele)
                    spamwriter.writerow(row_)


if __name__ == '__main__':
    # 染色体长度为17， 种群数量为300
    '''
    print len(bin(400))
    print bin(400)
    kk = KTN(4)
    print kk.An(1)
    print kk.X([0,1,3,2])

    male = random.randint(0, 9)
    female = random.randint(0, 9)
    child = 0
    if male != female:
        # 随机选取交叉点
        cross_pos = random.randint(0, 9)
        # 生成掩码，方便位操作
        mask = 0
        for i in xrange(cross_pos):
            mask |= (1 << i)
        male = 300
        female = 400
        print bin(male)
        print bin(female)
        print "cross_pos "+str(cross_pos)
        # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
        child = ((male & mask) | (female & ~mask)) & ((1 << 9) - 1)

    print child
    print bin(child)
    print len(bin(math.factorial(WEEKDAY*LESSON*CLASSN)))

    try:
        a = []
        a.append(2)
    except IndexError,e:
        print e.message


'''

    ga = GA(300, [ContinousClass], 20000)
    '''
    for x in xrange(20):
        ga.evolve()
    ga.result()
    '''
    conn.close()
'''
    ga = GA(17, 300)
    ga.printinfo()

    # 200次进化迭代
    for x in xrange(200):
        ga.evolve()
    print ga.result()
'''