from math import floor, ceil
from fractions import Fraction, gcd
from alloc_task import *
from decimal import Decimal

# http://www.enrico-franchi.org/2010/09/nice-functional-lcm-in-python.html
def _lcm(numbers):
    return reduce(lambda x, y: (x*y)/gcd(x,y), numbers)

def _gcdm(numbers):
    return reduce(lambda x, y: gcd(x,y), numbers)

class Partition:
    def __init__(self, number):
        self._number = number
        self._tasks = []
        self._nonmigutil = 0.0

    def __str__(self):
        return 'P' + str(self._number) + ':' + str(self.tasks())

    def __repr__(self):
        return self.__str__()

    def number(self):
        return self._number

    def tasks(self):
        """Return a list with all tasks"""
        return self._tasks

    def util(self):
        return self._nonmigutil

    def _addTask(self, t):
        self._nonmigutil += t.util()
        self._tasks.append(t)

    def _removeLastTask(self):
        self._nonmigutil -= self._tasks[-1].util()
        del self._tasks[-1]

    def _swapTask(self, index, otherTask):
        """Swap non-migratory tasks"""
        self._nonmigutil -= self._tasks[index].util()
        self._nonmigutil += otherTask.util()
        temp = self._tasks[index]
        self._tasks[index] = otherTask
        return temp

    def _merge(self, otherPart):
        """Merge partitions that have only normal (non-migratory) tasks"""
        self._nonmigutil += otherPart._nonmigutil
        self._tasks += otherPart._tasks

        # Clear the other partition
        otherPart._nonmigutil = 0.0
        otherPart._tasks = []

    def _qpa(self):
        """Return if the task set is schedulable"""
        if not self.tasks():
            return True
        else:
            if self.util() > 1.0:
                return False

            L = self._L()
            min_d = self._minDeadline()
            # QPA
            t = self._lastDeadline(L)
            h = self._h(t)
            while round(t,12) >= round(min_d,12):
                if round(h,12) > round(t,12):
                    return False
                elif round(h,12) < round(t,12):
                    t = h
                else:
                    t = self._lastDeadline(t)
                h = self._h(t)
            return True

    def _minDeadline(self):
        return min(self.tasks(), key = lambda t : t.deadline()).deadline()

    def _hyperperiod(self):
        return _lcm([t.period() for t in self.tasks()])

    def _L(self):
        L = self._Lb()
        if self.util() < 1.0:
            L = min(L, self._LaStar())
        return L

    def _La(self):
        maxdeadline = max(self.tasks(), key = lambda t : t.deadline()).deadline()
        
        s = 0.0
        for t in self.tasks():
            s += (t.period() - t.deadline())*t.util()
        s /= 1.0 - self.util()

        return max(maxdeadline, s)

    def _LaStar(self):
        maxdt = max(t.deadline() - t.period() for t in self.tasks())

        s = 0.0
        for t in self.tasks():
            s += (t.period() - t.deadline())*t.util()
        s /= 1.0 - self.util()

        return max(maxdt, s)

    def _Lb(self):
        s_old = sum([t.wcet() for t in self.tasks()])
        s = sum([ceil(round(s_old/t.period(), 12))*t.wcet() for t in self.tasks()])
        while s != s_old:
            s_old = s
            s = sum([ceil(round(s_old/t.period(), 12))*t.wcet() for t in self.tasks()])
        return s

    def _h(self, t):
        s = 0.0
        for task in self.tasks():
            frac = (t + task.period() - task.deadline())/task.period()
            s += max(floor(round(frac, 12)),0.0) * task.wcet() # Round frac to 12 decimal places to prevent floor problems (like 1.9999999999999998)
        return s

    def _h_oth(self, t, thisTask):
        s = 0.0
        for task in self.tasks():
            if task != thisTask:
                frac = (t + task.period() - task.deadline())/task.period()
                s += max(floor(round(frac, 12)),0.0) * task.wcet() # Round frac to 12 decimal places to prevent floor problems (like 1.9999999999999998)
        return s

    def _lastDeadline(self, t):
        dtmax = 0
        for task in self.tasks():
            if task.deadline() < t:
                dj = floor(round((t - task.deadline())/task.period(),12))*task.period() + task.deadline()
                if dj == t:
                    dj -= task.period()
                if dj > dtmax:
                    dtmax = dj
        return dtmax
