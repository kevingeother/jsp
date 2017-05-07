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
    if len(machineJob[-1]) > 0:
        return str(machineJob)
    else:
        return str(machineJob[:-1])

def drawDag(G, S, I, ts, s):
    A = gv.Digraph(format='png')
    machines = list(set([x[2] for x in S]))
    machineJobs = [[x for x in S if x[2] == machineId] for machineId in machines]
    file_resource = [[res for res in I[s[i][0]][1]] for i in xrange(len(s))]
    edges = []
    for i in xrange(len(s)):
        for x in [k for k in range(i) for res in file_resource[i] if res in file_resource[k]]:
            edges.append((getStr(S[s[x][0]]), getStr(S[s[i][0]])))
    for i in machines:
        machineJobs[i].sort(key=lambda tup: tup[1])
        edges.extend([(getStr(machineJobs[i][j]), getStr(machineJobs[i][j+1])) for j in range(len(machineJobs[i])-1)])
        edges.append((getStr(machineJobs[i][-1]), getStr(-1, ts)))

    for edge in edges:
        A.edge(edge[0],edge[1])
    A.render('dag')
    if doOpen:
        os.system('xdg-open dag.png')

if __name__ == "__main__":
    # test code
    G, S, I, ts, s = pickle.load(open('savedData','rb'))
    drawDag(G, S, I, ts, s)