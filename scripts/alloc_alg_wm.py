from alloc_task_wm import *
from alloc_part_wm import *

class WmTaskSet:
    def __init__(self, cpus):
        self._cpus = int(cpus)
        self._partition = [WmPartition(x) for x in xrange(self._cpus)]
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

        self._partition = [WmPartition(x) for x in xrange(self._cpus)] # Clear previous allocation

        if order == 'u':
            # In case of equal utilizations, we prioritize lesser periods.
            task_cmp = lambda t1, t2 : cmp(t1.util(), t2.util()) if t1.util() != t2.util() else -cmp(t1.period(), t2.period()) 
        elif order == 'p':
            # In case of equal periods, we prioritize greater utilizations.
            task_cmp = lambda t1, t2 : cmp(t1.period(), t2.period()) if t1.period() != t2.period() else cmp(t1.util(), t2.util()) 

        remaining_tasks = sorted(self._tasks, cmp=task_cmp) # Sort in descending order (actually it's ascending, but we use pop() to take the elements for efficiency)

        if self._verbose:
	    print 'Scheduling %d tasks using EDF-WM %s-%s' % (len(self._tasks), 'D' + order.upper(), bp.upper() + 'F');
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
                print 'CPU %d, U = %Lf:' % (part.number(), part.util())
                if part.tasks():
                    for task in part.normalTasks():
                        print '- Task %d, C = %Lf, T = %Lf, U = %Lf' % (task.number(), task.wcet(), task.period(), task.util())
                    for s in part.slices():
                        print '- Slice %d:%d, C = %Lf, D = %Lf, \n\t\tT = %Lf, U = %Lf' % (s.task().number(), s.slicenumber(), s.wcet(), s.deadline(), s.period(), s.util()) 
                    print

        return True # Allocation completed

    def _binpacking(self, curTask, bp):

        if bp == 'f': # First-Fit
            for part in self._partition: # For each partition
                part._addTask(curTask) # Add task temporarily
                if part._schedTest():
                    if self._verbose:
                        print 'Task %d -> Processor %d' % (curTask.number(), part.number())
                    return True
                else:
                    part._removeLastTask()
        elif bp == 'w': # Worst-Fit
            max_slack = -1
            max_slack_part = None

            for part in self._partition: # For each partition
                part._addTask(curTask) # Add task temporarily
                if part._schedTest():
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
                # Try to merge the two partitions with minimum utilization and no migratory tasks (worst-Fit improvement)
                part_without_mig = [x for x in self._partition if not x._hasSlices()]
                if(len(part_without_mig) >= 2):
                    p1 = min(part_without_mig, key = lambda part : part.util()) # Partition with minimum utilization
                    part_without_mig.remove(p1)
                    if part_without_mig:
                        p2 = min(part_without_mig, key = lambda part : part.util()) # Partition with second to the minimum utilization

                        # Let's put all tasks in a temporary partition and apply sched test
                        temp_part = WmPartition(-1)
                        for t in p1._tasks + p2._tasks:
                            temp_part._addTask(t) 

                        if temp_part._schedTest():
                            p1._merge(p2)
                            p2._addTask(curTask)
                            if self._verbose:
                                print 'MERGE: Processors %d and %d -> Processor %d' % (p1.number(), p2.number(), p1.number())
                                print 'Task %d -> Processor %d' % (curTask.number(), p2.number())
                            return True

        return False # Bin-Packing failed

    def _split_task(self, curTask, bp, order, remaining_tasks):
        s = 2
        while s <= self._cpus:
            dPrime = curTask.deadline()/s

            if self._verbose:
                print "\ns =",s

            # Let's order partitions by available exec time (decreasing order)
            orderedPartitions = sorted(self._partition, key = lambda part : part._calcExecTime(curTask, dPrime), reverse=True)

            # We called CalcExecTime() of every partition, so now memoExecTime() returns updated values

            i = 0
            remaining = curTask.wcet()
            # While the task is too large to fit in the current processor, break it in slices
            while i < self._cpus and i < s and remaining > 0.0: # Split the task in s slices
                available = orderedPartitions[i]._memoExecTime()
                #if remaining <= available:
                #    break

                orderedPartitions[i]._addSlice(WmSlice(i+1, available, dPrime, curTask))
                if self._verbose:
                    print 'Trying Task %d Slice %d -> Processor %d, remaining: %Lf, available: %Lf' % (curTask.number(), i+1, orderedPartitions[i].number(), remaining, available)

                remaining -= min(available, remaining)
                i += 1

            # Find the CPU to put the last piece of the task (minimizing waste)
            """j = i
            max_util_part = None
            max_util = -1.0
            while j < self._cpus:
                available = orderedPartitions[j]._memoExecTime()
                if self._verbose:
                    print 'Checking Task %d Slice %d -> Processor %d, remaining: %Lf, available: %Lf' % (curTask.number(), i+1, orderedPartitions[j].number(), remaining, available)
                if orderedPartitions[j].util() > max_util and remaining <= available:
                    max_util_part = orderedPartitions[j]
                    max_util = orderedPartitions[j].util()
                j += 1

            if(max_util_part != None):
                available = max_util_part._memoExecTime()
                max_util_part._addSlice(WmSlice(i+1, remaining, dPrime, curTask))

                if self._verbose:
                    print 'Done! Task %d Slice %d -> Processor %d' % (curTask.number(), i+1, max_util_part.number())

                # Try to put small tasks in max_util_part
                temp_list = reversed(remaining_tasks)
                for smallTask in temp_list:
                     max_util_part._addTask(smallTask) # Add task temporarily
                     if max_util_part._schedTest():
                         remaining_tasks.remove(smallTask)
                         if self._verbose:
                             print 'Task %d -> Processor %d' % (smallTask.number(), max_util_part.number())
                     else:
                         max_util_part._removeLastTask()

                return True"""

            if remaining == 0.0:
                return True

            # Allocation failed, we have to remove the tasks to try again with greater s.
            # There are slices in orderedPartitions[0...s-1].
            if self._verbose:
                print "s =", s, "is not enough."
            for j in xrange(s):
                orderedPartitions[j]._removeLastSlice()
            s += 1

        # Can't split the task in slices
        return False
