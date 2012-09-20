from os import getenv, path, listdir, remove, makedirs
from scipy.stats import scoreatpercentile
import xml.dom.minidom as minidom
import re

ALLOCATION_DIR = getenv('ALLOCATION', '/home/felipe/Desktop/qpa')
TASKSET_DIR = path.join(ALLOCATION_DIR, 'tasksets')
DATA_DIR = path.join(ALLOCATION_DIR, 'data')

def decode(name):
    params = {}
    parts = re.split('_(?!RESCHED|LATENCY|TIMER)', name) # Fix for event names with underscore
    for p in parts:
        kv = p.split('=')
        k = kv[0]
        v = kv[1] if len(kv) > 1 else None
        params[k] = v
    return params

def get_config(fname):
    return path.splitext(path.basename(fname))[0]  


def create_dir(dirpath):
    try:
        if not path.exists(dirpath):
            makedirs(dirpath)
    except OSError as (msg):
        raise OSError ("Could not create overhead directory: %s", (msg))

def cycles_to_ms(c):
    return c / (CLOCK * 1000.0)
