from math import floor
from alloc_task_wm import *
from alloc_part import *

class CDPartition(Partition):
    def __init__(self, number):
        Partition.__init__(self, number)
        self._slices = []

    def util(self):
        """Return the total utilization of ALL TASKS, INCLUDING MIGRATORY"""
        total = 0.0
        for task in self._slices:
            total += task.util()
        return self._nonmigutil + total

    def density(self):
        """Return the density of ALL TASKS, INCLUDING MIGRATORY"""
        total = 0.0
        for task in self.tasks():
            total += task.density()
        return total

    def normalTasks(self):
        """Return a list with all tasks"""
        return self._tasks

    def slices(self):
        """Return a list with all slices"""
        return self._slices

    def tasks(self):
        """Return a list with all tasks and slices"""
        return self._tasks + self._slices

    def _addSlice(self, s):
        self._slices.append(s)

    def _removeLastSlice(self):
        del self._slices[-1]

    def _lastSlice(self):
        return self._slices[-1]

    def _hasSlices(self):
        return len(self._slices) > 0

    def _schedTest(self):
        """Apply schedulability test. Assumes that only migratory tasks can have restricted deadlines (due to parameter modification)."""
        if not self._hasSlices(): # There are no migratory tasks, so let's check utilization
            return self.util() <= 1.0
        else:
            return self._qpa()

    def _calcExecTime(self, migTask):
        """Return the free execution time for a migratory task in this partition (version without GAP)"""
        # Let's start making U = 0.9999 (which probably causes deadline misses).
        # If we force U = 1, we won't be able to use La.
        if self.util() >= 0.9999:
            self._lastCost = 0.0
            return 0.0
        c_old = (0.9999 - self.util())*migTask.period()
        c = c_old

        # Temporarily add the slice with C = D
        tempSlice = WmSlice(-1, c, c, migTask)
        self._addSlice(tempSlice)

        # Repeat QPA in case of failure
        failure = True
        while failure:
            failure = False

            L = self._L()
            min_d = self._minDeadline()

            t = self._lastDeadline(L)
            h = self._h(t)
            while round(t,12) >= round(min_d,12):
                # We round the checking to 12 decimal places. Otherwise, it could make the algorithm repeat undefinedly, in
                # case new calculated cost is not 100% precise. We do the same when applying floor(). The other comparisons don't
                # need this correction, since they are not so critical.
                if round(h,12) > round(t,12):
                    c = (t - self._h_oth(t, tempSlice)) / floor(round((t + migTask.period() - c_old)/migTask.period(), 12))
                    while c != c_old:
                        c_old = c
                        c = (t - self._h_oth(t, tempSlice)) / floor(round((t + migTask.period() - c_old)/migTask.period(), 12))

                    # Update parameters to fix demand
                    tempSlice._wcet = c
                    tempSlice._deadline = c

                    if c <= 0.0: # Stop if the cost gets zero
                        self._removeLastSlice()
                        self._lastCost = 0.0
                        return 0.0

                    # Let's repeat QPA 
                    failure = True
                    break

                # Go to next point
                t = self._lastDeadline(t)
                h = self._h(t)
        
        #if not (self._qpa() and self._qpa2()):
        #    print self, self.util()
        #assert self._qpa()

        self._removeLastSlice()
        self._lastCost = c
        return c

    def _calcExecTime2(self, migTask):
        """Return the free execution time for a migratory task in this partition (version without GAP)"""
        # Let's start making U = 0.9999 (which probably causes deadline misses).
        # If we force U = 1, we won't be able to use La.
        if self.util() >= 0.9999:
            self._lastCost = 0.0
            return 0.0
        c_old = (0.9999 - self.util())*migTask.period()
        c = c_old

        # Temporarily add the slice with C = D
        tempSlice = WmSlice(-1, c, c, migTask)
        self._addSlice(tempSlice)

        # Repeat QPA in case of failure
        failure = True
        while failure:
            failure = False

            L = self._L()

            t = self._lastDeadline(L)
            h = self._h(t)
            while t >= tempSlice.deadline():
                # We round the checking to 12 decimal places. Otherwise, it could make the algorithm repeat undefinedly, in
                # case new calculated cost is not 100% precise. We do the same when applying floor(). The other comparisons don't
                # need this correction, since they are not so critical.
                if round(h,12) > round(t,12):
                    c = (t - self._h_oth(t, tempSlice)) / floor(round((t + migTask.period() - c_old)/migTask.period(), 12))
                    while c != c_old:
                        c_old = c
                        c = (t - self._h_oth(t, tempSlice)) / floor(round((t + migTask.period() - c_old)/migTask.period(), 12))

                    # Update parameters to fix demand
                    tempSlice._wcet = c
                    tempSlice._deadline = c

                    if c <= 0.0: # Stop if the cost gets zero
                        self._removeLastSlice()
                        self._lastCost = 0.0
                        return 0.0

                    # Let's repeat QPA 
                    failure = True
                    break

                # Go to next point
                t = self._lastDeadline(t)
                h = self._h(t)
        
        #if not (self._qpa() and self._qpa2()):
        #    print self, self.util()
        #assert self._qpa()

        self._removeLastSlice()
        self._lastCost = c
        return c

    def _memoExecTime(self):
        return self._lastCost
