#!/usr/bin/python
#-*- coding=utf-8 -*-
'''
Created on 2015-7-19

@author: ct
'''
import sys,os
import conf,data
import itertools
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed
from tradeanalyze import appconsant
import data_struct
from data_struct import *
import csv
from  datetime  import  * 

def main():
    
    rootdir = 'D:\pyTest_yh\data\\'
     
    instrumentID1 = "m1509"
    instrumentID2 = "m1601"
    c_instrumentID = "SP m1509&m1601"
#     instrumentID = "rb1510"
    date = "20150720"
    
    for f in os.listdir(rootdir):  
        ff = os.path.join(rootdir, f)  
        filename = ff.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(ff) and filename == date:   
            print '原始文件:'+ff
            data_lines1 = data.getDayData(instrumentID1,ff) #获取数据
            data_config1 = conf.getInstrumentInfo(instrumentID1) 
            
            data_lines2 = data.getDayData(instrumentID2,ff) #获取数据
            data_config2 = conf.getInstrumentInfo(instrumentID2) 
            
            data_lines3 = data.getDayData(c_instrumentID,ff) #获取数据
            data_config3 = conf.getInstrumentInfo(c_instrumentID) 
             
    print str(len(data_lines1))+'  '+str(len(data_lines2))+str(len(data_lines3))     
            #先去重和时间标准化
            #去重并保存到csv
    a=''
    c=[]
    for line in data_lines1:
        
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
#             line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec):
#             print str(i.TradingDay)+' '+str(i.UpdateTime)[0:8]+'.'+str(i.UpdateMillisec)
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
            c.append(line)
#             data_lines1.remove(line)
#         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec) 
    
    for line in c:
        data_lines1.remove(line)
    a=''
    c=[]
    for line in data_lines2:
        
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
#             line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec):
#             print str(i.TradingDay)+' '+str(i.UpdateTime)[0:8]+'.'+str(i.UpdateMillisec)
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
            c.append(line)
#             data_lines2.remove(line)
        
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
    for line in c:
        data_lines2.remove(line)
    
    
    
     
    a=''
    c=[]
    for line in data_lines3:
#         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])  
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec):
#             print str(i.TradingDay)+' '+str(i.UpdateTime)[0:8]+'.'+str(i.UpdateMillisec)
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
            c.append(line)
#             data_lines2.remove(line)
        
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
    for line in c:
        data_lines3.remove(line)      
    
    print str(len(data_lines1))+'  '+str(len(data_lines2))+'  '+str(len(data_lines3))
    
    
    diff_list = []
#     i = 0
#     
#     print str(len(data_lines1))+'  '+str(len(data_lines2))
# #     if len(data_lines1) == len(data_lines2):
# #         print '数组不对应，执行中断'    
# 
    heti = []
    index1 = 0
    index2 = 0
    x=0
    lines1 = []
    lines2 = []
    while True:
        if index1 >= len(data_lines1) or index2 >= len(data_lines2):break
        line1 = data_lines1[index1]
        line2 = data_lines2[index2]
        time_line1 = datetime.strptime(line1.UpdateTime[0:8]+' '+str(line1.UpdateMillisec*1000),"%H:%M:%S %f")
        time_line2 = datetime.strptime(line2.UpdateTime[0:8]+' '+str(line2.UpdateMillisec*1000),"%H:%M:%S %f")
        if(time_line2 >= time_line1):
            d = time_line2-time_line1
        else:
            d = time_line1-time_line2
        if d.seconds == 0 and d.microseconds < 300000:
            x += 1
            lines1.append(line1)
            lines2.append(line2)
            print 'line1:'+str(line1.UpdateTime)[0:8]+'.'+str(line1.UpdateMillisec)+'line2:'+str(line2.UpdateTime)[0:8]+'.'+str(line2.UpdateMillisec)
            index1 += 1
            index2 += 1
        elif time_line1 > time_line2:
            index2 += 1
        elif time_line1 < time_line2:
            index1 += 1
#             
#             
#     
#             
#     
#     
# 
    pre_vol1 = 0;pre_ot1 = 0;avg_pri1 = 0
    pre_vol2 = 0;pre_ot2 = 0;avg_pri2 = 0
    #价格归一，相减然后保存差值
    i = 0
    for line1 in lines1:
        diff = diffinfo()
         
        line2 = lines2[i]
         
        diff.__dateTime1 = str(line1.UpdateTime)[0:8]+' '+str(line1.UpdateMillisec)
        diff.__dateTime2 = str(line2.UpdateTime)[0:8]+' '+str(line2.UpdateMillisec)
        diff.__dateTime = str(line1.TradingDay)+' '+str(line1.UpdateTime)[0:8]+'.'+str(line1.UpdateMillisec)
        diff_vol1 = line1.Volume - pre_vol1  
        pre_vol1 = line1.Volume
         
        diff_ot1 = line1.Turnover - pre_ot1 
        pre_ot1 = line1.Turnover
     
        if diff_vol1 == 0: 
            avg_pri1 = avg_pri1+0#没有成交的话就取上一个值
        else :
