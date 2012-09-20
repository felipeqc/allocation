from alloc_task_hime import *
from alloc_part_hime import *

class HimeTaskSet:
    def __init__(self, cpus):
        self._cpus = int(cpus)
        self._partition = [HimePartition(x) for x in xrange(self._cpus)]
        self._tasks = []
        self._verbose = False
        Task.taskNumber = 0

    def setVerbose(self, option):
        self._verbose = option

    def tasks(self):
        """Return list of tasks"""
        return self._tasks

    def partitions(self):
        """Return list of partitions"""
        return sorted(self._partition, key = lambda part : part.number())

    def cpus(self):
        """Return the number of cpus"""
        return self._cpus

    def createTask(self, c, p):
        """Create a task with WCET c and period p"""
        self._tasks.append(Task(c, p))

    def allocate(self, bp = 'f', order = 'u'):
        """Execute the allocation and fill the partitions"""

        self._partition = [HimePartition(x) for x in xrange(self._cpus)] # Clear previous allocation

        if order == 'u':
            # In case of equal utilizations, we prioritize lesser periods.
            task_cmp = lambda t1, t2 : cmp(t1.util(), t2.util()) if t1.util() != t2.util() else -cmp(t1.period(), t2.period()) 
        elif order == 'p':
            # In case of equal periods, we prioritize greater utilizations.
            task_cmp = lambda t1, t2 : cmp(t1.period(), t2.period()) if t1.period() != t2.period() else cmp(t1.util(), t2.util()) 

        remaining_tasks = sorted(self._tasks, cmp=task_cmp) # Sort in descending order (actually it's ascending, but we use pop() to take the elements for efficiency)

        if self._verbose:
	    print 'Scheduling %d tasks using HIME-%s-%s' % (len(self._tasks), 'D' + order.upper(), bp.upper() + 'F');
	    for task in reversed(remaining_tasks):
		print '%d: C: %Lf, T: %Lf, U: %Lf' % (task.number(), task.wcet(), task.period(), task.util())
	    print

        while remaining_tasks:
            curTask = remaining_tasks.pop()
            if not self._binpacking(curTask, bp) and not self._split_task(curTask, bp, order, remaining_tasks): # If bin-packing failed and task splitting also failed
                if self._verbose:
                    print '\nAllocation FAILED!'
                return False

        if self._verbose:
            print '\nAllocation OK!\n'
            for part in self._partition:
                print 'CPU %d, U = %Lf%s:' % (part.number(), part.util(), " (%.10f with migtask)" % (part.util() + part.migTask().util()) if part.migTask() else "")
                if part.tasks():
                    for task in part.normalTasks():
                        print 'Task %d, C = %Lf, T = %Lf, U = %Lf' % (task.number(), task.wcet(), task.period(), task.util())
                    if part.migTask():
                        print 'Slice %d:%d, C = %Lf, T = %Lf, U = %Lf' % (part.migTask().task().number(), part.migTask().slicenumber(), part.migTask().wcet(), part.migTask().period(), part.migTask().util()) 
                    print

        return True # Allocation completed

    def _binpacking(self, curTask, bp):

        if bp == 'f': # First-Fit
            for part in self._partition: # For each partition
                if not part.migTask(): # There are no migratory tasks, so we can apply utilization test
                    if curTask.util() + part.util() <= 1.0:
                        part._addTask(curTask)
                        if self._verbose:
                            print 'Task %d -> Processor %d' % (curTask.number(), part.number())
                        return True
                elif part.migTask().period() <= curTask.period(): # If migratory task's period is not greater than this task's period
                     part._addTask(curTask) # Add task temporarily
                     #print 'Trying to add task %d to proc %d: sigma %Lf' % (curTask.number(), part.number(), part._sigma(part.migTask().period()))
                     if part.migTask().util() <= part._sigma(part.migTask().period()): # HIME test. No need to check U <= 1. This test is stronger.
                         if self._verbose:
                             print 'Task %d -> Processor %d' % (curTask.number(), part.number())
                         return True
                     else:
                         part._removeLastTask()
        elif bp == 'w': # Worst-Fit
            max_slack = -1
            max_slack_part = None

            for part in self._partition: # For each partition
                if not part.migTask(): # There are no migratory tasks, so we can apply utilization test
                    if curTask.util() + part.util() <= 1.0:
                        if 1.0 - part.util() > max_slack:
                            max_slack = 1.0 - part.util()
                            max_slack_part = part
                elif part.migTask().period() <= curTask.period(): # If migratory task's period is not greater than this task's period
                    part._addTask(curTask) # Add task temporarily
                    if part.migTask().util() <= part._sigma(part.migTask().period()): # HIME test. No need to check U <= 1. This test is stronger.
                        if 1.0 - part.util() > max_slack:
                            max_slack = 1.0 - part.util()
                            max_slack_part = part

                    part._removeLastTask() # Remove task anyway

            if max_slack_part != None:
                max_slack_part._addTask(curTask) # Add task permanently
                if self._verbose:
                    print 'Task %d -> Processor %d' % (curTask.number(), max_slack_part.number())
                return True
            else:
                # Try to merge the two partitions with minimum utilization (worst-Fit improvement)
                part_without_mig = [x for x in self._partition if not x.migTask()]
                if(len(part_without_mig) >= 2):
                    p1 = min(part_without_mig, key = lambda part : part.util()) # Partition with minimum utilization
                    part_without_mig.remove(p1)
                    if part_without_mig:
                        p2 = min(part_without_mig, key = lambda part : part.util()) # Partition with second to the minimum utilization
                        if p1.util() + p2.util() <= 1.0:
                            p1._merge(p2)
                            p2._addTask(curTask)
                            if self._verbose:
                                print 'MERGE: Processors %d and %d -> Processor %d' % (p1.number(), p2.number(), p1.number())
                                print 'Task %d -> Processor %d' % (curTask.number(), p2.number())
                            return True

        return False # Bin-Packing failed

    def _split_task(self, curTask, bp, order, remaining_tasks):
        if(order == 'u'): # HIME DU
            # Exchange the task with the one with minimum period of the whole system (except partitions with migratory tasks) (MigTaskAllocDU)
            min_period = curTask.period()
            min_period_partition = None
            min_period_index = None

            for part in self._partition:
                if not part.migTask() and part.util() < 1.0:
                    for i in xrange(len(part._tasks)):
                        if part._tasks[i].period() < min_period:
                            min_period = part._tasks[i].period()
                            min_period_partition = part
                            min_period_index = i

            if min_period_index != None:
                # Swap them
                curTask = min_period_partition._swapTask(min_period_index, curTask)

                if self._verbose:
                    print 'Task %d (Proc. %d) <=> Task %d' % (curTask.number(), min_period_partition.number(), min_period_partition._tasks[min_period_index].number())

        # MigTaskAlloc

        # Let's order partitions by sigma (decreasing). Partitions that already have migratory tasks are put at the end.
        orderedPartitions = sorted(self._partition, key = lambda part : part._sigma(curTask.period()) if not part.migTask() else -1.0, reverse=True)

        i = 0
        remaining = curTask.wcet()
        # While the task is too large to fit in the current processor, break it in slices
        while(i < self._cpus and  not orderedPartitions[i].migTask()):
            available = orderedPartitions[i]._sigma(curTask.period())*curTask.period()
            if remaining <= available:
                break

            orderedPartitions[i]._setMigTask(HimeSlice(i+1, available, curTask))
            if self._verbose:
                print 'Task %d Slice %d -> Processor %d, remaining: %Lf, available: %Lf' % (curTask.number(), i+1, orderedPartitions[i].number(), remaining, available);

            remaining -= available
            i += 1

        # Find the CPU to put the last piece of the task (minimizing waste)
        j = i
        max_util_part = None
        max_util = -1.0
        while(j < self._cpus and not orderedPartitions[j].migTask()):
            available = orderedPartitions[j]._sigma(curTask.period())*curTask.period()
            if orderedPartitions[j].util() > max_util and remaining <= available:
                max_util_part = orderedPartitions[j]
                max_util = orderedPartitions[j].util()
            j += 1

        if(max_util_part != None):
            available = max_util_part._sigma(curTask.period())*curTask.period()
            max_util_part._setMigTask(HimeSlice(i+1, remaining, curTask))

            if self._verbose:
                print 'Task %d Slice %d -> Processor %d, remaining: %Lf, available: %Lf' % (curTask.number(), i+1, max_util_part.number(), remaining, available);

            # Try to put small tasks in max_util_part
            temp_list = reversed(remaining_tasks)
            for smallTask in temp_list:
                if max_util_part.migTask().period() <= smallTask.period():
                     max_util_part._addTask(smallTask) # Add task temporarily
                     if max_util_part.migTask().util() <= max_util_part._sigma(max_util_part.migTask().period()):
                         remaining_tasks.remove(smallTask)
                         if self._verbose:
                             print 'Task %d -> Processor %d' % (smallTask.number(), max_util_part.number())
                     else:
                         max_util_part._removeLastTask()

            return True
        else:
            return False
