from alloc_task_hime import *
from alloc_part_hime import *

class HimeTaskSetOv:
    def __init__(self, cpus, ov, cpmd):
        self._cpus = int(cpus)
        self._partition = [HimePartitionOv(x) for x in xrange(self._cpus)]
        self._tasks = []
        self._verbose = False
        Task.taskNumber = 0
        self._overhead = ov
        self._cpmd = cpmd

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
        self._tasks.append(TaskOv(c, p))

    def allocate(self, bp = 'f', order = 'u'):
        """Execute the allocation and fill the partitions"""

        self._partition = [HimePartitionOv(x) for x in xrange(self._cpus)] # Clear previous allocation

        if order == 'u':
            # In case of equal utilizations, we prioritize lesser periods.
            task_cmp = lambda t1, t2 : cmp(t1.util(), t2.util()) if t1.util() != t2.util() else -cmp(t1.period(), t2.period()) 
        elif order == 'p':
            # In case of equal periods, we prioritize greater utilizations.
            task_cmp = lambda t1, t2 : cmp(t1.period(), t2.period()) if t1.period() != t2.period() else cmp(t1.util(), t2.util()) 

        remaining_tasks = sorted(self._tasks, cmp=task_cmp) # Sort in descending order (actually it's ascending, but we use pop() to take the rightmost elements first, for efficiency)

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
                print 'CPU %d, U = %Lf, U\' = %Lf:' % (part.number(), part.util(), part.currentUtil())
                if part.tasks():
                    for task in part.normalTasks():
                        print 'Task %d, C = %Lf, C\' = %Lf, T = %Lf, T\' = %Lf, U = %Lf, U\' = %Lf' % (task.number(), task.wcet(), task.currentWcet(), task.period(), task.currentPeriod(), task.util(), task.currentUtil())
                    if part.migTask():
                        print 'Slice %d:%d, C = %Lf, C\' = %Lf, T = %Lf, T\' = %Lf, U = %Lf, U\' = %Lf' % (part.migTask().task().number(), part.migTask().slicenumber(), part.migTask().wcet(), part.migTask().currentWcet(), part.migTask().period(), part.migTask().currentPeriod(), part.migTask().util(), part.migTask().currentUtil()) 
                    print

        return True # Allocation completed

    def _binpacking(self, curTask, bp):
        if bp == 'f': # First-Fit
            for part in self._partition: # For each partition
                part._addTask(curTask) # Add task temporarily
                if (not part.migTask() or part.migTask().period() <= curTask.period()) and part._schedTest(self._overhead, self._cpmd): # Schedulable (it updates the overheads before checking)
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
                if (not part.migTask() or part.migTask().period() <= curTask.period()) and part._schedTest(self._overhead, self._cpmd): # Schedulable (it updates the overheads before checking)
                    if 1.0 - part.currentUtil() > max_slack: # Get the partition with the greatest slack (considering overheads)
                        max_slack = 1.0 - part.currentUtil()
                        max_slack_part = part
                part._removeLastTask() # Remove task anyway

            if max_slack_part != None:
                max_slack_part._addTask(curTask) # Add task permanently
                if self._verbose:
                    print 'Task %d -> Processor %d' % (curTask.number(), max_slack_part.number())
                return True
            else:
                # Let's try to merge the two partitions with minimum utilization (worst-Fit improvement)
                #
                # util(union(p1,p2)) <= 1 doesn't imply the partition will be schedulable
                # To find a succesfull merge, we'd have to iterate for each pair of partitions and recalculate overheads.
                # Instead, we get the two partitions with the least util() and try to merge them. So we recalculate overheads only once.
                part_without_mig = [x for x in self._partition if not x.migTask()]
                if(len(part_without_mig) >= 2):
                    p1 = min(part_without_mig, key = lambda part : part.util()) # Partition with minimum utilization (considering overheads)
                    part_without_mig.remove(p1)
                    if part_without_mig:
                        p2 = min(part_without_mig, key = lambda part : part.util()) # Partition with second to the minimum utilization (considering overheads)

                        # We can't just sum both util(), we have to put all tasks in a temporary partition
                        temp_part = HimePartitionOv(-1)
                        for t in p1.normalTasks():
                            temp_part._addTask(t)
                        for t in p2.normalTasks():
                            temp_part._addTask(t)

                        if temp_part._schedTest(self._overhead, self._cpmd): # The merged partition is schedulable (it updates the overheads before checking)
                            del temp_part
                            p1._merge(p2)
                            p2._addTask(curTask)
                            if self._verbose:
                                print 'MERGE: Processors %d and %d -> Processor %d' % (p1.number(), p2.number(), p1.number())
                                print 'Task %d -> Processor %d' % (curTask.number(), p2.number())
                            return True

        return False # Bin-Packing failed

    def _split_task(self, curTask, bp, order, remaining_tasks):
        if(order == 'u'): # HIME DU
            # Exchange the task with the one with minimum period of partitions without migratory tasks (MigTaskAllocDU)
            #
            # There is a problem here. The current task not necessarily can be exchanged with the task of minimum period.
            # The partition can turn to be not schedulable after we update the overheads, so we have to test that.
            # A better solution would be to test each lower period task until we find a schedulable situation. But that would be a more expensive operation.
            # If the exchange can't be made, the current task won't be able to migrate to some partitions. So we need to verify that afterwards, when slicing the task.
            # This situation only occurs when we consider overheads.
            #
            # IMPORTANT: We are using period() instead of currentPeriod() [with overheads], but it's ok, because p1 < p2 iff cur_p1 < cur_p2. We just can't use normal periods
            # when doing schedulability analysis.

            min_period = curTask.period()
            min_period_partition = None
            min_period_index = None

            for part in self._partition:
                if not part.migTask() and part.util() < 1.0: # Also, we don't disassemble a partition which is already 100% full
                    for i in xrange(len(part._tasks)):
                        if part._tasks[i].period() < min_period:
                            min_period = part._tasks[i].period()
                            min_period_partition = part
                            min_period_index = i

            if min_period_index != None:
                # Swap them
                curTask = min_period_partition._swapTask(min_period_index, curTask)

                if min_period_partition._schedTest(self._overhead, self._cpmd): # The partition is schedulable
                    if self._verbose:
                        print 'Task %d (Proc. %d) <=> Task %d' % (curTask.number(), min_period_partition.number(), min_period_partition._tasks[min_period_index].number())
                else:
                    # Swap them back
                    curTask = min_period_partition._swapTask(min_period_index, curTask)

        # MigTaskAlloc

        # Let's proceed with task slicing. We first allocate slice 1, because it uses a specific formula at overhead accounting.
        # Since the value of sigma depends on the parameters of the other tasks, and those parameters depend on the period of the task to be inserted, we do a little trick.
        # We insert a dummy slice of curTask, calculate sigma for every partition to obtain the available inflated budget, and then we calculate the available normal budget.

        slicenum = 1
        remaining = curTask.wcet() # Remaining normal budget of the task to be sliced

        freePartitions = [part for part in self._partition if (not part.migTask()) and curTask.period() <= part._minPeriod()] # We can check just the normal period, as explained above.

        # Let's add slice 1 first, since it uses a different overhead equation
        normalBudget = -1.0 # Available normal budget
        inflatedBudget = None # Available inflated budget
        firstSlicePart = None

        for part in freePartitions:
            part._setMigTask(HimeSliceOv(-1, 0, curTask)) # Dummy slice
            part._updateOverheads(self._overhead, self._cpmd) # Update overheads
            inftemp = part._sigma(part.migTask().currentPeriod())*part.migTask().currentPeriod() # Available inflated budget of this partition
            normtemp = part._migInflated2Normal(firstslice = True, infbudget = inftemp, overhead = self._overhead, cpmd = self._cpmd) # Available normal budget of this partition
            if normtemp > normalBudget:
                normalBudget = normtemp
                inflatedBudget = inftemp
                firstSlicePart = part

        
        if firstSlicePart != None and normalBudget > 0.0: # Make sure the first slice has available budget
            remaining -= normalBudget

            # We kept the dummy task, let's just update the parameters
            firstSlicePart.migTask()._wcet = normalBudget # Normal budget
            firstSlicePart.migTask().updateWcet(inflatedBudget) # Budget with overheads
            firstSlicePart.migTask().updateSliceNumber(slicenum)

            if self._verbose:
                print 'Task %d Slice 1 -> Processor %d, available: %Lf, remaining: %Lf' % (curTask.number(), firstSlicePart.number(), normalBudget, remaining);

            slicenum += 1

            freePartitions.remove(firstSlicePart) # Remove this partition from the list
        else:
            return False

        
        # Let's sort the rest of the partitions by their available normal budget. All of them use the same equation.
        # Remember they already have the dummy slice and the overhead costs have already been accounted for.

        inflatedBudget = [-1.0 for x in self._partition]
        normalBudget = [-1.0 for x in self._partition]

        for part in freePartitions:
            inflatedBudget[part._number] = part._sigma(part.migTask().currentPeriod())*part.migTask().currentPeriod()
            normalBudget[part._number] = part._migInflated2Normal(firstslice = False, infbudget = inflatedBudget[part._number], overhead = self._overhead, cpmd = self._cpmd)

        freePartitions.sort(key = (lambda part : normalBudget[part._number]), reverse=True) # Sort using available normal budget
        toBeRemoved = []

        # While the task is too large to fit in the current processor, break it in slices
        i = 0
        while(i < len(freePartitions)):
            # If the current partition has no available space or we have already created all slices except the last one
            if normalBudget[freePartitions[i]._number] <= 0.0 or remaining <= normalBudget[freePartitions[i]._number]: 
                break

            remaining -= normalBudget[freePartitions[i]._number]

            # We kept the dummy task, let's just update the parameters
            freePartitions[i].migTask().updateSliceNumber(slicenum)
            freePartitions[i].migTask()._wcet = normalBudget[freePartitions[i]._number] # Normal budget
            freePartitions[i].migTask().updateWcet(inflatedBudget[freePartitions[i]._number]) # Budget with overheads

            if self._verbose:
                print 'Task %d Slice %d -> Processor %d, available: %Lf, remaining: %Lf' % (curTask.number(), slicenum, freePartitions[i].number(), normalBudget[freePartitions[i]._number], remaining);

            slicenum += 1

            toBeRemoved.append(freePartitions[i])
            i += 1

        for part in toBeRemoved:
            freePartitions.remove(part)

        # Find the CPU to put the last piece of the task, minimizing waste.
        # We check the current utilization (with overheads) for that.
        j = 0
        max_util_part = None
        max_util = -1.0
        while(j < len(freePartitions)):
            # If the current partition has no available space
            if normalBudget[freePartitions[j]._number] <= 0.0:
                break

            # Get the partition with maximum utilization in which the remaining cost fits
            if freePartitions[j].currentUtil() > max_util and remaining <= normalBudget[freePartitions[j]._number]:
                max_util_part = freePartitions[j]
                max_util = freePartitions[j].currentUtil()
            j += 1

        if(max_util_part != None):
            # We kept the dummy task, let's just update the parameters
            max_util_part.migTask().updateSliceNumber(slicenum)
            max_util_part.migTask()._wcet = remaining # Normal budget
            max_util_part._updateOverheads(self._overhead, self._cpmd) # Budget with overheads. TODO: Slow

            if self._verbose:
                print 'Task %d Slice %d -> Processor %d, available: %Lf, remaining: %Lf' % (curTask.number(), slicenum, max_util_part.number(), normalBudget[max_util_part.number()], 0.0);

            # Try to put small tasks in max_util_part
            temp_list = reversed(remaining_tasks)
            for smallTask in temp_list:
                if max_util_part.migTask().period() <= smallTask.period():
                    max_util_part._addTask(smallTask) # Add task temporarily
                    if max_util_part._schedTest(self._overhead, self._cpmd): # Schedulable (it updates the overheads before checking)
                        remaining_tasks.remove(smallTask)
                        if self._verbose:
                            print 'Task %d -> Processor %d' % (smallTask.number(), max_util_part.number())
                    else:
                        max_util_part._removeLastTask()


            freePartitions.remove(max_util_part)

            for part in freePartitions:
                part._setMigTask(None) # Remove dummy slices from unused partitions

            return True
        else:
            return False
