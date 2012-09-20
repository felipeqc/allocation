import math
from alloc_task import *
from alloc_part import *
#from alloc_overhead import *

class HimePartition(Partition):
    def __init__(self, number):
        Partition.__init__(self, number)
        self._migtask = None

    def util(self):
        """Return the total utilization for NON-MIGRATORY TASKS"""
        return self._nonmigutil

    def normalTasks(self):
        """Return a list with all tasks"""
        return self._tasks

    def migTask(self):
        return self._migtask

    def tasks(self):
        """Return a list with all tasks and slices"""
        if not self._migtask:
            return self._tasks
        else:
            return self._tasks + [self._migtask]

    def _schedTest(self):
        """Apply schedulability test"""
        if not self._migtask: # There isn't a migratory task, so let's check utilization
            return self.util() <= 1.0
        else:
            return self._migtask.util() <= self._sigma(self._migtask.period()) # HIME test. No need to check U <= 1. This test is stronger.

    def _sigma1(self, period):
        min_period = min(self._tasks, key = lambda task : task.period()).period()
        return (1.0 - self.util()) / (1.0 + (period / min_period))

    def _sigma2(self, period):
        sigmasum = 0.0
        for task in self._tasks:
            sigmasum += task.wcet() / (math.floor(task.period() / period)*period)
        return 1.0 - sigmasum

    def _sigma3(self, period):
        min_period = min(self._tasks, key = lambda task : task.period()).period()
        return (1.0 - self.util()) / (1.0 + (self.util() / math.floor(min_period / period)))

    def _sigma(self, period):
        return max(self._sigma1(period), self._sigma2(period), self._sigma3(period))

    def _setMigTask(self, s):
        self._migtask = s

    def _merge(self, otherPart):
        self._nonmigutil += otherPart._nonmigutil
        self._tasks += otherPart._tasks

        # Clear the other partition
        otherPart._nonmigutil = 0.0
        otherPart._tasks = []

    def _minPeriod(self):
        if self._tasks:
            return min(self._tasks, key = lambda task : task.period()).period()
        else:
            return 1E30

    def _minPeriodTaskIndex(self):
        min_period = None
        min_period_index = None

        for i in xrange(len(self._tasks)):
            if min_period == None or self._tasks[i].period() < min_period:
                min_period = self._tasks[i].period()
                min_period_index = i

        return min_period_index

    def _minPeriodTask(self):
        min_period_index = self._minPeriodTaskIndex()

        if min_period_index != None:
            return self._tasks[min_period_index]
        else:
            return None

    def _swapMinPeriodTask(self, otherTask):
        min_period_index = self._minPeriodTaskIndex()

        if min_period_index != None and self._tasks[min_period_index].period() < otherTask.period():
            temp = self._tasks[min_period_index]
            self._tasks[min_period_index] = otherTask
            return temp
        else:
            return otherTask

