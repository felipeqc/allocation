class Task:
    taskNumber = 0

    def __init__(self, c, p, d = None):
        if d is None:
            d = p
        self.__class__.taskNumber += 1
        self._number = self.__class__.taskNumber
        self._wcet = float(c)
        self._period = float(p)
        self._deadline = float(d)

    def __str__(self):
        if self._period == self._deadline:
            return '(Task' + str(self._number) + ',C=' + str(self._wcet) + ',T=' + str(self._period) + ',U=' + str(self.util()) + ')'
        else:
            return '(Task' + str(self._number) + ',C=' + str(self._wcet) + ',T=' + str(self._period) + ',D=' + str(self._deadline) + ',U=' + str(self.util()) + ')'

    def __repr__(self):
        return self.__str__()

    def number(self):
        return self._number

    def wcet(self):
        """Return the original cost of the task (without overheads)"""
        return self._wcet

    def period(self):
        """Return the original period of the task (without overheads)"""
        return self._period

    def deadline(self):
        """Return the original deadline of the task (without overheads)"""
        return self._deadline

    def util(self):
        """Return the original utilization of the task (without overheads)"""
        return self._wcet/self._period

    def density(self):
        """Return the original density of the task (without overheads)"""
        return self._wcet/min(self._period, self._deadline)

class TaskOv(Task):
    def __init__(self, c, p, d = None):
        Task.__init__(self, c, p, d)
        self._curwcet = self._wcet
        self._curperiod = self._period
        self._curperiod = self._deadline

    def __str__(self):
        return '(Task' + str(self._number) + ',C=' + str(self._wcet) + ',C\'=' + str(self._curwcet) + ',T=' + str(self._period) + ',T\'=' + str(self._curperiod) + ',D=' + str(self._deadline) + ',D\'=' + str(self._curdeadline) + ',U=' + str(self.util()) + ',U\'=' + str(self.currentUtil()) + ')'

    def __repr__(self):
        return self.__str__()

    def currentWcet(self):
        """Return the current cost of the task (considering overheads)"""
        return self._curwcet

    def currentPeriod(self):
        """Return the current period of the task (considering overheads)"""
        return self._curperiod

    def currentDeadline(self):
        """Return the current deadline of the task (considering overheads)"""
        return self._curperiod

    def currentUtil(self):
        """Return the current utilization of the task (considering overheads)"""
        return self._curwcet/self._curperiod

    def updateWcet(self, c):
        """Update the current cost of the task (for including overheads)"""
        self._curwcet = c

    def updatePeriod(self, p):
        """Update the current period of the task (for including overheads)"""
        self._curperiod = p

    def updateDeadline(self, d):
        """Update the current deadline of the task (for including overheads)"""
        self._curdeadline = pd
