#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import data
import data_struct
from data_struct import *
import processSegPankou

def process(data_lines,data_config):
    pre_vol = 0;pre_oi = 0;pre_ot = 0 #ot:ontickturnover
    idx = 0;

    
    AllData = CAllData()
    AllData.conf = data_config #都是对单个品种，合约乘数及最小变动
    AllData.allTicks = []     #都是对单个品种，tick数据
    AllData.allSegPankous = []#都是对单个品种，盘口数据
    oneSegPankou = CSegPankou()
    agv_pricelist=[]
    for line in data_lines:
        diff_vol = line.Volume - pre_vol
        pre_vol = line.Volume
        diff_OpenInterest = line.OpenInterest - pre_oi
        pre_oi = line.OpenInterest
        diff_ot = line.Turnover - pre_ot
        pre_ot = line.Turnover
        oneTick = COneTick()
        oneTick.dmd = line 
        oneTick.exData = CExData() #当前tick 的变化量
        oneTick.exData.vol = diff_vol
        oneTick.exData.DiffOpenInterest = diff_OpenInterest
        oneTick.exData.OneTurnover = diff_ot

        if oneTick.exData.vol == 0:
            oneTick.exData.avg_pri = 0 
        else :
            oneTick.exData.avg_pri = oneTick.exData.OneTurnover / oneTick.exData.vol / (data_config.PriceTick * data_config.VolumeMultiple)
        oneTick.exData.idx = idx
        idx += 1
        AllData.allTicks += [oneTick]
        
        processSegPankou.process(AllData)
 
        #print oneTick.dump()
        #print oneTick.OneTickDic_normalizations()
    return AllData
    


if __name__=="__main__":
    instrumentID = "IF1412"
    date = "20141119"
    data_lines = data.getDayData(date, instrumentID) #获取数据
    data_config = conf.getInstrumentInfo(instrumentID)
    a=process(data_lines,data_config)
