# encoding: utf8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../total.txt')
del df['idx']
del df['wss']
del df['taskset_file']
del df['mignum']
df['util'] = df['util'].apply(lambda x : float(x))

df2 = df.groupby(['sched','bp', 'o', 'n', 'util']).mean().reset_index()

#markers = {('f', 'u'): 's', ('f', 'p'): 'v', ('w', 'u'): '+', ('w', 'p'): 'x'}
markers = {('f', 'u'): 's', ('f', 'p'): 's', ('w', 'u'): 'x', ('w', 'p'): 's'}
linestyles = {('f', 'u'): '-', ('f', 'p'): '--', ('w', 'u'): '--', ('w', 'p'): '-'}
labels_hime = {('f', 'u'): 'HIME FF-DU', ('f', 'p'): 'HIME FF-DP', ('w', 'u'): 'HIME WF-DU', ('w', 'p'): 'HIME WF-DP'}
labels_wm = {('f', 'u'): 'EDF-WM FF-DU', ('f', 'p'): 'EDF-WM FF-DP', ('w', 'u'): 'EDF-WM WF-DU', ('w', 'p'): 'EDF-WM WF-DP'}
labels_overhead = {'no_ov': ' (original)', 'ov': ' (com overheads)'}

colors = {('f', 'u'): 'red', ('f', 'p'): 'blue', ('w', 'u'): 'black', ('w', 'p'): 'green'}

ngroups = df2.groupby('n')
for (n, x) in ngroups: # for each group n->x
    plt.clf()
    for (bp_o, y) in x.groupby(['bp','o']): # for each group bp_o->y
        if bp_o == ('None', 'None'):
            cd = x[x['sched'] == 'CD']
            plt.plot(cd['util'].tolist(), cd['schedulable'].tolist(), color='pink', label = 'C=D DDminD', linestyle='-', antialiased=True)
            himemind = y[y['sched'] == 'HIMEMIND']
            if len(himemind) > 0:
                plt.plot(himemind['util'].tolist(), himemind['schedulable'].tolist(), color='orange', label = 'HIME DDminD', linestyle='-', marker='s', antialiased=True, alpha=0.6)
        else:
            hime = y[y['sched'] == 'HIME']
            if len(hime) > 0:
                plt.plot(hime['util'].tolist(), hime['schedulable'].tolist(), color=colors[bp_o], label = labels_hime[bp_o], linestyle='-', marker=markers[bp_o], antialiased=True, alpha=0.6)
            wm = y[y['sched'] == 'EDFWM']
            if len(wm) > 0:
                plt.plot(wm['util'].tolist(), wm['schedulable'].tolist(), color=colors[bp_o], label = labels_wm[bp_o], linestyle='--', marker='s', antialiased=True, alpha=0.6)
    plt.ylabel(u'Taxa de Escalonabilidade')
    plt.xlabel(u'Utilização do Sistema')
    plt.legend(loc=0)
    #plt.xlim(3.4, 3.9)
    plt.xlim(11.2, 15.6)
    plt.ylim(0, 1.02)
    plt.xticks([11.2, 11.6, 12.0, 12.4, 12.8, 13.2, 13.6, 14.0, 14.4, 14.8, 15.2, 15.6], ['70%', '72.5%', '75%', '77.5%', '80%', '82.5%', '85%', '87.5%', '90%', '92.5%', '95%', '97.5%'])
    #plt.xticks([3.4, 3.5, 3.6, 3.7, 3.8, 3.9], ['85%', '87.5%', '90%', '92.5%', '95%', '97.5%'])

    fig = plt.gcf()
    fig.set_size_inches(9, 9)
    plt.savefig('n%d.eps' % n, format="eps", dpi=100)
"""a = df2[df2['bp'] == 'w']
b = a[a['o'] == 'p']
c = b[b['wss'] == 10240]
d = c[c['n'] == 7]
plt.plot(d['util'], d['schedulable'], 'b')
a = df2[df2['bp'] == 'w']
b = a[a['o'] == 'p']
c = b[b['wss'] == 'None']
d = c[c['n'] == 7]
plt.plot(d['util'], d['schedulable'], 'r')
plt.show()"""
