#!/usr/bin/env python2
import pickle
from instance import *
import graphviz as gv

def getStr(i,S, ts):
    # Item is jobid, startTime, machine
    if(i<len(S)):
        return str(S[i])
    return 'End'

def drawDag(G, S, ts):
    A = gv.Digraph(format='png')
    edges=[(getStr(y, S, ts),getStr(i, S, ts)) for i,x in enumerate(G) for y in x]
    x = [e[0] for e in edges]
    x.sort()
    x = list(set(x))
    print x
    for edge in edges:
        A.edge(edge[0],edge[1])
    A.render('dag')

if __name__ == "__main__":
    # test code
    G, S, ts = pickle.load(open('savedData','rb'))
    print S
    drawDag(G, S, ts)