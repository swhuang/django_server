#encoding=utf-8

import math
import random
import operator
import copy
import DataInit
import sys
import MySQLdb
import time
import Util

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

CLASSN = 14
COURSE = 9
LESSON = 8
WEEKDAY = 5
#GRADE = 3


resourcedata = DataInit.getResourcedata(conn,WEEKDAY*LESSON*CLASSN)
reslist = []
for key in resourcedata:
    reslist.append(key)

coursedict = {}
coursedict[2] = "数学"
coursedict[1] = "语文"
coursedict[3] = "英语"
coursedict[5] = "物理"
coursedict[6] = "化学"
coursedict[10] = "政治"
coursedict[7] = "生物"
coursedict[8] = "历史"
coursedict[9] = "地理"
coursedict[4] = "体育"
coursedict[11] = "信息"
coursedict[12] = "校"
coursedict[13] = "技"
coursedict[14] = "艺术"
coursedict[15] = "班"
coursedict[16] = "社"
coursedict[17] = "加"

teacherdict = DataInit.getTeacherInfo(conn)
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
#
#chromosome int array
#chromosome -> tablematrix
#
#@Util.calctime
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
                    n = n+1
                except IndexError,e:
                    lesson.append(0)
            weekday.append(lesson)
        tablematrix.append(weekday)
    return tablematrix

#
#tablematrix -> chromosome
#
def processdata(tablematrix):
    chromosome = []
    for i in range(WEEKDAY):
        for j in range(LESSON):
            for k in range(CLASSN):
                try:
                    chromosome.append(tablematrix[i][j][k])
                except IndexError,e:
                    chromosome.append(0)
    return chromosome

'''
从1开始
KTN（4）0,1,2,3   4个数字全排列
康托展开
'''
class KTN():
    def __init__(self,N):
        self.maxn = N

    def X(self,list):
        lens = len(list)
        ans = 0
        for i in xrange(lens):
            x = 0
            for j in xrange(i+1,lens):
                if list[j] < list[i]:
                    x += 1
            ans += x * math.factorial(lens-i-1)
        ans += 1

        return ans

    #@Util.calctime
    def An(self,X):
        n = self.maxn
        showed = []
        ans = []
        for i in xrange(n+1):
            showed.append(False)
        for i in xrange(n):
            ans.append(0)

        X -= 1
        for i in xrange(n):
            numOfMin = X / math.factorial(n-1-i)
            X = X % math.factorial(n - 1 - i)
            j = 0
            k = 0
            while j<=numOfMin:
                if showed[k] == False:
                    j += 1
                k += 1
            k -= 1
            ans[i] = k;
            showed[ans[i]] = True
        for i in xrange(n):
            ans[i] += 1
        return ans
"""
软约束函数列表
"""
####################
def ContinousClass(tablematrix,ii=WEEKDAY,jj=LESSON,kk=CLASSN):
    marks = 0
    for i in xrange(ii):
        for k in xrange(kk):
            cls_dict = {}
            for j in xrange(jj):
                if j > 1:
                    if getClassUnit(tablematrix[i][j][k]).courseid == getClassUnit(tablematrix[i][j-1][k]).courseid:
                        marks += 1
    return marks

####################


class GA():
    def __init__(self, count, softorderlist):
        # 康托展开
        # 将课程全排列映射成数字作为染色体
        self.kt_chromosome = KTN(WEEKDAY*LESSON*CLASSN)
        # 染色体长度
        self.length = len(bin(math.factorial(WEEKDAY*LESSON*CLASSN)))-2#length
        # 种群中的染色体数量
        self.count = count

        self.allkindcnt = math.factorial(WEEKDAY*LESSON*CLASSN)
        #软约束列表
        self.softorderlist = softorderlist

        self.evolvecnt = 0

        self.allkindlist = []

        # 随机生成初始种群
        self.population = self.gen_population(self.length, count)

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
        print "evolving times: "+ str(self.evolvecnt)

    def gen_chromosome(self, length):
        """
        随机生成长度为length的染色体，每个基因的取值是0或1
        这里用一个bit表示一个基因
        """
