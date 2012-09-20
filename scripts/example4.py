import os
import subprocess
import sys
import pickle
import alloc_alg_cd as cd
import int_qpa
import task

s = cd.CDTaskSet(5)
s.setVerbose(True)

"""s.createTask(1.07405014,2)
s.createTask(2.62655436,5)
s.createTask(4.25197068,8)
s.createTask(1.25749268,4)
s.createTask(8.73098010,14)
s.createTask(24.68196289,28)
s.createTask(4.37989001,9)"""

e = 0.000001
k=0.25
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+k,1.5)
s.createTask(1+k,1.5)

"""s.createTask(2.95533833,3)
s.createTask(5.71001129,8)
s.createTask(4.92044153,7)
s.createTask(0.12417671,2)
s.createTask(2.01080292,6)
s.createTask(6.72695394,7)"""

"""s.createTask(1.01,2)
s.createTask(1.01,2)
s.createTask(1.01,2)
s.createTask(1.01,2)
s.createTask(1.01,2)
s.createTask(1.48,1.5)
s.createTask(1.48,1.5)"""

"""s.createTask(30.25707492,42)
s.createTask(0.68512816,1)
s.createTask(1.94357511,3)
s.createTask(9.93136320,27)
s.createTask(2.43825839,3)
s.createTask(13.98654294,21)"""

"""s.createTask(7,10)
s.createTask(7,10)
s.createTask(7,10)
s.createTask(7,10)
s.createTask(6,7)"""

#<properties hyperperiod="92210040" utilization="2.96000000" />
"""s.createTask(0.00654686,1)
s.createTask(13.32806769,51)
s.createTask(6.21880037,40)
s.createTask(1.13536344,3)
s.createTask(13.88252884,19)
s.createTask(7.31101851,61)
s.createTask(16.62833523,45)
s.createTask(12.19612228,13)"""

#<properties hyperperiod="106020" utilization="3.92000000" />
"""s.createTask(137,200)
s.createTask(1181,3100)
s.createTask(859,1900)
s.createTask(1946,2000)
s.createTask(496,900)
s.createTask(1314,1500)"""

#<properties hyperperiod="106020" utilization="3.92000000" />
"""s.createTask(1.37150963,2)
s.createTask(11.81605462,31)
s.createTask(8.59921716,19)
s.createTask(19.46288118,20)
s.createTask(4.96095913,9)
s.createTask(13.14195021,15)"""

#<properties hyperperiod="2063970" utilization="3.92000000" />
"""s.createTask(0.50805005,2)
s.createTask(20.36227122,38)
s.createTask(2.43234197,3)
s.createTask(0.99023697,5)
s.createTask(1.59109136,3)
s.createTask(6.76293885,9)
s.createTask(21.63067600,34)
s.createTask(14.43429232,71)"""

# BOM <properties hyperperiod="168" utilization="3.76000000" />
"""s.createTask(2.95533833,3)
s.createTask(5.71001129,8)
s.createTask(4.92044153,7)
s.createTask(0.12417671,2)
s.createTask(2.01080292,6)
s.createTask(6.72695394,7)"""

#<properties hyperperiod="421665873300" utilization="3.68000000" />
"""s.createTask(3.90714455,84)
s.createTask(3.48486422,79)
s.createTask(39.70616795,50)
s.createTask(3.47811832,5)
s.createTask(0.02386321,1)
s.createTask(0.34533880,7)
s.createTask(0.06633977,9)
s.createTask(1.64302256,76)
s.createTask(31.04027324,43)
s.createTask(22.57463469,61)
s.createTask(1.98383312,17)
s.createTask(3.15520464,4)"""

#<properties hyperperiod="15810" utilization="3.84000000" />
"""s.createTask(5.05246096,10)
s.createTask(92.70035349,93)
s.createTask(0.65984633,1)
s.createTask(12.29607445,51)
s.createTask(4.81254883,6)
s.createTask(6.34938609,10)"""

#<properties hyperperiod="58088520" utilization="3.84000000" />
"""s.createTask(85.88559398,89)
s.createTask(69.46064351,90)
s.createTask(3.88593293,8)
s.createTask(0.65140309,1)
s.createTask(45.56024258,98)
s.createTask(18.54304066,37)"""

#<properties hyperperiod="6257790" utilization="3.76000000" />
"""s.createTask(47.39579388,54)
s.createTask(28.82183682,49)
s.createTask(0.38339359,1)
s.createTask(27.07738312,55)
s.createTask(16.97900606,43)
s.createTask(2.45115122,45)
s.createTask(10.61549687,30)
s.createTask(6.76730108,11)"""

"""s.createTask(20.86783435,35)
s.createTask(37.96020861,40)
s.createTask(11.70988193,33)
s.createTask(11.53958577,12)
s.createTask(0.96361802,13)
s.createTask(21.92606258,83)"""

"""s.createTask(1.64089977,3)
s.createTask(6.33249692,21)
s.createTask(47.83631956,85)
s.createTask(15.18951363,19)
s.createTask(0.12315423,4)
s.createTask(25.32117679,97)
s.createTask(11.43848155,22)
s.createTask(27.28731597,37)"""

"""s.createTask(6.31570667,10)
s.createTask(2.39520364,21)
s.createTask(1.60992678,2)
s.createTask(0.99991724,1)
s.createTask(1.43472774,2)
s.createTask(0.65212752,1)"""

"""s.createTask(6.50507,16)
s.createTask(9.45353,14)
s.createTask(76.89867,80)
s.createTask(12.43273,30)
s.createTask(55.26938,95)
s.createTask(13.21109,15)"""

