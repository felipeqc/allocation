import numpy

class Overhead:
    """We assume the x-values are added in ascending order"""
    def __init__(self):
        self._xvalues = [0]
        self._yvalues = [0]

    def _add(self, x, y):
        self._xvalues.append(x)
        self._yvalues.append(y)

        if len(self._xvalues) > 1: # Force the sequence to be monotonically increasing
            if self._yvalues[-1] < self._yvalues[-2]:
                self._yvalues[-1] = self._yvalues[-2]

    def __getitem__(self, n):
        return numpy.interp(n, self._xvalues, self._yvalues)

class OverheadSet:
    """Each pair (x,y) is added individually, but we override get() to force 'SCHED' to be equal to 'SCHED' + 'SCHED2'"""
    def __init__(self):
        self._overhead = {}

    def createOverhead(self, name):
        if not self._overhead.has_key(name):
            self._overhead[name] = Overhead()

    def addValue(self, name, x, y):
        self._overhead[name]._add(x, y)

    def get(self, name, n):
        if name == 'SCHED':
            return self._overhead['SCHED'][n] + self._overhead['SCHED2'][n]
        elif name == 'SCHED2':
            raise KeyError('SCHED2')
        else:
            return self._overhead[name][n]

