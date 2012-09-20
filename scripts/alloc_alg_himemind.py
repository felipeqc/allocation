from alloc_task_hime import *
from alloc_part_hime import *
import copy

class HimeMindTaskSet:
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

    def allocate(self):
        """Execute the allocation and fill the partitions"""

        # In case of equal densities, we prioritize lesser deadlines.
        dd_cmp = lambda t1, t2 : cmp(t1.density(), t2.density()) if t1.density() != t2.density() else -cmp(t1.deadline(), t2.deadline())
        # In case of equal deadlines, we prioritize greater densities.
        min_d = lambda t1, t2 : -cmp(t1.deadline(), t2.deadline()) if t1.deadline != t2.deadline() else cmp(t1.density(), t2.density()) 

        if self._verbose:
            print 'Scheduling %d tasks using C=D Split then Pack (DD-MinD)\n' % len(self._tasks);

        for k in range(self._cpus):
            if self._verbose:
                print "k =",k

            self._partition = [HimePartition(x) for x in xrange(self._cpus)] # Clear previous allocation

            temp = sorted(copy.deepcopy(self._tasks), cmp=min_d)
            presel = []
            if k > 0:
                presel = temp[-k:] # We use pop() to take the elements for efficiency, so the list is reversed
            unassigned = sorted(temp[:len(temp)-k], cmp=dd_cmp)

            if self._verbose:
                print "Migratory Tasks"
                for task in reversed(presel):
                    print '%d: C: %Lf, T: %Lf, U: %Lf, Den: %Lf' % (task.number(), task.wcet(), task.period(), task.util(), task.density())
                print "Non-Migratory Tasks"
                for task in reversed(unassigned):
                    print '%d: C: %Lf, T: %Lf, U: %Lf, Den: %Lf' % (task.number(), task.wcet(), task.period(), task.util(), task.density())
                print

            while unassigned:
                curTask = unassigned[-1]
                p = 0
                while p < len(self._partition):
                    if curTask.util() + self._partition[p].util() <= 1.0:
                        self._partition[p]._addTask(curTask)
                        if self._verbose:
                            print 'Task %d -> Processor %d' % (curTask.number(), self._partition[p].number())
                        unassigned.pop()
                        break
                    p += 1

                if p == len(self._partition): # Couldn't allocate this task
                    break

            if unassigned:
                # Could not allocate non-migratory tasks
                # Let's try a greater k
                continue

            p = 0
            s = 1
            unassigned = presel
            while unassigned:
                #print "unassigned", unassigned
                curTask = unassigned[-1]

                # First try to allocate without slicing
                allocated = False
                for part in self._partition:
                    part._addTask(curTask)
                    if part._schedTest():
                        if self._verbose:
                            print 'Task %d -> Processor %d' % (curTask.number(), part.number())
                        unassigned.pop()
                        allocated = True
                        break
                    else:
                        part._removeLastTask()

                if not allocated:
                    freePartitions = [x for x in self._partition if not x.migTask() and curTask.period() <= x._minPeriod()]
                    #print "curtask", curTask
                    #print freePartitions
                    i = 0
                    remaining = curTask.wcet()
                    # While the task is too large to fit in the current processor, break it in slices
                    while i < len(freePartitions):
                        available = freePartitions[i]._sigma(curTask.period())*curTask.period()
                        if remaining <= available:
                            break

                        freePartitions[i]._setMigTask(HimeSlice(i+1, available, curTask))
                        if self._verbose:
                            print 'Task %d Slice %d -> Processor %d, remaining: %Lf, available: %Lf' % (curTask.number(), i+1, freePartitions[i].number(), remaining, available);

                        remaining -= available
                        i += 1

                    # Find the CPU to put the last piece of the task (minimizing waste)
                    j = i
                    max_util_part = None
                    max_util = -1.0
                    while j < len(freePartitions):
                        available = freePartitions[j]._sigma(curTask.period())*curTask.period()
                        if freePartitions[j].util() > max_util and remaining <= available:
                            max_util_part = freePartitions[j]
                            max_util = freePartitions[j].util()
                        j += 1

                    if(max_util_part != None):
                        available = max_util_part._sigma(curTask.period())*curTask.period()
                        max_util_part._setMigTask(HimeSlice(i+1, remaining, curTask))

                        unassigned.pop()

                        if self._verbose:
                            print 'Task %d Slice %d -> Processor %d, remaining: %Lf, available: %Lf' % (curTask.number(), i+1, max_util_part.number(), remaining, available);

                        # Try to put small tasks in max_util_part
                        """temp_list = reversed(remaining_tasks)
                        for smallTask in temp_list:
                            if max_util_part.migTask().period() <= smallTask.period():
                                max_util_part._addTask(smallTask) # Add task temporarily
                                if max_util_part.migTask().util() <= max_util_part._sigma(max_util_part.migTask().period()):
                                    remaining_tasks.remove(smallTask)
                                    if self._verbose:
                                        print 'Task %d -> Processor %d' % (smallTask.number(), max_util_part.number())
                                else:
                                    max_util_part._removeLastTask()"""
                    else:
                        if self._verbose:
                            print "\nAllocation FAILED!\n"
                        return False

            if self._verbose:
                print "\nAllocation OK!\n"
                for part in self._partition:
                    print 'CPU %d, U = %Lf:' % (part.number(), part.util())
                    if part.tasks():
                        for task in part.normalTasks():
                            print '- Task %d, C = %Lf, T = %Lf, U = %Lf' % (task.number(), task.wcet(), task.period(), task.util())
                        if part.migTask():
                            print '- Slice %d:%d, C = %Lf, T = %Lf, U = %Lf' % (part.migTask().task().number(), part.migTask().slicenumber(), part.migTask().wcet(), part.migTask().period(), part.migTask().util()) 
                        print

            return True

        if self._verbose:
            print "\nAllocation FAILED!\n"
        return False
