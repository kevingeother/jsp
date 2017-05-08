#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from random import randint, random, seed, shuffle, choice
import plotter
import pickle
from instance import *
from sys import argv

DEBUG=False
DEBUG=False
# DEFAULT PARAMETERS
SEED = 0
# Population size
PS = 1000
# no of iterations/Generations
IT = 50
# Crossover probability
CP = 1.0
# Mutation probability
MP = 0.05

def debug(object):
    if DEBUG:
        print(object)

def LoadInstance(fname):
    """Load instance file."""
    f = open(fname, 'r')
    I = []
    l = f.readline()
    l = l.split()
    machineCapability = [float(k) for k in l]
    for l in f:
        l = l.split()
        # Change to l[0] and count to 1, to make it into jobs and i[-1] to append
        # duration and resource requirement is appended to the array
        dur = float(l[0])
        res = l[1:]
        I.append((dur, res))
    debug(I)
    return Instance(I, machineCapability)

def ComputeDAG(s, I):
    """Compute the DAG representing a solution from a chromosome
    (topological ordering of the DAG)."""
    G = []
    for t in s: 
        G.append([])
    G.append([])
    tasks_resource = [[-1 for j in xrange(I.n)] for m in xrange(I.m)]
    file_resource = [[res for res in I[s[i][0]][1]] for i in xrange(len(s))]
    for i in xrange(len(s)):
        jobId = s[i][0]
        machineId = s[i][1]
        file_resource[i] = [res for res in I[jobId][1]]
        G[-1].append(i)
        # Wait for the last task from other jobs using the same resource
        G[i].extend([tasks_resource[machineId][j2] for j2 in xrange(I.n) if j2 != jobId and tasks_resource[machineId][j2] != -1])
        tasks_resource[machineId][jobId] = i
        G[i].extend([k for k in range(i) for res in file_resource[i] if res in file_resource[k]])
        # Remove redundancy
        G[i] = list(set(G[i]))
    return G

def ComputeStartTimes(s, I, isFinal=False):
    """This computes the start time of each task encoded in a chromosome of
    the genetic algorithm. The last element of the output list is the
    timespan."""
    G= ComputeDAG(s, I)
    C = [0 for t in G]
    for i in xrange(len(G)):
        if len(G[i]) == 0: C[i] = 0
        else: C[i] = max(C[k] + I.getDuration(s[k]) for k in G[i])
    if isFinal:
        return C,G
    return C

def decimal(floatVal):
    return float("{0:.2f}".format(floatVal))

def FormatSolution(s, C, I):
    file_resource = [[res for res in I[s[i][0]][1]] for i in xrange(len(s))]
    S = [0 for j in xrange(I.n)]
    for i in xrange(len(s)):
        j = s[i][0]
        S[j] = (j, decimal(C[i]), s[i][1], decimal(I.getDuration(s[i])), file_resource[i])
    return S

def Genetic(I, ps = PS, pc = CP, pm = MP, mit = IT):
    # Get ps variations of job id * taks no
    def InitPopulation(ps, I):
        """Generate initial population from random shuffles of the tasks."""
        gene = [j for j in xrange(I.n)]
        machines = [choice(range(I.m)) for j in xrange(I.n)]
        population = []
        # Population is a list of individuals
        # individuals is of the form [ (jobid, machineId)]
        for i in xrange(ps):
            shuffle(gene)
            machines = [choice(range(I.m)) for j in xrange(I.n)]
            population.append([(gene[j], machines[j]) for j in xrange(I.n)])
        return population

    def Crossover(p1, p2, I):
        """Crossover operation for the GA. Generalized Order Crossover (GOX)."""
        def Index(p1, I):
            # Convertd jobs to (jobs, tasks)
            return [i+(0,) for i in p1]
        idx_p1 = Index(p1, I)
        idx_p2 = Index(p2, I)
        # total number of tasks
        noOfTasks = len(idx_p1) 
        i = randint(1, noOfTasks)
        j = randint(0, noOfTasks-1)
        k = randint(0, noOfTasks)
        implant = idx_p1[j:min(j+i,noOfTasks)] + idx_p1[:i - min(j+i,noOfTasks) + j]
        lft_child = idx_p2[:k]
        rgt_child = idx_p2[k:]
        for jt in implant:
            if jt in lft_child: lft_child.remove(jt)
            if jt in rgt_child: rgt_child.remove(jt)

        child = [ (job,machine) for (job,machine, task) in lft_child + implant + rgt_child ]
        return child
    def Mutation(p):
        """Mutation operation for the GA. Swaps to genes of the chromosome."""
        nt = len(p)
        i = randint(0, nt - 1)
        j = randint(0, nt - 1)
        m = [job for job in p]
        m[i], m[j] = m[j], m[i]
        return m

    # Start times, for the dag is found and the max (end node) is found. For each chromosome
    pop = [(ComputeStartTimes(g, I)[-1], g) for g in InitPopulation(ps, I)]
    for it in xrange(1, mit+1):
        # Random ordering of the population
        shuffle(pop)
        hpop = len(pop) / 2
        for i in xrange(hpop):
            if random() < pc:
                # Create two new elements
                ch1 = Crossover(pop[i][1], pop[hpop + i][1], I)
                ch2 = Crossover(pop[hpop + i][1], pop[i][1], I)
                if random() < pm:
                    ch1 = Mutation(ch1)
                if random() < pm:
                    ch2 = Mutation(ch2)
                pop.append((ComputeStartTimes(ch1, I)[-1], ch1))
                pop.append((ComputeStartTimes(ch2, I)[-1], ch2))
        # Sort individuals in increasing timespan order and
        # select only the best ones for the next iteration
        pop.sort()
        pop = pop[:ps]
    return pop[0]

def usage():
    print 'Usage: %s [OPTIONS] <instance-file>' % argv[0]
    print 'Options:'
    print '  -s <seed>           Random seed. Default: %d' % SEED
    print '  -p <population>     Population size. Default: %d' % PS
    print '  -i <iterations>     Iterations. Default: %d' % IT
    print '  -c <crossover-prob> Crossover probability. Default: %f' % CP
    print '  -m <mutation-prob>  Mutation probability. Default: %f' % MP

if len(argv) < 2:
    usage()
    exit(1)

i = 1
while i < len(argv) - 1:
    if argv[i] == '-s':
        SEED = int(argv[i+1])
    elif argv[i] == '-p':
        PS = int(argv[i+1])
    elif argv[i] == '-d':
        DEBUG = bool(argv[i+1])
    elif argv[i] == '-i':
        IT = int(argv[i+1])
    elif argv[i] == '-c':
        CP = float(argv[i+1])
    elif argv[i] == '-m':
        MP = float(argv[i+1])
    elif argv[i] == '-h':
        usage()
        exit(0)
    else:
        print 'Unknown option: %s' % argv[i]
        usage()
        exit(1)
    i = i + 2

seed(SEED)
# I is the array from the result of loading file
I = LoadInstance(argv[-1])
(ts, g) = Genetic(I, ps=PS, mit=IT, pc=CP, pm=MP)
C,G = ComputeStartTimes(g, I, True)
S = FormatSolution(g, C, I)
pickle.dump((G, S, I, ts, g),open('savedData', 'wb'))
plotter.drawDag(G, S, I, ts, g)
# print ts, S
