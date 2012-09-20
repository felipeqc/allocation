from alloc_task_cd import *
from alloc_part_cd import *
import copy

class CDTaskSet:
    def __init__(self, cpus):
        self._cpus = int(cpus)
        self._partition = [CDPartition(x) for x in xrange(self._cpus)]
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

    def dd_cmp(self, t1, t2):
        if t1.density() != t2.density():
            return cmp(t1.density(), t2.density())
        elif t1.deadline() != t2.deadline():
            return -cmp(t1.deadline(), t2.deadline())
        else:
            return -cmp(t1.number(), t2.number())

    def min_d(self, t1, t2):
        if t1.deadline() != t2.deadline():
            return -cmp(t1.deadline(), t2.deadline())
        elif t1.density() != t2.density():
            return cmp(t1.density(), t2.density())
        else:
            return -cmp(t1.number(), t2.number())

    def allocate(self):
        """Execute the allocation and fill the partitions"""

        # In case of equal densities, we prioritize lesser deadlines.
        dd_cmp2 = lambda t1, t2 : cmp(t1.density(), t2.density()) if t1.density() != t2.density() else -cmp(t1.deadline(), t2.deadline())
        # In case of equal deadlines, we prioritize greater densities.
        min_d2 = lambda t1, t2 : -cmp(t1.deadline(), t2.deadline()) if t1.deadline() != t2.deadline() else cmp(t1.density(), t2.density()) 

        if self._verbose:
            print 'Scheduling %d tasks using C=D Split then Pack (DD-MinD)\n' % len(self._tasks);

        for k in range(self._cpus):
            if self._verbose:
                print "\nk =",k

            self._partition = [CDPartition(x) for x in xrange(self._cpus)] # Clear previous allocation

            temp = sorted(copy.deepcopy(self._tasks), cmp=self.min_d)
            presel = []
            if k > 0:
                presel = temp[-k:] # We use pop() to take the elements for efficiency, so the list is reversed
            unassigned = sorted(temp[:len(temp)-k], cmp=self.dd_cmp)

            if self._verbose:
                print "Migratory Tasks"
                for task in reversed(presel):
                    print '%d: C: %Lf, T: %Lf, D: %Lf, U: %Lf, Den: %Lf' % (task.number(), task.wcet(), task.period(), task.deadline(), task.util(), task.density())
                print "Non-Migratory Tasks"
                for task in reversed(unassigned):
                    print '%d: C: %Lf, T: %Lf, D: %Lf, U: %Lf, Den: %Lf' % (task.number(), task.wcet(), task.period(), task.deadline(), task.util(), task.density())
                print

            while unassigned:
                curTask = unassigned[-1]
                p = 0
                while p < len(self._partition):
                    self._partition[p]._addTask(curTask) # Add task temporarily
                    if self._partition[p]._schedTest():
                        if self._verbose:
                            print 'Task %d -> Processor %d' % (curTask.number(), self._partition[p].number())
                        unassigned.pop()
                        break
                    else:
                        self._partition[p]._removeLastTask()
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
            while unassigned and p < self._cpus:
                curTask = unassigned[-1]
                # Add task temporarily
                self._partition[p]._addTask(curTask) if s == 1 else self._partition[p]._addSlice(CDSlice(s, curTask.wcet(), curTask.deadline(), curTask))
                if self._partition[p]._schedTest():
                    if self._verbose:
                        if s == 1:
                            print 'Task %d -> Processor %d' % (curTask.number(), self._partition[p].number())
                        else:
                            print 'Task %d Slice %d -> Processor %d, C = %Lf, D = %Lf, T = %Lf' % (curTask.number(), s, self._partition[p].number(), curTask.wcet(), curTask.deadline(), curTask.period())
                    unassigned.pop()
                    s = 1
                else:
                    self._partition[p]._removeLastTask() if s == 1 else self._partition[p]._removeLastSlice()

                    # split task
                    available = self._partition[p]._calcExecTime(curTask)

                    if available <= 0.0: # Don't create an empty slice, jump to next processor
                        p += 1
                        continue

                    self._partition[p]._addSlice(CDSlice(s, available, available, curTask))

                    if self._verbose:
                        print 'Task %d Slice %d -> Processor %d, C = %Lf, D = %Lf, T = %Lf' % (curTask.number(), s, self._partition[p].number(), available, available, curTask.period())

                    curTask._wcet -= available
                    curTask._deadline -= available

                    s += 1
                    p += 1

            if not unassigned:
                if self._verbose:
                    print "\nAllocation OK!\n"
                    for part in self._partition:
                        print 'CPU %d, U = %Lf:' % (part.number(), part.util())
                        if part.tasks():
                            for task in part.normalTasks():
                                print '- Task %d, C = %Lf, T = %Lf, U = %Lf' % (task.number(), task.wcet(), task.period(), task.util())
                            for s in part.slices():
                                print '- Slice %d:%d, C = %Lf, D = %Lf, \n\t\tT = %Lf, U = %Lf' % (s.task().number(), s.slicenumber(), s.wcet(), s.deadline(), s.period(), s.util()) 
                            print

                return True

        if self._verbose:
            print "\nAllocation FAILED!\n"
        return False
