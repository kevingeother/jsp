#!/usr/bin/env python2
import pickle
from instance import *
import graphviz as gv
import os
# doOpen = False
doOpen = True

def getStr(machineJob, ts=0):
    if machineJob == -1:
        return "End '" + str(ts) + "'"
    #return str(machineJob[0])
    if len(machineJob[-1]) > 0:
        return str(machineJob)
    else:
        return str(machineJob[:-1])

def decimal(floatVal):
    return float("{0:.2f}".format(floatVal))

def drawDag(G, S, I, ts, s):
    f = open('output', 'wb')
    f.write("JOB ID, MACHINE\n")
    for l in s:
        f.write(str(l)+'\n')
    A = gv.Digraph(format='svg')
    machines = list(set([x[2] for x in S]))
    file_resource = [[res for res in I[s[i][0]][1]] for i in xrange(len(s))]
    edges = []
    machineJobs = {}
    for i in xrange(len(s)):
        for x in [k for k in range(i) for res in file_resource[i] if res in file_resource[k]]:
            edges.append((getStr(S[s[x][0]]), getStr(S[s[i][0]])))
    for i in machines:
        machineJobs[i] = [x for x in S if x[2] == i]
        machineJobs[i].sort(key=lambda tup: tup[1])
        edges.extend([(getStr(machineJobs[i][j]), getStr(machineJobs[i][j+1])) for j in range(len(machineJobs[i])-1)])
        edges.append((getStr(machineJobs[i][-1]), getStr(-1, ts)))
    edges = list(set(edges))
    edges = [edge for edge in edges if edge[0] != edge[1]]

    for edge in edges:
        A.edge(edge[0],edge[1])
    A.render('dag')
    noFileS=[x[:-1] for x in S]
    noFileS.sort(key=lambda tup: tup[1] + tup[3])
    noFileS=[(s[0], decimal(s[1]+s[3]), s[1]) for s in noFileS]
    f.write("\n\nJOBID, FINISHING TIME, STARTING TIMES\n")
    for l in noFileS:
        f.write(str(l) + '\n')
    f.close()
    if doOpen:
        os.system('xdg-open dag.svg')

if __name__ == "__main__":
    # test code
    G, S, I, ts, s = pickle.load(open('savedData','rb'))
    drawDag(G, S, I, ts, s)
