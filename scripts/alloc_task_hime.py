class HimeSlice:
    def __init__(self, snum, c, task):
        """Initialize a slice with its number, its budget and the task which it represents"""
        self._slicenumber = snum
        self._wcet = c
        self._task = task

    def __str__(self):
        """String representation"""
        return '(Slice' + str(self._task.number()) + ':' + str(self._slicenumber) + ',C=' + str(self._wcet) + ',T=' + str(self.period()) + ')'

    def __repr__(self):
        """Python representation"""
        return self.__str__()

    def slicenumber(self):
        """Return the number of this slice"""
        return self._slicenumber

    def updateSliceNumber(self, snum):
        self._slicenumber = snum

    def task(self):
        """Return the task which this slice is associated to"""
        return self._task

    def wcet(self):
        """Return the current budget of the slice"""
        return self._wcet

    def period(self):
        """Return the period of the slice"""
        return self._task._period

    def util(self):
        """Return the utilization of the slice"""
        return self._wcet/self._task._period

class HimeSliceOv(HimeSlice):
    def __init__(self, snum, c, task):
        HimeSlice.__init__(self, snum, c, task)
        self._curwcet = self._wcet

    def __str__(self):
        return '(Slice' + str(self._task.number()) + ':' + str(self._slicenumber) + ',C=' + str(self._wcet) + ',C\'=' + str(self._curwcet) + ',T=' + str(self.period()) + ',T\'=' + str(self.currentPeriod()) + ')'

    def __repr__(self):
        return self.__str__()

    def currentWcet(self):
        """Return the current budget of the slice (with overheads)"""
        return self._curwcet

    def currentPeriod(self):
        """Return the current period of the slice (with overheads)"""
        return self._task._curperiod

    def currentUtil(self):
        """Return the current utilization of the slice (with overheads)"""
        return self._curwcet/self._task._curperiod

    def updateWcet(self, c):
        """Update the current budget of the task (for including overheads)"""
        self._curwcet = c

    def updatePeriod(self, c):
        """Update the current period of the task (for including overheads)"""
        self._task._curperiod = c
