#!/usr/bin/env python2
import pickle
from instance import *
import graphviz as gv

def drawDag(C,G,I,g):
    A = gv.Digraph(format='svg')

    for i in enumerate(G):
        A.node(str(i))
    edges=[(str(y),str(i)) for i,x in enumerate(G) for y in x]
    for edge in edges:
        A.edge(edge[0],edge[1])
    A.render('dag')
    # A.write('graph.dot')
    # A = p.AGraph('graph.dot')

if __name__ == "__main__":
    # test code
    fileName = 'savedData'
    C,G,I,g = pickle.load(open(fileName,'rb'))
    print G
    print
    # print C
    # print I.jobs
    # print g

    drawDag(C, G, I, g)