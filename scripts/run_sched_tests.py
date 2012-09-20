from os import path
import multiprocessing
from xml.dom import minidom
import random
from alloc_util import *
from alloc_params import *
import alloc_alg_wm as wm
import alloc_alg_cd as cd
import alloc_alg_hime as hime
import alloc_alg_himemind as himemind
import alloc_alg_himex as himex
import sys
import signal
from task import Task as TaskJamsjr
import int_qpa

def run_taskset_wrapper(args):
    return run_taskset(*args)

def run_taskset(sched, bp, o, taskset_file, wss, results):
    print >> sys.stderr, '*\t',

    tasks = minidom.parse(path.join(TASKSET_DIR, taskset_file))
    schedulable = None
    mignum = 0
    slicenum = 0

    params = decode(get_config(taskset_file))
    idx = params['idx']
    n = params['n']
    util = params['util']

    # Recall that we imported some variables from alloc_params
    # himeoverhead: HIME scheduler overheads
    # preemption: preemption overheads
    # l3: L3 migration overheads

    if sched == 'HIME':
        ts = hime.HimeTaskSet(cpus)

        for task in tasks.getElementsByTagName("task"):
            wcet = float(task.getAttribute("wcet"))
            period = int(task.getAttribute("period"))
            ts.createTask(wcet, period)

        schedulable = ts.allocate(bp, o)  
    elif sched == 'HIMEX':
        ts = himex.HimexTaskSet(cpus)

        for task in tasks.getElementsByTagName("task"):
            wcet = float(task.getAttribute("wcet"))
            period = int(task.getAttribute("period"))
            ts.createTask(wcet, period)

        schedulable = ts.allocate(bp, o)  
    elif sched == 'HIMEMIND':
        ts = himemind.HimeMindTaskSet(cpus)

        for task in tasks.getElementsByTagName("task"):
            wcet = float(task.getAttribute("wcet"))
            period = int(task.getAttribute("period"))
            ts.createTask(wcet, period)

        schedulable = ts.allocate()              
    elif sched == 'EDFWM':
        ts = wm.WmTaskSet(cpus)

        for task in tasks.getElementsByTagName("task"):
            wcet = float(task.getAttribute("wcet"))
            period = int(task.getAttribute("period"))
            ts.createTask(wcet, period)

        schedulable = ts.allocate(bp, o)
        #if schedulable:
            #TaskJamsjr.implicit(False)
            #for part in ts.partitions():
                #l = [TaskJamsjr((0, int(1000000*t.wcet()), int(1000000*t.period()), int(1000000*t.deadline()), 0)) for t in part.tasks()]
                #assert part._schedTest() and int_qpa.QPA(l)
    elif sched == 'CD':
        ts = cd.CDTaskSet(cpus)

        for task in tasks.getElementsByTagName("task"):
            wcet = float(task.getAttribute("wcet"))
            period = int(task.getAttribute("period"))
            ts.createTask(wcet, period)

        """o2 = None
        if o == 'u':
            o2 = 'dd'
        elif o == 'p':
            o2 = 'rdm'"""
        schedulable = ts.allocate()
        #if schedulable:
            #TaskJamsjr.implicit(False)
            #for part in ts.partitions():
                #l = [TaskJamsjr((0, int(1000000*t.wcet()), int(1000000*t.period()), int(1000000*t.deadline()), 0)) for t in part.tasks()]
                #assert part._schedTest() and int_qpa.QPA(l)
    elif sched == 'HIMEOV':

        overhead = himeoverhead
        cpmd = max(preemption[wss], l3[wss])

        ts = HimeTaskSetOv(cpus, overhead, cpmd)

        for task in tasks.getElementsByTagName("task"):
            wcet = float(task.getAttribute("wcet"))
            period = int(task.getAttribute("period"))
            ts.createTask(wcet, period)

        schedulable = ts.allocate(bp, o)

    if schedulable == False:
        schedulable = 0
    else:
        schedulable = 1

        for task in ts.tasks():
            found = False
            for part in ts.partitions():
                for otherTask in part._tasks:
                    if task.number() == otherTask.number():
                        found = True
                        break
            if not found:
                mignum += 1

        totaltasks = sum([len(part.tasks()) for part in ts.partitions()])
        slicenum = totaltasks - len(ts.tasks()) + mignum

    results.put((idx, sched, bp, o, taskset_file, wss, n, util, schedulable, mignum, slicenum))

