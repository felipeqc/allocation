import math
from alloc_task_wm import *
from alloc_part import *

class WmPartition(Partition):
    def __init__(self, number):
        Partition.__init__(self, number)
        self._slices = []

    def util(self):
        """Return the total utilization for ALL TASKS, INCLUDING MIGRATORY"""
        total = 0.0
        for task in self._slices:
            total += task.util()
        return self._nonmigutil + total

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

    def _calcExecTime(self, migTask, dPrime):
        """Return the free execution time for a migratory task in this partition"""
        #print "ae", self
        # Let's start making U = 0.9999 (which probably causes deadline misses).
        # If we force U = 1, we won't be able to use La.
        if self.util() >= 0.9999:
            self._lastCost = 0.0
            return 0.0
        cPrime = (0.9999 - self.util())*migTask.period()

        # Temporarily add the slice
        tempSlice = WmSlice(-1, cPrime, dPrime, migTask)
        self._addSlice(tempSlice)

        L = self._L()
        min_d = self._minDeadline()

        #print "L", L
        #print self
        #print "Calculating cost. dPrime", dPrime

        # QPA
        t = self._lastDeadline(L)
        h = self._h(t)
        #print t
        while round(t,12) >= round(min_d,12): # We are checking demand only for the migratory task
            # We round the checking to 12 decimal places. Otherwise, it could make the algorithm repeat undefinedly, in
            # case new calculated cost is not 100% precise. We do the same when applying floor(). The other comparisons don't
            # need this correction, since they are not so critical.
            if round(h,12) > round(t,12):
                #print "HIGH. t %.15f" % t, "h(t) %.15f" % h, ". C was", cPrime
                cPrime = (t - self._h_oth(t, tempSlice)) / floor(round((t + migTask.period() - dPrime)/migTask.period(), 12))
                #print "New C is", cPrime
                tempSlice._wcet = cPrime # Update slice cost to fix demand

                if cPrime <= 0.0: # Stop if the cost gets negative
                    self._removeLastSlice()
                    self._lastCost = 0.0
                    return 0.0

            #print "OK. t", t, "h(t)",h, "new t",
            t = self._lastDeadline(t)
            #print t
            h = self._h(t)
        #print "OK. t", t, "h(t)",h

        #print self
        #print "Final cost", cPrime
        #if not self._qpa():
        #    print self.tasks()
        #assert self._qpa()

        self._removeLastSlice()
        self._lastCost = cPrime
        return cPrime

    def _memoExecTime(self):
        return self._lastCost
