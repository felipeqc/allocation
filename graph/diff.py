# encoding: utf8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../total.txt')
del df['wss']
del df['taskset_file']
del df['n']

df2 = df[df['schedulable'] == True]

idxgroups = df2.groupby('idx')
for (idx, x) in idxgroups:
    cd = x[x['sched'] == 'CD']
    hime = x[x['sched'] != 'CD']

    if len(cd) == 0 and len(hime) > 0:
        print idx
        #for x in hime:
        #    print "Schedulable by",x[0]
