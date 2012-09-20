import os
import subprocess
import sys
import pickle
from alloc_part_cd import *
from alloc_task_cd import *
import int_qpa
import task

#P2:[(Task3,C=8.59921716,T=19.0,U=0.452590376842), (Slice1:-1,C=0.5,D=0.5,T=2.0)]

p = CDPartition(1)

p._addTask(Task(8,60,11))
p._addTask(Task(12,170,20))
p._addTask(Task(6,120,26))
p._addTask(Task(7,110,80))

"""p._addTask(Task(8,60,10))
p._addTask(Task(12,170,19))
p._addTask(Task(10,210,30))
p._addTask(Task(6,190,36))
p._addTask(Task(8,280,70))
p._addTask(Task(7,320,90))"""

"""p._addTask(Task(6000,31000,18000))
p._addTask(Task(2000,9800,9000))
p._addTask(Task(1000,17000,12000))
p._addTask(Task(90,4200,3000))
p._addTask(Task(8,96,78))
p._addTask(Task(2,12,16))
p._addTask(Task(10,280,120))
p._addTask(Task(26,660,160))"""

"""p._addTask(Task(0.28,50,9))
p._addTask(Task(1.76,10,10))
p._addTask(Task(2.13,200,14))
p._addTask(Task(1.43,200,17))
p._addTask(Task(1.43,200,17))
p._addTask(Task(1.43,100,24))
p._addTask(Task(8.21,100,50))
p._addTask(Task(52.84,200,200))
p._addTask(Task(5.16,1000,400))
p._addTask(Task(6.91,1000,900))
p._addTask(Task(0.18,0.96,0.63))
p._addTask(Task(3.19,62.5,30))
p._addTask(Task(4.08,100,100))
p._addTask(Task(2.5,187,187))"""


"""p._addTask(Task(0.046017, 1.324642, 1.419897))
p._addTask(Task(0.103668, 1.665016, 1.819094))
p._addTask(Task(0.005133, 2.894035, 0.341237))
p._addTask(Task(0.867954, 14.970213, 17.024084)) 
p._addTask(Task(0.138762, 47.98906, 37.186903))
p._addTask(Task(4.374349, 90.746475, 42.335452))
p._addTask(Task(21.725475, 372.991594, 287.330462))
p._addTask(Task(18.601216, 847.449375, 673.81609))
p._addTask(Task(164.298311, 1762.311388, 1874.27352)) 
p._addTask(Task(624.972457, 5787.904261, 5915.216558))
p._addTask(Task(1641.81716, 15549.16986, 7625.959698))
p._addTask(Task(1129.07592, 46697.68032, 4560.327895))
p._addTask(Task(13712.6729, 80125.00202, 92575.63579))
p._addTask(Task(12241.42, 439136.1428, 379004.064))
p._addTask(Task(24268.6361, 715880.6276, 781900.4736))
p._addTask(Task(48061.4305, 1000000, 939573.2658))"""

#p._addTask(Task(1,3))
#p._addTask(Task(3,9))
#p._addTask(Task(9,27, 21))

#t = Task(1.371510, 2)

#p._addTask(Task(13.14195021, 15))
#p._addSlice(CDSlice(1, 0.2321, 0.5, t))

#print p
#print p._h(15)
print p._qpa()

#task.Task.implicit(False)
#l = [task.Task((0, int(1000000*t.wcet()), int(1000000*t.period()), int(1000000*t.deadline()), 0)) for t in p.tasks()]
#assert p._qpa() and int_qpa.QPA(l)