#<properties hyperperiod="1268820" utilization="3.84000000" />
"""s.createTask(5.85019902,14)
s.createTask(22.72001451,38)
s.createTask(27.60028984,45)
s.createTask(0.17087541,6)
s.createTask(44.63799183,53)
s.createTask(5.56744084,14)
s.createTask(2.80950330,12)
s.createTask(4.55442754,10)
s.createTask(0.25401645,5)
s.createTask(0.20214259,1)"""

"""s.createTask(6.50507251,16)
s.createTask(9.45353670,14)
s.createTask(76.89867961,80)
s.createTask(12.43273304,30)
s.createTask(55.26938306,95)
s.createTask(13.21109156,15)"""

"""s.createTask(2.70325946,35)
s.createTask(29.78090901,38)
s.createTask(21.76381751,50)
s.createTask(37.39450584,100)
s.createTask(32.26606008,44)
s.createTask(6.10069334,17)
s.createTask(0.48156407,1)
s.createTask(0.14656073,11)
s.createTask(0.13385236,1)
s.createTask(0.52891048,1)"""

#<properties hyperperiod="138525482550" utilization="3.76000000" />
"""s.createTask(1.57018889,43)
s.createTask(47.34399758,73)
s.createTask(3.28162553,5)
s.createTask(9.28846873,13)
s.createTask(16.19427835,53)
s.createTask(0.00885172,7)
s.createTask(1.33861849,2)
s.createTask(40.37545285,75)
s.createTask(6.82242319,61)
s.createTask(0.54463354,7)"""

"""s.createTask(7.123547, 18)
s.createTask(7.379277, 12)
s.createTask(145.551818, 184)
s.createTask(13.594508, 37)
s.createTask(12.441299, 15)
s.createTask(48.63833, 97)"""

"""s.createTask(329.288561, 394)
s.createTask(38.521882, 42)
s.createTask(34.533365, 377)
s.createTask(4.259794, 14)
s.createTask(399.42189, 683)
s.createTask(22.813132, 153)
s.createTask(7.889999, 11)"""

"""s.createTask(11, 27)
s.createTask(170.165188, 177)
s.createTask(7.439177, 84)
s.createTask(340.31733, 384)
s.createTask(211.125917, 339)
s.createTask(17.582787, 22)"""

"""s.createTask(2.03646911, 27)
s.createTask(12.13827373, 26)
s.createTask(1.11237785, 2)
s.createTask(0.23060683, 5)
s.createTask(0.07010402, 1)
s.createTask(5.05860607, 59)
s.createTask(0.08621087, 1)
s.createTask(0.11080750, 1)
s.createTask(22.64126689, 55)
s.createTask(1.06532220, 61)
s.createTask(0.02583878, 1)
s.createTask(4.21917542, 27)
s.createTask(0.49495724, 2)
s.createTask(0.04961314, 2)
s.createTask(0.27971904, 1)
s.createTask(18.07321844, 83)
s.createTask(0.59960175, 5)
s.createTask(13.07499436, 16)
s.createTask(0.28233233, 94)
s.createTask(0.07197870, 1)
s.createTask(0.17334764, 6)
s.createTask(0.00614032, 1)
s.createTask(0.06888674, 2)"""

"""s.createTask(39.486501, 42.000000)
s.createTask(143.515088, 177.000000)
s.createTask(190.467064, 315.000000)
s.createTask(57.125724, 97.000000)
s.createTask(42.213681, 76.000000)"""

"""s.createTask(343.961763, 345.000000)
s.createTask(397.389016, 471.000000)
s.createTask(10.016103, 13.000000)
s.createTask(137.218524, 201.000000)
s.createTask(10.007465, 31.000000)
s.createTask(26.771471, 209.000000)
s.createTask(0.607559, 11.000000)"""

"""s.createTask(377.614115, 392.000000)
s.createTask(11.824482, 13.000000)
s.createTask(55.354998, 79.000000)
s.createTask(88.855944, 129.000000)
s.createTask(67.128946, 125.000000)
s.createTask(3.423007, 50.000000)
s.createTask(1.124532, 35.000000)"""

"""s.createTask(0.22550820, 1)
s.createTask(5.05137502, 45)
s.createTask(14.34700132, 44)
s.createTask(0.15103559, 7)
s.createTask(17.38278086, 20)
s.createTask(0.39412191, 1)
s.createTask(1.92383949, 3)
s.createTask(6.31363809, 11)
s.createTask(0.53445461, 11)
s.createTask(53.54997466, 68)"""

"""s.createTask(0.74604242,1)
s.createTask(24.96913034,29)
s.createTask(0.93437238,1)
s.createTask(3.69301198,4)
s.createTask(5.35327708,10)"""


s.allocate()

#print s.partitions()[0].tasks()

#task.Task.implicit(False)
#print s._partition[0]._slices[0]
#s._partition[0]._slices[0]._wcet += 0.0002
#s._partition[0]._slices[0]._deadline += 0.0002
#print s._partition[0]._slices[0]
#for part in s.partitions():
#    l = [task.Task((0, int(1000000*t.wcet()), int(1000000*t.period()), int(1000000*t.deadline()), 0)) for t in part.tasks()]
#    assert part._qpa() and int_qpa.QPA(l)

"""slicenum = 0
mignum = 0
for task in s.tasks():
    found = False
    for part in s.partitions():
        for otherTask in part._tasks:
            if task.number() == otherTask.number():
                found = True
                break
    if not found:
        mignum += 1

totaltasks = sum([len(part.tasks()) for part in s.partitions()])
slicenum = totaltasks - len(s.tasks()) + mignum
print mignum
print slicenum"""