class HimePartitionOv(HimePartition):
    def __init__(self, number):
        HimePartition.__init__(self, number)

    def currentUtil(self):  # TODO otimizar util
        """Return the total inflated utilization for NON-MIGRATORY TASKS"""
        total = 0.0
        for task in self._tasks:
            total += task.currentUtil()
        return total

    def _schedTest(self, overhead, cpmd):
        """Apply schedulability test"""
        self._updateOverheads(overhead, cpmd) # Update the task parameters first

        if not self._migtask: # There isn't a migratory task, so let's check utilization
            return self.currentUtil() <= 1.0
        else:
            return self._migtask.currentUtil() <= self._sigma(self._migtask.currentPeriod()) # HIME test. No need to check U <= 1. This test is stronger.

    def _migInflated2Normal(self, firstslice, infbudget, overhead, cpmd):
        """Transform inflated budget to normal budget (of a migratory task)"""
        n = len(self._tasks) + 1

        # den is the denominator in the normal overhead accounting formula

        if firstslice: # Slice 1           
            den = 1 - overhead.get('TICK', n) # Denominator. Utick = Ctick, because Ttick = 1. We are using tick units of time.
            for anyTask in self.tasks(): # Mig and Non-mig
                den -= overhead.get('RELEASE', n)/anyTask.period() # DeltaRel / originalPeriod. DeltaCid is assumed to be zero.

            cpre2_num = overhead.get('TICK', n) + overhead.get('RELEASE_LATENCY', n)*overhead.get('TICK', n) # Cpre numerator. Utick = Ctick
            for anyTask in self.tasks(): # Mig and Non-mig
                cpre2_num += overhead.get('RELEASE_LATENCY', n)*(overhead.get('RELEASE', n)/anyTask.period()) + overhead.get('RELEASE', n)  

            cpre2_den = den

            return (infbudget - 2.0*(cpre2_num/cpre2_den) - overhead.get('SEND_RESCHED', n))*den - 2.0*(overhead.get('SCHED', n) + overhead.get('CXS', n)) - cpmd

        else: # Other slices (the difference is that anyTask only consider the other tasks)          
            den = 1 - overhead.get('TICK', n) # Denominator. Utick = Ctick, because Ttick = 1. We are using tick units of time.
            for anyTask in self._tasks: # Only non-mig tasks
                den -= overhead.get('RELEASE', n)/anyTask.period() # DeltaRel / originalPeriod. DeltaCid is assumed to be zero.

            cpre3_num = overhead.get('TICK', n) + overhead.get('RELEASE_LATENCY', n)*overhead.get('TICK', n) # Cpre3 numerator. Utick = Ctick
            for anyTask in self._tasks: # Only non-mig tasks
                cpre3_num += overhead.get('RELEASE_LATENCY', n)*(overhead.get('RELEASE', n)/anyTask.period()) + overhead.get('RELEASE', n)  

            cpre3_den = den

            return (infbudget - 2.0*(cpre3_num/cpre3_den) - overhead.get('SEND_RESCHED', n))*den - 2.0*(overhead.get('SCHED', n) + overhead.get('CXS', n)) - cpmd

    def _updateOverheads(self, overhead, cpmd):
        """Update the CURRENT wcet of all tasks to account for overheads"""
        n = len(self._tasks)
        if self._migtask:
            n += 1

        for task in self._tasks:
            # Update each non-migratory tasks
            num = task.wcet() + 2.0*(overhead.get('SCHED', n) + overhead.get('CXS', n)) + cpmd # Numerator
            
            den = 1 - overhead.get('TICK', n) # Denominator. Utick = Ctick, because Ttick = 1. We are using tick units of time.
            for anyTask in self.tasks(): # Mig and Non-mig
                den -= overhead.get('RELEASE', n)/anyTask.period() # DeltaRel / originalPeriod. DeltaCid is assumed to be zero.

            cpre2_num = overhead.get('TICK', n) + overhead.get('RELEASE_LATENCY', n)*overhead.get('TICK', n) # Cpre2 numerator. Utick = Ctick
            for anyTask in self.tasks(): # Mig and Non-mig
                cpre2_num += overhead.get('RELEASE_LATENCY', n)*(overhead.get('RELEASE', n)/anyTask.period()) + overhead.get('RELEASE', n)  

            cpre2_den = den

            task.updateWcet(num/den + 2.0*(cpre2_num/cpre2_den))
            task.updatePeriod(task.period() - overhead.get('RELEASE_LATENCY', n))

        if self._migtask:
            # Update migratory task
            mig = self._migtask

            if mig.slicenumber() == 1: # Slice 1
                num = mig.wcet() + 2.0*(overhead.get('SCHED', n) + overhead.get('CXS', n)) + cpmd # Numerator
            
                den = 1 - overhead.get('TICK', n) # Denominator. Utick = Ctick, because Ttick = 1. We are using tick units of time.
                for anyTask in self.tasks(): # Mig and Non-mig
                    den -= overhead.get('RELEASE', n)/anyTask.period() # DeltaRel / originalPeriod. DeltaCid is assumed to be zero.

                cpre2_num = overhead.get('TICK', n) + overhead.get('RELEASE_LATENCY', n)*overhead.get('TICK', n) # Cpre numerator. Utick = Ctick
                for anyTask in self.tasks(): # Mig and Non-mig
                    cpre2_num += overhead.get('RELEASE_LATENCY', n)*(overhead.get('RELEASE', n)/anyTask.period()) + overhead.get('RELEASE', n)  

                cpre2_den = den

                mig.updateWcet(num/den + 2.0*(cpre2_num/cpre2_den) + overhead.get('SEND_RESCHED', n)) # Including IPI
                mig.updatePeriod(mig.period() - overhead.get('RELEASE_LATENCY', n))

            else: # Other slices (the difference is that anyTask only consider the other tasks)
                num = mig.wcet() + 2.0*(overhead.get('SCHED', n) + overhead.get('CXS', n)) + cpmd # Numerator
            
                den = 1 - overhead.get('TICK', n) # Denominator. Utick = Ctick, because Ttick = 1. We are using tick units of time.
                for anyTask in self._tasks: # Only non-mig tasks
                    den -= overhead.get('RELEASE', n)/anyTask.period() # DeltaRel / originalPeriod. DeltaCid is assumed to be zero.

                cpre3_num = overhead.get('TICK', n) + overhead.get('RELEASE_LATENCY', n)*overhead.get('TICK', n) # Cpre3 numerator. Utick = Ctick
                for anyTask in self._tasks: # Only non-mig tasks
                    cpre3_num += overhead.get('RELEASE_LATENCY', n)*(overhead.get('RELEASE', n)/anyTask.period()) + overhead.get('RELEASE', n)  

                cpre3_den = den

                mig.updateWcet(num/den + 2.0*(cpre3_num/cpre3_den) + overhead.get('SEND_RESCHED', n)) # Including IPI
                mig.updatePeriod(mig.period() - overhead.get('RELEASE_LATENCY', n))

    def _minCurrentPeriod(self):
        if self._tasks:
            return min(self._tasks, key = lambda task : task.currentPeriod()).currentPeriod()
        else:
            return 1E30

    # Sigma functions should use updated parameters (with overheads)
    def _sigma1(self, period):
        return (1.0 - self.util()) / (1.0 + (period / self._minCurrentPeriod()))

    def _sigma2(self, period):
        sigmasum = 0.0
        for task in self._tasks:
            sigmasum += task.wcet() / (math.floor(task.currentPeriod() / period)*period)
        return 1.0 - sigmasum

    def _sigma3(self, period):
        return (1.0 - self.util()) / (1.0 + (self.util() / math.floor(self._minCurrentPeriod() / period)))

    def _sigma(self, period):
        return max(self._sigma1(period), self._sigma2(period), self._sigma3(period))
