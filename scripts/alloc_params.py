from os import path
import pickle
import alloc_overhead
from alloc_util import *
from cachetopology import *

timeout = 60 # Timeout when running schedulability tests (in seconds)

# HIME scheduler overheads
ovfile = open(path.join(DATA_DIR, 'HIME.ovset'), 'r')
himeoverhead = pickle.load(ovfile)
ovfile.close()

# Preemption overheads
ovfile = open(path.join(DATA_DIR, 'PREEMPTION.ovset'), 'r')
preemption = pickle.load(ovfile)
ovfile.close()

# Migration overheads
ovfile = open(path.join(DATA_DIR, 'L3.ovset'), 'r')
l3 = pickle.load(ovfile)
ovfile.close()

# Topology
topo = CacheTopology(path.join(DATA_DIR, 'ufba.topo'))
cpus = topo.cpus()

cpus = 16
#util_values = [2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9] # 70% to 100% (2.5% steps)
util_values = [11.2, 11.6, 12.0, 12.4, 12.8, 13.2, 13.6, 14.0, 14.4, 14.8, 15.2, 15.6] # 70% to 100% (2.5% steps)
#wss_values = preemption.keys()
wss_values = []
#n_values = [6,7,8,10]
n_values = [20,24,28,40]
samples = 1000

min_period = 1
max_period = 100
gran_period = 1
