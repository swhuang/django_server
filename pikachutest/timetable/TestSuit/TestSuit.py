#encoding=utf-8
import random

"""
A；物理
B；化学
C；生物
D；历史
E；政治
F；地理
"""
STATIC = []
STATIC.append('A')
STATIC.append('B')
STATIC.append('C')
STATIC.append('D')
STATIC.append('E')
STATIC.append('F')

if __name__ == "__main__":
    classdict = {}
    classdict['A'] = 0
    classdict['B'] = 0
    classdict['C'] = 0
    classdict['D'] = 0
    classdict['E'] = 0
    classdict['F'] = 0
    for i in xrange(200):
        g = random.sample(range(0,6),3)
        for k in range(len(g)):
            classdict[STATIC[g[k]]] += 1

    print classdict
