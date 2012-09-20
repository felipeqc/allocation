import os
import subprocess
import sys
import pickle
import alloc_alg_himemind as himemind

ovfile = open('../data/HIME.ovset', 'r')
overhead = pickle.load(ovfile)
ovfile.close()

# Preemption overheads
ovfile = open('../data/PREEMPTION.ovset', 'r')
preemption = pickle.load(ovfile)
ovfile.close()

# Migration overheads
ovfile = open('../data/L3.ovset', 'r')
l3 = pickle.load(ovfile)
ovfile.close()


wss = 8192
cpmd = max(preemption[wss], l3[wss])

s = himemind.HimeMindTaskSet(4)
s.setVerbose(True)

s.createTask(1.07405014,2)
s.createTask(2.62655436,5)
s.createTask(4.25197068,8)
s.createTask(1.25749268,4)
s.createTask(8.73098010,14)
s.createTask(24.68196289,28)
s.createTask(4.37989001,9)

#<properties hyperperiod="2520" utilization="3.90000000" />
"""s.createTask(1.07405014,2)
s.createTask(2.62655436,5)
s.createTask(4.25197068,8)
s.createTask(1.25749268,4)
s.createTask(8.73098010,14)
s.createTask(24.68196289,28)
s.createTask(4.37989001,9)"""

#<properties hyperperiod="23963940" utilization="3.80000000" />
"""s.createTask(72.79308736,98)
s.createTask(2.03089738,5)
s.createTask(15.41714969,22)
s.createTask(2.97112102,95)
s.createTask(19.32084187,33)
s.createTask(1.48384799,12)
s.createTask(6.06892521,9)
s.createTask(13.92352909,26)"""

"""s.createTask(0.43253311,1)
s.createTask(0.69226585,6)
s.createTask(12.08662332,21)
s.createTask(26.26739903,33)
s.createTask(1.53082864,11)
s.createTask(7.46763640,13)
s.createTask(10.63649574,11)"""

"""s.createTask(2.95533833,3)
s.createTask(5.71001129,8)
s.createTask(4.92044153,7)
s.createTask(0.12417671,2)
s.createTask(2.01080292,6)
s.createTask(6.72695394,7)"""

"""s.createTask(30.25707492,42)
s.createTask(0.68512816,1)
s.createTask(1.94357511,3)
s.createTask(9.93136320,27)
s.createTask(2.43825839,3)
s.createTask(13.98654294,21)"""

#<properties hyperperiod="17100" utilization="3.80000000" />
"""s.createTask(1.66138647,4)
s.createTask(7.37481211,19)
s.createTask(14.00255163,19)
s.createTask(36.91346907,45)
s.createTask(62.93347508,95)
s.createTask(19.41930075,25)"""

#<properties hyperperiod="56168" utilization="3.80000000" />
"""s.createTask(0.63461087,1)
s.createTask(2.34649906,4)
s.createTask(1.46239259,2)
s.createTask(26.15370950,56)
s.createTask(48.94465736,59)
s.createTask(9.36644039,17)"""

"""s.createTask(7000,10000)
s.createTask(7000,10000)
s.createTask(7000,10000)
s.createTask(7000,10000)
s.createTask(4000,7000)"""

#<properties hyperperiod="106020" utilization="3.92000000" />
"""s.createTask(1.37150963,2)
s.createTask(11.81605462,31)
s.createTask(8.59921716,19)
s.createTask(19.46288118,20)
s.createTask(4.96095913,9)
s.createTask(13.14195021,15)"""

#<properties hyperperiod="168" utilization="3.76000000" />
"""s.createTask(2.95533833,3)
s.createTask(5.71001129,8)
s.createTask(4.92044153,7)
s.createTask(0.12417671,2)
s.createTask(2.01080292,6)
s.createTask(6.72695394,7)"""

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

"""s.createTask(0.85306774,7)
s.createTask(1.06001437,3)
s.createTask(7.97919681,9)
s.createTask(1.28873988,3)
s.createTask(10.43418794,35)
s.createTask(50.32264738,51)
s.createTask(0.23334981,1)
s.createTask(17.26124079,25)"""

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
print totaltasks
slicenum = totaltasks - len(s.tasks()) + mignum
print "mig",mignum,"slice",slicenum