#             print "diff_ot:"+str(diff_ot1)+"diff_vol:"+str(diff_vol1)+"data_config.PriceTick:"+str(data_config1.PriceTick)+"data_config.VolumeMultiple:"+str(data_config1.VolumeMultiple)
             
            avg_pri1 = diff_ot1/diff_vol1/ (data_config1.PriceTick * data_config1.VolumeMultiple)
             
         
        diff_vol2 = line2.Volume - pre_vol2
        pre_vol2 = line2.Volume
         
        diff_ot2 = line2.Turnover - pre_ot2 
        pre_ot2 = line2.Turnover
     
        if diff_vol2 == 0: 
            avg_pri2 = avg_pri2+0#没有成交的话就取上一个值
        else :
#             print "diff_ot:"+str(diff_ot2)+"diff_vol:"+str(diff_vol2)+"data_config.PriceTick:"+str(data_config2.PriceTick)+"data_config.VolumeMultiple:"+str(data_config2.VolumeMultiple)
             
            avg_pri2 = diff_ot2/diff_vol2/ (data_config2.PriceTick * data_config2.VolumeMultiple)
         
        diff.__avgprice = avg_pri1 - avg_pri2
         
        try:
            newbidprice1 = int(round(line1.BidPrice1/data_config1.PriceTick))
        except OverflowError:
            print 'OverflowError BidPrice1:'+str(line1.BidPrice1) +str('avg_pri:'+str(avg_pri1))
            newbidprice1 = 0
             
        try:
            newbidprice2 = int(round(line2.BidPrice1/data_config2.PriceTick))
        except OverflowError:
            print 'OverflowError BidPrice1:'+str(line2.BidPrice1) +str('avg_pri:'+str(avg_pri2))
            newbidprice2 = 0
             
        diff.__bidprice = newbidprice1 - newbidprice2
             
        try:
            newlastprice1 = round(line1.LastPrice/data_config1.PriceTick,3)
        except OverflowError:
            print 'OverflowError LastPrice:'+str(line1.LastPrice) +str('avg_pri:'+str(avg_pri1))
            newlastprice1 = 0
             
        try:
            newlastprice2 = round(line2.LastPrice/data_config2.PriceTick,3)
        except OverflowError:
            print 'OverflowError LastPrice:'+str(line2.LastPrice) +str('avg_pri:'+str(avg_pri2))
            newlastprice2 = 0
             
        diff.__lastprice = newlastprice1 - newlastprice2
             
        try:
    #                 newaskprice = int(round(line.AskPrice1*5))
            newaskprice1 = int(round(line1.AskPrice1/data_config1.PriceTick))
        except OverflowError:
            print 'OverflowError AskPrice1:'+str(line1.AskPrice1) +str('avg_pri:'+str(avg_pri1))
            newaskprice1 = 0
             
        try:
    #                 newaskprice = int(round(line.AskPrice1*5))
            newaskprice2 = int(round(line2.AskPrice1/data_config2.PriceTick))
        except OverflowError:
            print 'OverflowError AskPrice1:'+str(line2.AskPrice1) +str('avg_pri:'+str(avg_pri2))
            newaskprice2 = 0
             
        diff.__askprice = newaskprice1 - newaskprice2
        
        diff.__lBidrAsk = newbidprice1 - newaskprice2
        diff.__lAskrBid = newaskprice1 - newbidprice2
 
        diff_list.append(diff)
        i+=1
        
#     for diff in diff_list:
#         print diff.__dateTime1+' '+str(diff.__lastprice)+' '+str(diff.__askprice)+' '+str(diff.__bidprice)+' '+str(diff.__avgprice)
    
    all_list = data_lines1 + data_lines2 + data_lines3
    all_list = sorted(all_list, key=lambda line: line.UpdateTime[0:8]+' '+str(line.UpdateMillisec*1000))
#     for line in all_list:
#         printLine(line)

    filename = 'diff'+instrumentID1+instrumentID2+'.csv'
    writer = csv.writer(file(filename, 'wb'))
     
    writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close','bidvol','askvol'])
    for line in diff_list:
        writer.writerow([line.__dateTime,str(line.__bidprice),str(line.__lastprice),str(line.__avgprice),str(line.__askprice),0,str(line.__avgprice),0,0])

        
#     index1 = 0
#     index2 = 0
#     line1 = diff_list[index1]
#     line2 = all_list[index2]
#     
#     time_line1 = datetime.strptime(line1.__dateTime1,"%H:%M:%S %f")
#     time_line2 = datetime.strptime(line2.UpdateTime[0:8]+' '+str(line2.UpdateMillisec*1000),"%H:%M:%S %f")
#     while True:
#         if index1 >= len(diff_list) and index2 >= len(all_list):break
#         print str(index1)+' '+str(index2)
# #         print str(time_line1)+' '+str(time_line2)+' '+str(time_line3)
#         
#         if index2 < len(all_list) and (time_line2 <= time_line1 or index1 >= len(diff_list)):       
#             printLine(line2)
#             index2 += 1
#             if index2 < len(all_list):
#                 line2 = all_list[index2]
#                 time_line2 = datetime.strptime(line2.UpdateTime[0:8]+' '+str(line2.UpdateMillisec*1000),"%H:%M:%S %f")
#         
#         elif index1 < len(diff_list) and (time_line1 <= time_line2 or index2 >= len(all_list)) :
#             print >>appconsant.testfile,'diff:'+line1.__dateTime1+' '+str(line1.__lastprice)+' '+str(line1.__askprice)+' '+str(line1.__bidprice)+' '+str(line1.__avgprice)+' lAskrBid:'+str(line1.__lAskrBid)+ ' lBidrAsk:'+str(line1.__lBidrAsk)
#             index1 += 1
#             if index1 < len(diff_list):
#                 line1 = diff_list[index1]
#                 time_line1 = datetime.strptime(line1.__dateTime1,"%H:%M:%S %f")
    
