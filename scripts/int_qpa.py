#-*- coding: latin1 -*-
__author__ = "José Augusto (jamjunior@ufba.br)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/12/24 18:53:59 $"

import math
import fractions
from task import Task


C_i = lambda task: task.C()
T_i = lambda task: task.T()
D_i = lambda task: task.D()
U_i = lambda task: float(task.C())/task.T()
GAP = 1

Sum = lambda S,f: math.fsum(f(x) for x in S)
U = lambda Gamma: Sum(Gamma, lambda tau: U_i(tau))

def La(Gamma):
    Fa = lambda tau: (T_i(tau)-D_i(tau))*U_i(tau)    
    tmp = D_i(max(Gamma, key = lambda tau: D_i(tau)-T_i(tau)))

    #print "La=",max(tmp, Sum(Gamma, lambda tau: Fa(tau))/(1-U(Gamma)) ) #test
    return math.ceil(max(tmp, Sum(Gamma, lambda tau: Fa(tau))/(1-U(Gamma)) )) #max(tmp, Sum(Gamma, lambda tau: Fa(tau))/(1-U(Gamma)) )

def Lb(Gamma):
    Fb = lambda tau, w: math.ceil(w/T_i(tau))*C_i(tau)    
    w_0 = Sum(Gamma, lambda tau: C_i(tau))
    w_m = Sum(Gamma, lambda tau: Fb(tau, w_0))
    while w_0 != w_m:
        w_0 = w_m
        w_m = Sum(Gamma, lambda tau: Fb(tau, w_m))

    #print "Lb=",w_m #test
    return w_m

def L(Gamma):
    aux = Lb(Gamma) 
    return min(La(Gamma), aux) if U(Gamma) <1 else aux

def h(Gamma, t):
    Fh = lambda tau: max(0, math.floor((T_i(tau)+t-D_i(tau))/T_i(tau)) )*C_i(tau)
    return Sum(Gamma, lambda tau: Fh(tau))


            
def maxDi(Gamma,t):
    dmax = 0
    for tau in Gamma:
        if D_i(tau)<t:
            dj = math.floor((t-D_i(tau))/T_i(tau))*T_i(tau) + D_i(tau)
            if dj == t: dj = dj - T_i(tau)
            if dj > dmax: dmax = dj

    #print "d_max=",dmax #test
    return dmax

            
def QPA(Gamma):
    if U(Gamma)>1: return False #jamsjr
    elif not Gamma: return True
    
    D_min = D_i(min(Gamma, key = lambda tau: D_i(tau)))   
    t =  maxDi(Gamma,L(Gamma))
    tmp = h(Gamma, t)
    #print "d_max=",t ,"d_min=",D_min #test
    #print "t=",t, "h(t)=",tmp #test
    while (tmp <= t and tmp > D_min):
        t = tmp if tmp<t else maxDi(Gamma,t)
        tmp = h(Gamma, t)

        #print "t=",t, "h(t)=",h(Gamma, t) #test
        
    return True if (tmp <= D_min) else False





if __name__ == '__main__':
    import sys
    Task.implicit(False)


##    print "QPA1 unsched"
##    gamma = [Task((0.0, 6000, 31000, 18000, 0.0)),
##             Task((0.0, 2000, 9800, 9000, 0.0)),
##             Task((0.0, 1000, 17000, 12000, 0.0)),
##             Task((0.0, 90, 4200, 3000, 0.0)),
##             Task((0.0, 8, 96, 10, 0.0)),
##             Task((0.0, 2, 12, 16, 0.0)),
##             Task((0.0, 10, 280, 19, 0.0)),
##             Task((0.0, 26, 660, 160, 0.0))
##             ]   
##    print QPA(gamma)
##
##    print "QPA2 sched"  
##    gamma = [Task((0.0, 6000, 31000, 18000, 0.0)),
##             Task((0.0, 2000, 9800, 9000, 0.0)),
##             Task((0.0, 1000, 17000, 12000, 0.0)),
##             Task((0.0, 90, 4200, 3000, 0.0)),
##             Task((0.0, 8, 96, 78, 0.0)),
##             Task((0.0, 2, 12, 16, 0.0)),
##             Task((0.0, 10, 280, 120, 0.0)),
##             Task((0.0, 26, 660, 160, 0.0))
##             ]   
##    print QPA(gamma)
##
##
##
##

