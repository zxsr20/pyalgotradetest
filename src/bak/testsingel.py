'''
Created on 2015-9-24

@author: Administrator
'''
from tradeanalyze import appconsant
def singleton(cls, *args, **kw):    
    instances = {}    
    def _singleton():    
        if cls not in instances:    
            instances[cls] = cls(*args, **kw)    
        return instances[cls]    
    return _singleton    
  
@singleton    
class MyClass(object):    
    a = 1    
    def __init__(self, x=0):    
        self.x = x    
    
one = MyClass()    
two = MyClass()   

xx=appconsant.getLogger() 
    
two.a = 3    
print one.a    
#3    
print id(one)    
#29660784    
print id(two)    
#29660784    
print one == two    
#True    
print one is two    
#True    
one.x = 1    
print one.x    
#1    
print two.x  