#     index1 = 0
#     index2 = 0
#     index3 = 0
#     line1 = data_lines1[index1]
#     line2 = data_lines2[index2]
#     line3 = data_lines3[index3]
#     time_line1 = datetime.strptime(line1.UpdateTime[0:8]+' '+str(line1.UpdateMillisec*1000),"%H:%M:%S %f")
#     time_line2 = datetime.strptime(line2.UpdateTime[0:8]+' '+str(line2.UpdateMillisec*1000),"%H:%M:%S %f")
#     time_line3 = datetime.strptime(line3.UpdateTime[0:8]+' '+str(line3.UpdateMillisec*1000),"%H:%M:%S %f")
#     while True:
#         if index1 >= len(data_lines1) and index2 >= len(data_lines2) and index3 >= len(data_lines3):break
#         print str(index1)+' '+str(index2)+' '+str(index3)
#         print str(line3.InstrumentID)
# #         print str(time_line1)+' '+str(time_line2)+' '+str(time_line3)
#         if index1 < len(data_lines1):
#             if (time_line1 <= time_line2 or index2 >= len(data_lines2)) and (time_line1 <= time_line3 or index3 >= len(data_lines3)):
#                 printLine(line1)
#                 index1 += 1
#                 if index1 < len(data_lines1):
#                     line1 = data_lines1[index1]
#                     time_line1 = datetime.strptime(line1.UpdateTime[0:8]+' '+str(line1.UpdateMillisec*1000),"%H:%M:%S %f")
#         if index2 < len(data_lines2):       
#             if (time_line2 <= time_line1 or index1 >= len(data_lines1)) and (time_line2 <= time_line3 or index3 >= len(data_lines3)):
#                 printLine(line2)
#                 index2 += 1
#                 if index2 < len(data_lines2):
#                     line2 = data_lines2[index2]
#                     time_line2 = datetime.strptime(line2.UpdateTime[0:8]+' '+str(line2.UpdateMillisec*1000),"%H:%M:%S %f")
#         if index3 < len(data_lines3):
#             if (time_line3 <= time_line1 or index1 >= len(data_lines1)) and (time_line3 <= time_line2 or index3 >= len(data_lines3)):
#                 print " ".join([str(line3.InstrumentID),str(line3.TradingDay),str(line3.UpdateTime)[0:8],str(line3.UpdateMillisec),str(line3.LastPrice),str(line3.Volume),str(line3.AskPrice1),str(line3.AskVolume1),str(line3.BidPrice1),str(line3.BidVolume1)])
#                 printLine(line3)
#                 index3 += 1
#                 if index3 < len(data_lines3):
#                     line3 = data_lines3[index3]
#                     time_line3 = datetime.strptime(line3.UpdateTime[0:8]+' '+str(line3.UpdateMillisec*1000),"%H:%M:%S %f")
        
    print 'wancheng'
    
#     for line in data_lines1:
#         print >>appconsant.testfile," ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
#         
#     for line in data_lines2:
#         print >>appconsant.testfile," ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
#         
    
#         
#     data_lines3 = data.getDayData(c_instrumentID,file) #获取数据
#     data_config3 = conf.getInstrumentInfo(c_instrumentID) 
#      
#     a=''
#     for line in data_lines3:
#         
# #         print line.UpdateTime
# #         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
#             line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
# #         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
#         if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec) or str(line.UpdateTime)[0:8] < '09:00:00':
# #             print str(i.TradingDay)+' '+str(i.UpdateTime)[0:8]+'.'+str(i.UpdateMillisec)
#             data_lines3.remove(line)
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
#         else:
#             pass
#         a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
#     print  str(data_lines3)   
    
          
def printLine(line):
    pass

            
            
            
class diffinfo():
    __slots__ = (
        '__dateTime',         
        '__dateTime1',
        '__dateTime2',
        '__lastprice',
        '__askprice',
        '__bidprice',
        '__avgprice',
        '__lBidrAsk',
        '__lAskrBid',
    )
    
    def __init__(self):
        self.__dateTime = ''
        self.__dateTime1 = ''
        self.__dateTime2 = ''
        self.__lastprice = 0.0
        self.__askprice = 0.0
        self.__bidprice = 0.0 
        self.__avgprice = 0.0
        self.__lBidrAsk = 0.0 
        self.__lAskrBid = 0.0 


if __name__=="__main__": main()