##    print "QPA4 sched"  
##    gamma = [Task((0.0, 8, 60, 11, 0.0)),
##             Task((0.0, 12, 170, 20, 0.0)),
##             Task((0.0, 6, 120, 26, 0.0)),
##             Task((0.0, 7, 110, 80, 0.0))
##             ]   
##    print QPA(gamma)
##    
##    print "QPA5 unsched"  
##    gamma = [Task((0.0, 8, 60, 10, 0.0)),
##             Task((0.0, 12, 170, 19, 0.0)),
##             Task((0.0, 10, 210, 30, 0.0)),
##             Task((0.0, 6, 190, 36, 0.0)),
##             Task((0.0, 8, 280, 70, 0.0)),
##             Task((0.0, 7, 320, 90, 0.0))
##             ]   
##    print QPA(gamma)



##
##
##
##
##    print "QPA1 unshed"
##    gamma = [Task((0.0, 10, 30, 30, 0.0)),Task((0.0, 13, 20, 13, 0.0))]
##    print QPA(gamma)
##
##    print "QPA2 unshed"
##    gamma = [Task((0.0, 100, 300, 300, 0.0)),Task((0.0, 130, 200, 130, 0.0))]
##    print QPA(gamma)
##    
##    print "QPA3 shed"    
##    gamma = [Task((0.0, 1, 2, 1, 0.0)), Task((0.0, 1, 3, 3, 0.0))]    
##    print QPA(gamma)
##
##    print "QPA4 unshed"    
##    gamma = [Task((0.0, 11, 20, 11, 0.0)), Task((0.0, 10, 30, 30, 0.0))]    
##    print QPA(gamma)
##
##
    print "QPA5 unshed"    
    gamma = [Task((0.0, 10, 20, 10, 0.0)), Task((0.0, 11, 30, 30, 0.0))]    
    print QPA(gamma)


    print "QPA4 unshed"    
    gamma = [Task((0.0, 1, 2, 1, 0.0)), Task((0.0, 2, 4, 4, 0.0))]    
    print QPA(gamma)

    """CPU 0, U = 0.999900:
- Task 4, C = 1946.000000, T = 2000.000000, U = 0.973000
- Slice 1:1, C = 5.380000, D = 5.380000, 
		T = 200.000000, U = 0.026900

CPU 1, U = 0.992250:
- Task 6, C = 1314.000000, T = 1500.000000, U = 0.876000
- Slice 1:2, C = 23.250000, D = 23.250000, 
		T = 200.000000, U = 0.116250

CPU 2, U = 0.999757:
- Task 5, C = 496.000000, T = 900.000000, U = 0.551111
- Task 2, C = 1181.000000, T = 3100.000000, U = 0.380968
- Slice 1:3, C = 13.535714, D = 13.535714, 
		T = 200.000000, U = 0.067679

CPU 3, U = 0.926277:
- Task 3, C = 859.000000, T = 1900.000000, U = 0.452105
- Slice 1:4, C = 94.834286, D = 157.834286, 
		T = 200.000000, U = 0.474171"""


    print "QPA novo"    
    gamma = [Task((0, 194600,200000, 200000, 0)), Task((0, 538,20000, 538, 0))]
    print QPA(gamma)
    gamma = [Task((0, 131400,150000, 150000, 0)), Task((0, 2325,20000, 2325, 0))]
    print QPA(gamma)
    gamma = [Task((0, 496000000,900000000, 900000000, 0)), Task((0, 1181000000,3100000000, 3100000000, 0)), Task((0, 13535714,200000000, 13535714, 0))]
    print QPA(gamma)
    gamma = [Task((0, 859000000,1900000000, 1900000000, 0)), Task((0, 94834286,200000000, 157834286, 0))]
    print QPA(gamma)


##
##
##    print "QPA5 unshed"    
##    gamma = [Task((0.0, 110, 200, 110, 0.0)), Task((0.0, 100, 300, 300, 0.0))]    
##    print QPA(gamma)




