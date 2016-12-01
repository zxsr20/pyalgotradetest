'''
Created on 2015-8-16

@author: ct
'''
from collections import Counter
#include <stdio.h>
#include <stdlib.h>
#define UT 32768
class ap():
    def __init__(self):
        self.key = 0
        self.pos = 0

def comp(ap1,ap2):
    if ap1.key > ap2.key:
        return 1
    elif ap1.key < ap2.key:
        return -1
    else:
        return 0


def rabs(x,n):
    if x>n:
        return x-n
    else:
        return n-x

def most_close_array(array,length,n):
    i=0;k=0
    offset = 10000;
    temp=0
    cumarr = []
    
    for i in range(length):
#         cum = ap()
        if i == 0:
            key = 0 + array[i] 
        else:
            key = cumarr[i-1] + array[i] 
#         cum.key = cumarr[-1]
#         cum.pos = i
        print 'i:'+str(i)+'cum.key'+str(key)
        cumarr.append(key)
    if n<1:
        n = cumarr[-1]*n
    print 'n:'+str(n)
#     cumarr = sorted(cumarr, key=lambda line: line.key)

    for i in range(length):
        print "i:"+str(i)+"key:"+str(cumarr[i])
    i=0
    j=0
    
    for k in range(length):
        for y in range(k,length):
            if k == 0 :
                temp = cumarr[y] - 0 - n;
            else:
                temp = cumarr[y] - cumarr[k-1] - n;
            print 'temp:'+str(temp)+'k:'+str(k)+'y:'+str(y)+'cumarr[y]'+str(cumarr[y])+'cumarr[k]'+str(cumarr[k])
            if temp < offset and temp >= 0:
                offset = temp;
                print 'offset:'+str(temp)
#                 if k == 0:
#                     i = -1
#                 else:
                i = k
                j = y
#     if i == 0 and j == 1:
#         if  cumarr[0] > n:
#             j = 0
                
    print 'i:'+str(i)+'j:'+str(j)
    
#     for k in range(length-2):
#         if  cumarr[k+1].pos > cumarr[k].pos:
#             temp = rabs(cumarr[k+1].key - cumarr[k].key,n)
#             if temp<offset:
#                 print 'temp'+str(temp)
#                 offset = temp;
#                 i = cumarr[k].pos +1
#                 j = cumarr[k+1].pos
#         else:
#             temp = rabs(cumarr[k].key - cumarr[k+1].key,n)
#             if temp<offset:
#                 print 'temp'+str(temp)
#                 offset = temp;
#                 i = cumarr[k+1].pos+1;
#                 j = cumarr[k].pos;
#     print 'i:'+str(i)+'  j:'+str(j)
    return 0;

def countnum():
    priceds = [12,11,12,500,100,200,100,19,15,14,18,19]
#     priceds = sorted(priceds)
#     for n in priceds:
#         print str(n)
    numds = []
    keyds = []
    cnt = Counter(priceds)
    for k,v in cnt.iteritems():
        print k, '-->', v
        keyds.append(k)
        numds.append(v)
        
def countnum1():
#     a = [8.0, 4.0, 4.0, 4.0, 11.0,8.0]
    numds = []
    priceds = [12,11,12,500,100,200,100,19,15,14,18,19]
    dic = {}
    for item in priceds:
        dic[item] = dic.get(item, 0) + 1
    dic = sorted(dic.items())
    for item in dic:
       numds.append(item[1]) 
    print(dic)
    print numds
    
    n = 0.8;
    
    most_close_array(numds,len(numds),n)
    
    

def mymost_close_array(array,length,n):
    
    cumarr = []
    
    for i in range(length):
#         cum = ap()
        if i == 0:
            key = 0 + array[i] 
        else:
            key = cumarr[i-1] + array[i] 
#         cum.key = cumarr[-1]
#         cum.pos = i
        print 'i:'+str(i)+'cum.key'+str(key)
        cumarr.append(key)
    if n<1:
        n = cumarr[-1]*n
    
    i = -1
    k = length -1
    a = False
    b = False
    while True:
        if a==False:
            i=i+1
            if cumarr[k] - cumarr[i] < n:
                a = True
                i = i-1
        if b==False:
            k=k-1
            if cumarr[k] - cumarr[i] < n:
#                 k = k+1
                b = True
                k = k+1
        if a==True and b==True:
            break        
    
    
    
    print 'i:'+str(i)+'k:'+str(k)
    print array[i+1:k+1]

if __name__=="__main__": 
#     countnum1()
#     n = 29;
#     a = [2,4,8,16,32,64,128,256]
#     most_close_array(a,len(a),n)
    n = 0.8;
#     a = [2,1,1,1,2,1,3,1,2,1,3,1,4,1,1,5,4]
    
    a = [1,1,1,1,1,1,1,1,1,1]
    mymost_close_array(a,len(a),n)
    

