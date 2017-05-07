jsp-ga
======

Job-shop Scheduling Problem using Genetic Algorithms.

Usage
-----

The program usage is straightforward:

```
$ python jsp.py jsp-instance.txt
```

The program will output the timespan of the best solution and the start time
of each task (presented as a list of lists of integers) and its corresponding instance.

jsp-ga has some options that can be configured to tune the performance/speed
of the genetic algorithm.

```
$ python jsp.py
Usage: jsp.py [OPTIONS] <instance-file>
Options:
  -s <seed>           Random seed. Default: 0
  -p <population>     Population size. Default: 1000
  -i <iterations>     Iterations. Default: 50
  -c <crossover-prob> Crossover probability. Default: 1.000000
  -m <mutation-prob>  Mutation probability. Default: 0.100000
```
