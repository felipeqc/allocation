import os
import subprocess
import sys
import pickle
import alloc_alg_wm as wm

s = wm.WmTaskSet(5)
s.setVerbose(True)

e = 0.01
k=0.23675
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+2*e,2)
s.createTask(1+k,1.5)
s.createTask(1+k,1.5)

#<properties hyperperiod="106020" utilization="3.92000000" />
"""s.createTask(1.37150963,2)
s.createTask(11.81605462,31)
s.createTask(8.59921716,19)
s.createTask(19.46288118,20)
s.createTask(4.96095913,9)
s.createTask(13.14195021,15)"""

#<properties hyperperiod="375648" utilization="3.84000000" />
"""s.createTask(6.20338824,39)
s.createTask(31.61676459,32)
s.createTask(7.69011993,8)
s.createTask(9.11662875,12)
s.createTask(5.82816626,43)
s.createTask(5.85474446,7)"""

#<properties hyperperiod="70" utilization="3.92000000" />
"""s.createTask(0.89468040,1)
s.createTask(0.20109815,1)
s.createTask(3.06434068,5)
s.createTask(29.96020930,35)
s.createTask(6.23678499,14)
s.createTask(4.54931344,5)"""

# BOM <properties hyperperiod="168" utilization="3.76000000" />
"""s.createTask(2.95533833,3)
s.createTask(5.71001129,8)
s.createTask(4.92044153,7)
s.createTask(0.12417671,2)
s.createTask(2.01080292,6)
s.createTask(6.72695394,7)"""

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

#<properties hyperperiod="510" utilization="3.76000000" />
"""s.createTask(0.03038894,1)
s.createTask(24.11365616,34)
s.createTask(3.38865096,15)
s.createTask(0.89237686,1)
s.createTask(0.97859789,1)
s.createTask(0.69591318,1)
s.createTask(0.20607049,1)
s.createTask(0.06455214,3)"""

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


s.allocate('w', 'p')

#result = True
#for part in s.partitions():
#    result = result and part._qpa()
#assert result
