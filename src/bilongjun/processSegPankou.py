#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import conf,data,process
import data_struct
from data_struct import *

def process(alldata):
    if alldata.allSegPankous == None :
        alldata.allSegPankous = []
    allSegPankous = alldata.allSegPankous
    allTicks = alldata.allTicks
    cur_tick = allTicks[-1]
    idx1 = cur_tick.exData.idx
    if idx1 == 0 :
        return   #如果是第一个tick ， 则无法确定方向
    pre_tick = allTicks[-2] #倒数第二个tick
    idx2=pre_tick.exData.idx

#我分了三个方向，1表示涨，-1表示下跌。如果一波趋势没结束，在此期间的tick_idx_start都一样，tick_idx_end我都赋为0。
    oneSegPankou = CSegPankou()
    if idx1 == 1: #如果是第二个ticket
        if cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']>pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1 #如果目前的申卖价除于申买价高于前一个的，就把盘口开始设为idx1
            oneSegPankou.tick_idx_start = idx1
            oneSegPankou.tick_idx_end = 0
            oneSegPankou.dir=1
        elif cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']==pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1   #如果目前的申卖价除于申买价等于前一个的，就把盘口开始设为idx1，说明是降
            oneSegPankou.tick_idx_start = idx1
            oneSegPankou.tick_idx_end = 0
            oneSegPankou.dir=0
        else:
            oneSegPankou.idx=idx1
            oneSegPankou.tick_idx_start = idx1
            oneSegPankou.tick_idx_end = 0
            oneSegPankou.dir=-1
            
        allSegPankous.append(oneSegPankou)
            
        
    if allSegPankous[-1].dir == 1:   
        if cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']>pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1
            oneSegPankou.tick_idx_start =allSegPankous[-1].tick_idx_start
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=1
        elif cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']==pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1
            allSegPankous[-1].tick_idx_end=idx2
            oneSegPankou.tick_idx_start =idx2
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=0
        else:
            oneSegPankou.idx=idx1
            allSegPankous[-1].tick_idx_end=idx2
            oneSegPankou.tick_idx_start =idx2
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=-1
            
        allSegPankous.append(oneSegPankou)

            
    if allSegPankous[-1].dir==-1:   
        if cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']>pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1
            allSegPankous[-1].tick_idx_end=idx2
            oneSegPankou.tick_idx_start =idx2
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=1
        elif cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']==pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1
            allSegPankous[-1].tick_idx_end=idx2
            oneSegPankou.tick_idx_start =idx2
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=0
        else:
            oneSegPankou.idx=idx1
            oneSegPankou.tick_idx_start = allSegPankous[-1].tick_idx_start
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=-1
            
        allSegPankous.append(oneSegPankou)

            
    if alldata.allSegPankous[-1].dir==0: 
        if cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']>pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1
            allSegPankous[-1].tick_idx_end=idx2
            oneSegPankou.tick_idx_start =idx2
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=1
        elif cur_tick.OneTickDic_normalizations()['AskPrice1']/cur_tick.OneTickDic_normalizations()['BidPrice1']==pre_tick.OneTickDic_normalizations()['AskPrice1']/pre_tick.OneTickDic_normalizations()['BidPrice1']:
            oneSegPankou.idx=idx1
            oneSegPankou.tick_idx_start = allSegPankous[-1].tick_idx_start
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=0
        else:
            oneSegPankou.idx=idx1
            allSegPankous[-1].tick_idx_end=idx2
            oneSegPankou.tick_idx_start =idx2
            oneSegPankou.tick_idx_end=0
            oneSegPankou.dir=-1
            
        allSegPankous.append(oneSegPankou)

    alldata.allSegPankous=allSegPankous
    
