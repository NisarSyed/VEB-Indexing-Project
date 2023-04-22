#Implementation of Van Emde Boas trees 
import math
from typing import List

class VEBTree(object):
    def __init__(self,u: int) -> None:
        self._u = 2 # u refers to size
        tmp = 2
        while (self._u < u):
            self._u = 2**tmp # should be in powers of 2 because of clusters
            tmp = tmp*2

        self._min = None
        self._max = None 
        self._cluster = {}
        self._summary = None

    def high(self,x: int) -> int:
        return int(x // math.sqrt(self._u))

    def low(self,x: int) -> int:
        return int(x % math.sqrt(self._u))

    def index(self,i: int, j: int) -> int:
        return int(i * math.sqrt(self._u) + j)
    
    def insert(self, x: int) -> None:
        if self._min == None:
            self._min = self._max = x
        else:
            if x < self._min:
                # swap
                self._min, x = x, self._min
            if x > self._max:
                self._max = x
            if self._u > 2:
                
                h = self.high(x)
                l = self.low(x)
                if self._summary == None:
                    self._summary = VEBTree(self.high(self._u))
                if h not in self._cluster:
                    self._cluster[h] = VEBTree(self.high(self._u))
                    
                if self._cluster[h]._min == None:
                    self._summary.insert(h)

                self._cluster[h].insert(l)

    def is_in(self, x: int) -> bool:
        if x == self._min or x == self._max:
            return True
        else:
            if self._u == 2:
                return False
            else:
                h = self.high(x)
                l = self.low(x)
                if h not in self._cluster:
                    return False
                return self._cluster[h].is_in(l)
            
    def __contains__(self, item: int) -> bool:
        return self.is_in(item)

    def successor(self, x:int) -> int:
        if self._u == 2:
            if x==0 and self._max == 1:
                return 1
            else:
                return None
        elif self._min != None and x < self._min:
            return self._min
        else:
            h = self.high(x)
            l = self.low(x)
            i = self.high(x)
            tmp = self._cluster.get(h,None)
            
            if tmp != None and tmp._max != None and l < tmp._max:
                j = self._cluster[h].successor(l)
            else:
                i == None
                if self._summary != None:
                    i = self._summary.successor(h)
                if i == None:
                    return None
                tmp = self._cluster.get(i,None)
                if tmp == None:
                    return None
                j = tmp._min

            if j == None:
                return None
            return self.index(i,j)
        
    def predecessor(self, x:int) -> int:
        if self._u == 2:
            if x == 1 and self._min == 0:
                return 0
            else:
                return None
        elif self._max!= None and x > self._max:
            return self._max
        else:
            h = self.high(x)
            l = self.low(x)
            i = self.high(x)
            j = None

            tmp = self._cluster.get(h,None)
            if tmp != None and tmp._min != None and l > tmp._min:
                
                j = self._cluster[h].predecessor(l)
                    
                return self.index(h,j)
                    
            else:
                
                i = None
                if self._summary != None:
                    i = self._summary.predecessor(h)
                if i == None:
                    if self._min != None and x > self._min:
                        return self._min
                    else:
                        return None
                else:
                    tmp = self._cluster.get(i,None)
                    if tmp == None:
                        return None
                    j = tmp._max
                    if j == None:
                        return None
                    return self.index(i,j)

    def delete(self,x: int) -> None:
        if self._min == self._max:
            self._min = None
            self._max = None
        elif self._u == 2:
            if x == 0:
                self._min = 1
            else:
                self._min = 0
            self._max = self._min
        else:
            if x == self._min:
                h = self.high(self._min)
                l = self.low(self._min)
                tmp = self._cluster.get(h,None)
                if tmp == None:
                    self._min = self._max
                else:
                    self._min = self.index(h,tmp._min)
                x = self._min
            h = self.high(x)
            l = self.low(x)
            self._cluster[h].delete(l)
            if self._cluster[h]._min == None:
                self._summary.delete(h)
                if x == self._max:
                    summary_max = self._summary._max
                    if summary_max == None:
                        self._max = self._min
                    else:
                        self._max = self.index(summary_max,self._cluster[summary_max]._max)
            elif x == self._max:
                self._max = self.index(h,self._cluster[h]._max)

    def search(self, x: int) -> int:
        if self.is_in(x):
            return x
        else:
            return None

    def __str__(self) -> str:
        return "min: " + str(self._min) + " max: " + str(self._max) + " u: " + str(self._u)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    
# # # Test cases 

# def test():
#     veb = VEBTree(16)
#     veb.insert(1)
#     veb.insert(2)
#     veb.insert(3)
#     veb.insert(4)
#     veb.insert(5)
#     veb.insert(1000)

#     print(veb)

#     print(veb.successor(5))
# test()