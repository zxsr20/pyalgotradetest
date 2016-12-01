#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import conf,data,process
import data_struct

def process(alldata):
    if alldata.allSegPankous == None :
        alldata.allSegPankous = []
    allSegPankous = alldata.allSegPankous
    allTicks = alldata.allTicks
    cur_tick = allTicks[-1]  #取当前也就是最后一个ticket
    idx = cur_tick.exData.idx  #取下标
    if idx == 0 : return   #如果是第一个tick ， 则无法确定方向
    pre_tick = allTicks[-2] #倒数第二个tick
    
    if len(allSegPankous) == 0: #first seg
        pass
    

        
    
