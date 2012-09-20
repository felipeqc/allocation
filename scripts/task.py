# -*- coding: latin1 -*-
"""Class task"""

__author__ = "José Augusto (jamjunior@ufba.br)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/12/24 18:53:59 $"

class Task(object):
    count = 0
    implicit = True

    @classmethod
    def inc(cls):
        cls.count += 1
        return cls.count
    
    @classmethod
    def implicit(cls, cond):
        cls.implicit = cond
        

    @classmethod
    def clear(cls):
        cls.count = 0
    
    def __init__(self, data):
        """
        Inicializador da classe
        """
        
        self._id = self.inc()
        self._r = float(data[0])
        self._C = float(data[1])
        self._T = float(data[2])
        self._D = float(data[3])
        self._mi = float(data[4])
    
    def __done__(self):
        """
        Destrutor da classe
        """
        self._id = 0
        self._r = 0.0
        self._C = 0.0
        self._T = 0.0
        self._D = 0.0
 
    def id(self):
        """
        ID of task 
        """
        return self._id


    def D(self):
        """
        Relative deadline of task 
        """
        return self.T() if self.implicit else self._D
        
    def T(self):
        """
        Minimum inter-arrival time of task
        """
        return self._T 
    
    def C(self):
        """
        Worst-case execution time of task 
        """
        return self._C
    
    def r(self):
        """
        Release time of task 
        """ 
        return self._r

    def mi(self):
        """
        Migration of task 
        """ 
        return self._mi
        
    def utilisation(self):
        """
        Utilisation of task
        """ 
        return self.C()/self.T()
        
    def density(self):
        """
        Density of task
        """ 
        return self.C()/min(self.T(),self.D())
    
    def A(self):
        """
        min(T,D)
        """ 
        return min(self.T(),self.D())
    
    
    def __repr__(self):
        return "Task-" + str(self.id()) + ":(" + str(self.r()) + ", " + str(self.C()) + ", " + str(self.T()) + ", " + str(self.D()) + ", " + str(self.mi()) + ")"
    

if __name__ == '__main__':
    import sys    
    task = Task((7, 5, 3, 2, 9))
    task = Task((7, 5, 3, 2, 9))
    print task  
    print "utilisation:" + str(task.utilisation()) + " density:" + str(task.density())



