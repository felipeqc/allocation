class WmSlice:
    def __init__(self, snum, c, d, task):
        """Initialize a slice with a number, budget, relative deadline and the task which it represents"""
        self._slicenumber = snum
        self._wcet = c
        self._deadline = d
        self._task = task

    def __str__(self):
        """String representation"""
        return '(Slice' + str(self._task.number()) + ':' + str(self._slicenumber)+ ',C=' + str(self._wcet) + ',D=' + str(self._deadline) + ',T=' + str(self.period()) + ')'

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
        """Return the budget of the slice"""
        return self._wcet

    def deadline(self):
        """Return the relative deadline of the slice"""
        return self._deadline

    def period(self):
        """Return the period of the slice"""
        return self._task._period

    def util(self):
        """Return the utilization of the slice"""
        return self._wcet/self._task._period
