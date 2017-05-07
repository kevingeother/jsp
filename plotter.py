#!/usr/bin/env python2
import pickle
from instance import *
import graphviz as gv

def getStr(i,C,G,I,g):
    machine = [x[1] for x in g if x[0]==i ]
    return str(i) + ', ' + str('{0:.2f}'.format(C[i])) + (', '+str(machine[0]) if len(machine)>0 else '')

def drawDag(C,G,I,g):
    A = gv.Digraph(format='png')
    edges=[(getStr(y,C,G,I,g),getStr(i,C,G,I,g)) for i,x in enumerate(G) for y in x]
    x = [e[0] for e in edges]
    x.sort()
    x = list(set(x))
    print x
    for edge in edges:
        A.edge(edge[0],edge[1])
    A.render('dag')

if __name__ == "__main__":
    # test code
    C,G,I,g = pickle.load(open('savedData','rb'))
    print g
    print
    g.sort(key=lambda tup: tup[0])
    print g
    drawDag(C, G, I, g)