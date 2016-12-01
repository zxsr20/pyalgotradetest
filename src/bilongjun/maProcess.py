#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import data
from data_struct import *

def maprocess(data_lines,data_config,malength=60):
    idx = 0;
    AllData = CAllData()
    AllData.conf = data_config
    AllData.allTicks = []
    agv_pricelist=[]
    for line in data_lines:
        oneTick = COneTick()
        oneTick.dmd = line
        oneTick.exData = CExData()

        if(idx<=malength):
            oneTick.exData.avg_price =0.0;
            agv_pricelist.append(oneTick.dmd.LastPrice)
        else: 
            del agv_pricelist[0]
            agv_pricelist.append(oneTick.dmd.LastPrice)
            oneTick.exData.avg_price =sum(agv_pricelist)/malength

        AllData.allTicks += [oneTick]
        
        idx += 1

    return AllData

if __name__=="__main__":
    instrumentID = "IF1412"
    date = "20141119"
    data_path = "F:\Python\intership\data"
    data_lines = data.getDayData(date, instrumentID,data_path) #获取数据
    data_config = conf.getInstrumentInfo(instrumentID)
    a=maprocess(data_lines,data_config)
