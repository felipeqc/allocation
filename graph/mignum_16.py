# encoding: utf8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../total.txt')
del df['idx']
del df['wss']
del df['taskset_file']
del df['n']

schedgroups = df.groupby('sched')
for (sched, x) in schedgroups: # for each group n->x
    for (bp_o, y) in x.groupby(['bp','o']):
        print "\t", sched, bp_o
        for (u, z) in y.groupby('util'):
            print "%.2f" % (float(u)/16.0),
            schedsets = z[z['schedulable'] == 1]
            print "\t%d/%d" % (len(schedsets), len(z)),
            print "\t%f" % (z['slicenum'].mean()),
            for s in xrange(16):
                print "\t%d" % (len(schedsets[schedsets['mignum'] == s])),
            print
        print "\n"
