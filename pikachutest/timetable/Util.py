import time
import math
import copy

def calctime(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        rt = fn(*args, **kwargs)
        end = time.time()
        print fn.__name__ + " cost time: "+str(end-start)
        return rt
    return wrapper

def sort_by_value(d):
    #m = copy.deepcopy(d)

    items=d.items()

    backitems=[[len(v[1]),v[0],v[1]] for v in items]

    backitems.sort()

    backitems.reverse()

    return backitems

def sort_list(l):
    m = copy.deepcopy(l)


@calctime
def tt(n):
    n = 10
    for i in range(560):
        n += 1
        k = math.factorial(abs(560-n))
        #print "hhh"+str(n)




if __name__ == '__main__':
    tt(10)