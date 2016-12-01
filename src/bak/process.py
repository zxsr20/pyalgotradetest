#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import data_struct
from data_struct import *
import processSegPankou


def process(data_lines,data_config,malength=60):
    pre_vol = 0;pre_oi = 0;pre_ot = 0 #ot:ontickturnover
    idx = 0;
    resdic={}
    AllData = CAllData()
    AllData.conf = data_config
    AllData.allTicks = []
    AllData.allSegPankous = []
    agv_pricelist=[]
    for line in data_lines:
        diff_vol = line.Volume - pre_vol  #数量减去上一次数量
        pre_vol = line.Volume
        diff_OpenInterest = line.OpenInterest - pre_oi  #持仓量减去上一次数量
        pre_oi = line.OpenInterest
        diff_ot = line.Turnover - pre_ot #成交金额减去上一次金额
        pre_ot = line.Turnover
        oneTick = COneTick(malength)  #定义一个oneticket
        oneTick.dmd = line 
        oneTick.exData = CExData() #初始化 当前tick 的变化量
        oneTick.exData.vol = diff_vol #把变化量放进去
        oneTick.exData.DiffOpenInterest = diff_OpenInterest
        oneTick.exData.OneTurnover = diff_ot

        if(idx<=malength):
            oneTick.exData.avg_price =0.0;
            agv_pricelist.append(oneTick.dmd.LastPrice)  #把最新价放到数组中
        else: 
            del agv_pricelist[0] #如果idx大于最大值，删除最新价数组的第一位
            agv_pricelist.append(oneTick.dmd.LastPrice)
            oneTick.exData.avg_price =sum(agv_pricelist)/malength #求出maxlength中的平均价

        if oneTick.exData.vol == 0: oneTick.exData.avg_pri = 0 ;
        else :oneTick.exData.avg_pri = oneTick.exData.OneTurnover / oneTick.exData.vol / (data_config.PriceTick * data_config.VolumeMultiple) / 5 #成交金额除于树木除于最小变动价和合约乘积的乘得出均价一笔
        oneTick.exData.idx = idx #赋予下标
        #去重和去掉错误的数据后，计算出每一个tick的平均价格，放入csv中
        
        

        AllData.allTicks += [oneTick] #
#         processSegPankou.process(AllData)
        #print oneTick.dump()
#         resdic[idx]=oneTick.OneTickDic()
        #返回归一化结果
        #resdic[idx]=oneTick.OneTickDic_normalizations() 
        idx += 1
    return resdic

def TimeSeries(inputdic): #输入以idx为键的字典,输出以时间为键的字典
    resdic={}
    for x in inputdic.keys():
        resdic[inputdic[x]['UpdateTime'][0:8]+'_'+inputdic[x]['UpdateMillisec']]=inputdic[x]
    return resdic

def MerageTimeSeries(dic1,dic2): #dic1为相对不活跃，dic2为相对活跃
    res=[]
    for x in dic1.keys():
        if(dic1[x]['vol']>0 and x in dic2.keys()):
            res.append([x,dic1[x]['LastPrice']-dic2[x]['LastPrice']])
    return res


#主要是处理数据，主要是这个函数获得盘口处理的数据
