from os import path
from alloc_params import *
from alloc_util import *
from multiprocessing import cpu_count

def make_taskset_file_wrapper(args):
    return make_taskset_file(*args)

def make_taskset_file(idx, n, util):
    outputfile = 'taskset_idx=%d_n=%d_util=%f.ts' % (idx, n, util)

    if n == util: # Fix taskgen bug when n == util
        tspath = 'taskgen -s 1 -n %d -u %s.9999999999999 -p %d -q %d -g %d -d logunif > %s' % (n, n-1, min_period, max_period, gran_period, path.join(TASKSET_DIR, outputfile))
    else:
        tspath = 'taskgen -s 1 -n %d -u %f -p %d -q %d -g %d -d logunif > %s' % (n, util, min_period, max_period, gran_period, path.join(TASKSET_DIR, outputfile))

    try:
        proc = subprocess.Popen(tspath, shell=True, stdout=subprocess.PIPE)
        proc.communicate()
    except OSError as (msg):
        raise OSError("Could not create taskset '%s': %s" % (fname, msg))

    if path.getsize(path.join(TASKSET_DIR, outputfile)) == 0: # Check if the file is not empty (due to taskgen errors)
        raise Exception('Taskgen error. Task set file is empty: ' + outputfile)


def main():
    create_dir(TASKSET_DIR)

    work = []
    idx = 1

    for n in n_values:
        for util in util_values:
            for s in xrange(samples):
                work.append((idx, n, util))
                idx += 1

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(make_taskset_file_wrapper, work, len(util_values)*samples/(8*cpu_count())) 

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