class TimeoutException(Exception): 
    pass

def timeout(signum, frame):
    raise TimeoutException()

def main2():
    schedulers = [('HIME', 'f', 'u'), ('HIMEMIND', None, None), ('CD', None, None), ('EDFWM', 'f', 'p')]
    """schedulers = ['HIME', 'EDFWM', 'CD']
    binpacking = ['f', 'w']
    order = ['u', 'p']"""

    manager = multiprocessing.Manager()
    results = manager.Queue() # Shared buffer for saving results

    work = []
    for taskset_file in listdir(TASKSET_DIR):
        for sched in schedulers:
            work.append((sched[0], sched[1], sched[2], taskset_file, None, results)) # scheduler without overheads
            for wss in wss_values:
                work.append((sched[0] + 'OV', sched[1], sched[2], taskset_file, wss, results)) # scheduler with overheads

    """work = []
    for taskset_file in listdir(TASKSET_DIR):
        work.append(('CD', None, None, taskset_file, None, results)) # scheduler without overheads
        for wss in wss_values:
            work.append(('CDOV', None, None, taskset_file, wss, results)) # scheduler with overheads
        for bp in binpacking:
            for o in order:
                for sched in schedulers:
                    if sched != 'CD':
                        work.append((sched, bp, o, taskset_file, None, results)) # scheduler without overheads
                        for wss in wss_values:
                            work.append((sched + 'OV', bp, o, taskset_file, wss, results)) # scheduler with overheads"""

    total = len(work)
    for i in xrange(len(work)):
        #print >> sys.stderr, i,'/',total
        print >> sys.stderr, i,'/',total,':', work[i]
        #sys.stdout.flush()
        #signal.signal(signal.SIGALRM, timeout)
        #signal.alarm(10)
        try:
            run_taskset_wrapper(work[i])
        except TimeoutException:
            print 'LATE:', work[i]
        #signal.alarm(0)

    print 'idx,sched,bp,o,taskset_file,wss,n,util,schedulable,mignum,slicenum'
    while not results.empty():
        v = results.get()
        print '%d,%s,%s,%s,%s,%s,%d,%f,%d,%d,%d' % (int(v[0]), v[1], v[2], v[3], v[4], str(v[5]), int(v[6]), float(v[7]), v[8], v[9], v[10])
        
def main():
    schedulers = [('HIME', 'f', 'u'), ('HIMEMIND', None, None), ('CD', None, None), ('EDFWM', 'f', 'p')]
    """schedulers = ['HIME', 'EDFWM', 'CD']
    binpacking = ['f', 'w']
    order = ['u', 'p']"""

    manager = multiprocessing.Manager()
    results = manager.Queue() # Shared buffer for saving results

    """work = []
    for taskset_file in listdir(TASKSET_DIR):
        work.append(('CD', None, None, taskset_file, None, results)) # scheduler without overheads
        for wss in wss_values:
            work.append(('CDOV', None, None, taskset_file, wss, results)) # scheduler with overheads
        for bp in binpacking:
            for o in order:
                for sched in schedulers:
                    if sched != 'CD':
                        work.append((sched, bp, o, taskset_file, None, results)) # scheduler without overheads
                        for wss in wss_values:
                            work.append((sched + 'OV', bp, o, taskset_file, wss, results)) # scheduler with overheads"""

    work = []
    for taskset_file in listdir(TASKSET_DIR):
        for sched in schedulers:
            work.append((sched[0], sched[1], sched[2], taskset_file, None, results)) # scheduler without overheads
            for wss in wss_values:
                work.append((sched[0] + 'OV', sched[1], sched[2], taskset_file, wss, results)) # scheduler with overheads

    random.seed()
    random.shuffle(work)

    print >> sys.stderr,"Running",len(work),"task sets."
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(run_taskset_wrapper, work, len(work)/(30*multiprocessing.cpu_count()))

    pool.close()
    pool.join()

    print 'idx,sched,bp,o,taskset_file,wss,n,util,schedulable,mignum,slicenum'
    while not results.empty():
        v = results.get()
        print '%d,%s,%s,%s,%s,%s,%d,%f,%d,%d,%d' % (int(v[0]), v[1], v[2], v[3], v[4], str(v[5]), int(v[6]), float(v[7]), v[8], v[9], v[10])

if __name__ == '__main__':
    main()
