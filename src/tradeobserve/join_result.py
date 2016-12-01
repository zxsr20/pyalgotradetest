#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from tradeobserve import basic_marketdata, order_data
import new
import csv
import time
import sys
from __builtin__ import int
class joindata():
    def __init__(self):
        self.DepthMarketDataField = None   #data.py
        self.OrderField = None #计算
        self.time = ''
        
        
        
def join(InstrumentID):
        
    joindatas = []
        
    basic_marketdatadir = 'D:\\pyTest_yh\\basicdata\\data.20150617.zip'
    bl = basic_marketdata.getDayData(InstrumentID,basic_marketdatadir)  
    
    order_datadir = 'D:\\pyTest_yh\\basicdata\\orderdata.zip'
    ol = order_data.getDayData(InstrumentID,order_datadir)
    
    f=0
    for i in bl:
        for b in ol:
            if f<100 and i.timestamp[0] > 1434524502000000:
                print str(int(i.timestamp[0]))+'  '+str(int(b.timestamp))
                f+=1
            if i.timestamp[0] == b.timestamp:
                j=joindata()
                j.DepthMarketDataField = i
                j.OrderField = b
                x = time.localtime(i.timestamp/1000000)
                t = time.strftime('%Y-%m-%d %H:%M:%S',x)
                j.time = t
                joindatas += [j] #把该dmd数据放进数组去
                
    #把需要的字段写到csv中
    writer = csv.writer(file('ting1.csv', 'wb'))
     
    writer.writerow(['时间戳','交易日', '最新价', '数量','成交金额','申买价一','申买量一','申卖价一','申卖量一','order交易日', '报单编号', '客户代码','交易用户代码','合约代码','报单价格条件','买卖方向','组合开平标志','组合投机套保标志','价格','数量','有效期类型','报单状态','今成交数量','剩余数量'])
    
    for j in joindatas:
        marketdata = j.DepthMarketDataField
        orderdata = j.OrderField
        writer.writerow([j.time,str(marketdata.TradingDay),str(marketdata.LastPrice),str(marketdata.Volume),str(marketdata.Turnover),str(marketdata.OpenInterest),str(marketdata.BidPrice1),str(marketdata.BidVolume1),str(marketdata.AskPrice1),str(marketdata.AskVolume1),str(orderdata.TradingDay),str(orderdata.OrderSysID),str(orderdata.ClientID),str(orderdata.UserID),str(orderdata.InstrumentID),str(orderdata.OrderPriceType),str(orderdata.Direction),str(orderdata.CombOffsetFlag),str(orderdata.CombHedgeFlag),str(orderdata.LimitPrice),str(orderdata.VolumeTotalOriginal),str(orderdata.TimeCondition),str(orderdata.OrderStatus),str(orderdata.VolumeTraded),str(orderdata.VolumeTotal)])
    

def longToInt(value):
    if value > 2147483647 :
        return (value & (2 ** 31 - 1))
    else :
        return value
    
if __name__=="__main__":
    join('IF1507')
    print 'finish'                   
                    
            
        
        