#        print self.length
        chromosome = 0
        for i in xrange(length):
            chromosome |= (1 << i) * random.randint(0, 1)
        #=====================================
        '''
        N = len(resourcedata)
        resourcedata_cp = copy.copy(self.allkindlist)

        chromosome_ = []
        for i in range(N):
            try:
                index = random.randint(0,len(resourcedata_cp)-1)
                chromosome_.append(resourcedata_cp[index])
            except IndexError,e:
                print e.message
                print index
            try:
                #resourcedata_cp.remove(index)
                del resourcedata_cp[index]
            except ValueError,e:
                print e.message
                print index
        #print "getcurrent chromosome: "+ str(chromosome_)
        '''

        index = random.randint(1, self.allkindcnt)
        if index in self.allkindlist:
            self.gen_chromosome(length)
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
            #tmpk = self.kt_chromosome.X(chromosome_)
            #print "getcurrent chromosome: " + str(elem)
            return index

    def gen_population(self, length, count):
        """
        获取初始种群（一个含有count个长度为length的染色体的列表）
        对初始种群进行筛选以免过早陷入局部最优解
        """

        population = []
        '''
        for i in xrange(count):
            c_a = self.gen_chromosome(length)
            c_d = generatedata(c_a)
            nTolerance = 0
            while self.strongjudge(c_d) == False:
                nTolerance += 1
                if nTolerance == 200:
                    print "Generate population fail"
                    return False
                c_a = self.gen_chromosome(length)
                c_d = generatedata(c_a)
            population.append(c_a)
        '''
        for i in xrange(count):
            population.append(self.gen_chromosome(length))
            print "get population: "+ str(i)
        return population

    def chromosome2data(self,chromosome):

        pass

    def fitness(self, chromosome, rule = []):
        """
        计算适应度，将染色体解码为0~9之间数字，代入函数计算
        因为是求最大值，所以数值越大，适应度越高
        """

        x = self.decode(chromosome)

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

        return remarks
        #return x + 10*math.sin(5*x) + 7*math.cos(4*x)

    @Util.calctime
    def selection(self, retain_rate, random_select_rate):
        """
        选择
        先对适应度从大到小排序，选出存活的染色体
        再进行随机选择，选出适应度虽然小，但是幸存下来的个体
        """
        # 对适应度从大到小进行排序
        graded = [(self.fitness(chromosome,self.softorderlist), chromosome) for chromosome in self.population]
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
            male = random.randint(0, len(parents)-1)
            female = random.randint(0, len(parents)-1)
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
                j = random.randint(0, self.length-1)
                self.population[i] ^= 1 << j


    def decode(self, chromosome):
        """
        解码染色体，将二进制转化为三维数组
        """
        return generatedata(self.kt_chromosome.An(chromosome))
        #return chromosome * 9.0 / (2**self.length-1)

    def decode2(self, chromosome):
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
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)]
        rest = self.decode(graded[0])
        self.exportresult(rest)

    def printinfo(self):
        for k in self.population:
            print bin(k)

    def strongjudge(self,tablematrix):
        j_dict = {}
        for i in range(WEEKDAY):
            for j in range(LESSON):
                j_dict.clear()
                for k in range(CLASSN):
                    km = getClassUnit(tablematrix[i][j][k])
                    # same teacher same time different classrroom
                    if j_dict.has_key(km.teacherid):
                        #print "sametime error"
                        #return False
                        return True
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
        with open('egg2.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            colname = []
            colname.append(" ")
            for i in xrange(CLASSN):
                colname.append("Class "+str(i+1))
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
                for j in xrange(LESSON):
                    lesson = "Lesson "+str(j+1)
                    row_ = []
                    row_.append(lesson)
                    for k in xrange(CLASSN):
                        ele = getClassUnit(tablematrix[i][j][k])
                        strele = coursedict[ele.courseid] + " " + teacherdict[ele.teacherid]
                        row_.append(tablematrix[i][j][k])
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
    ga = GA(300,[ContinousClass])
    for x in xrange(200):
        ga.evolve()
    ga.result()
    conn.close()
'''
    ga = GA(17, 300)
    ga.printinfo()

    # 200次进化迭代
    for x in xrange(200):
        ga.evolve()
    print ga.result()
'''