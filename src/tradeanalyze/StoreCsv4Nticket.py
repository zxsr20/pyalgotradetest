#!/usr/bin/python
#-*- coding=utf-8 -*-
'''
Created on 2015-6-13

@author: ct
'''
import sys,os
import data_struct
from data_struct import *
import csv
from tradeanalyze import appconsant
from datetime import *
import copy


def process(data_lines,data_config,filename,malength=60):
    pre_vol = 0;pre_oi = 0;pre_ot = 0;avg_pri=0;newbidprice=0;newaskprice=0 #ot:ontickturnover
    idx = 0;
#     resdic={}
#     AllData = CAllData()
#     AllData.conf = data_config
#     AllData.allTicks = []
#     AllData.allSegPankous = []


    writer = csv.writer(file(filename, 'wb'))
     
    writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close','bidvol','askvol'])
#     writer.writerow(['Date', 'bidprice', 'lastprice','avgprice','askprice','diff_vol','avgprice'])
    a=''
    c = []
    print '文件总行数:'+str(len(data_lines))  
    #去重并保存到csv
    for line in data_lines:
        
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
#             line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec) :
            c.append(line)
#             data_lines.remove(line)
            print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        elif str(line.UpdateTime)[0:8] < '09:00:00':
            c.append(line)
#             data_lines.remove(line)
            pass
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        else:
            pass
            
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
        
    for line in c:
        data_lines.remove(line)

    i = 1
    for line in data_lines:
        if i % appconsant.nticket == 0:
            diff_vol = line.Volume - pre_vol  
            pre_vol = line.Volume
            
            diff_ot = line.Turnover - pre_ot 
            pre_ot = line.Turnover
        
            if diff_vol == 0: 
                avg_pri = avg_pri+0#没有成交的话就取上一个值
            else :
#                 print "diff_ot:"+str(diff_ot)+"diff_vol:"+str(diff_vol)+"data_config.PriceTick:"+str(data_config.PriceTick)+"data_config.VolumeMultiple:"+str(data_config.VolumeMultiple)
                
                avg_pri = diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple)
#                 print "diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple):"+str(avg_pri)
#             print str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+'  '+str('avg_pri:'+str(avg_pri)) + 'BidPrice1:'+str(line.BidPrice1)+'AskPrice1:'+str(line.AskPrice1)
            try:
                newbidprice = int(round(line.BidPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError BidPrice1:'+str(line.BidPrice1) +str('avg_pri:'+str(avg_pri))
                newbidprice = 0
                
            try:
                newlastprice = round(line.LastPrice/data_config.PriceTick,3)
            except OverflowError:
                print 'OverflowError LastPrice:'+str(line.LastPrice) +str('avg_pri:'+str(avg_pri))
                newlastprice = 0
                
            try:
#                 newaskprice = int(round(line.AskPrice1*5))
                newaskprice = int(round(line.AskPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError AskPrice1:'+str(line.AskPrice1) +str('avg_pri:'+str(avg_pri))
                newaskprice = 0
#             newbidprice = int(round(line.BidPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
#             newaskprice = int(round(line.AskPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
            #如果是下午的行情，把它们都减去
            writer.writerow([str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec),newbidprice,newlastprice,avg_pri,newaskprice,diff_vol,avg_pri,str(line.BidVolume1),str(line.AskVolume1)])
            line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+str(newbidprice)+str(newlastprice)+str(avg_pri)+str(newaskprice)+str(diff_vol)+str(avg_pri)+str(line.BidVolume1)+str(line.AskVolume1)
#             line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+' '+instrumentId+' '+str(newlastprice)+' '+str(diff_vol)+' '+str(newbidprice)+' '+str(line.BidVolume1)+' '+str(newaskprice)+' '+str(line.AskVolume1)
            
            date_oldformat = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
            year = int(date_oldformat[0:4])
            month = int(date_oldformat[4:6])
            day = int(date_oldformat[6:8])
            hour = int(date_oldformat[9:11])
            minute = int(date_oldformat[12:14])
            second = int(date_oldformat[15:17])
            microsecond = int(date_oldformat[18:22])*1000
            ret = datetime(year, month, day,hour,minute,second,microsecond)
            __barTime = ret.strftime('%Y-%m-%d %H:%M:%S %f')
            barTime = __barTime[0:len(__barTime)-3]
            
            line.date_format = barTime
            line.ask1_format = newaskprice
            line.bid1_format = newbidprice
            line.avg_format = avg_pri
            print 'info: '+line.info
        i+=1        
      
    return data_lines

def guiyi(instrumentId,data_lines,data_config,filename,malength=60):
    pre_vol = 0;pre_oi = 0;pre_ot = 0;avg_pri=0;newbidprice=0;newaskprice=0 #ot:ontickturnover
    idx = 0;
#     resdic={}
#     AllData = CAllData()
#     AllData.conf = data_config
#     AllData.allTicks = []
#     AllData.allSegPankous = []


#     writer = csv.writer(file(filename, 'wb'))
#      
#     writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close','bidvol','askvol'])
#     writer.writerow(['Date', 'bidprice', 'lastprice','avgprice','askprice','diff_vol','avgprice'])
    a=''
    c = []
    print '文件总行数:'+str(len(data_lines))  
    #去重并保存到csv
    for line in data_lines:
        str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
#             line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
        print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec) :
#             c.append(line)
#             data_lines.remove(line)
            print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        elif str(line.UpdateTime)[0:8] < '09:00:00':
            c.append(line)
#             data_lines.remove(line)
            pass
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        else:
            pass
            
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
        
    for line in c:
        data_lines.remove(line)

    i = 1
    for line in data_lines:
        if i % appconsant.nticket == 0:
            diff_vol = line.Volume - pre_vol  
            pre_vol = line.Volume
            
            diff_ot = line.Turnover - pre_ot 
            pre_ot = line.Turnover
        
            if diff_vol == 0: 
                avg_pri = avg_pri+0#没有成交的话就取上一个值
            else :
#                 print "diff_ot:"+str(diff_ot)+"diff_vol:"+str(diff_vol)+"data_config.PriceTick:"+str(data_config.PriceTick)+"data_config.VolumeMultiple:"+str(data_config.VolumeMultiple)
                
                avg_pri = diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple)
                print "diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple):"+str(avg_pri)
#             print str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+'  '+str('avg_pri:'+str(avg_pri)) + 'BidPrice1:'+str(line.BidPrice1)+'AskPrice1:'+str(line.AskPrice1)
            try:
                newbidprice = int(round(line.BidPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError BidPrice1:'+str(line.BidPrice1) +str('avg_pri:'+str(avg_pri))
                newbidprice = 0
                
            try:
                newlastprice = round(line.LastPrice/data_config.PriceTick,3)
            except OverflowError:
                print 'OverflowError LastPrice:'+str(line.LastPrice) +str('avg_pri:'+str(avg_pri))
                newlastprice = 0
                
            try:
#                 newaskprice = int(round(line.AskPrice1*5))
                newaskprice = int(round(line.AskPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError AskPrice1:'+str(line.AskPrice1) +str('avg_pri:'+str(avg_pri))
                newaskprice = 0
#             newbidprice = int(round(line.BidPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
#             newaskprice = int(round(line.AskPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
            #如果是下午的行情，把它们都减去
#             writer.writerow([str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec),newbidprice,newlastprice,avg_pri,newaskprice,diff_vol,avg_pri,str(line.BidVolume1),str(line.AskVolume1)])
#             line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+' '+str(newbidprice)+' '+str(newlastprice)+' '+str(avg_pri)+' '+str(newaskprice)+' '+str(diff_vol)+' '+str(avg_pri)+' '+str(line.BidVolume1)+' '+str(line.AskVolume1)
            line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+' '+instrumentId+' '+str(newlastprice)+' '+str(diff_vol)+' '+str(newbidprice)+' '+str(line.BidVolume1)+' '+str(newaskprice)+' '+str(line.AskVolume1)
            
            print 'info: '+line.info
        i+=1        
      
    return data_lines


def guiyigai(instrumentId,data_lines,data_config,filename,malength=60):
    pre_vol = 0;pre_oi = 0;pre_ot = 0;avg_pri=0;newbidprice=0;newaskprice=0 #ot:ontickturnover
    idx = 0;
#     resdic={}
#     AllData = CAllData()
#     AllData.conf = data_config
#     AllData.allTicks = []
#     AllData.allSegPankous = []


    writer = csv.writer(file(filename, 'wb'))
#      
    writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close','bidvol','askvol'])
#     writer.writerow(['Date', 'bidprice', 'lastprice','avgprice','askprice','diff_vol','avgprice'])
    a=''
    c = []
    print '文件总行数:'+str(len(data_lines))  
    repeat = 0
    #去重并保存到csv
    
    for line in data_lines:
        if str(line.UpdateTime)[0:8] < '09:00:00':
            c.append(line)
#             data_lines.remove(line)
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        else:
            pass
            
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
        
    for line in c:
        data_lines.remove(line)
        
    c = []
    
    for line in data_lines:
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
        if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
            line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=2)).strftime( '%H:%M:%S' )
#         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec) :
            if repeat > 0:
                
                if repeat == 1:
                    line.UpdateMillisec = 700 #如果时间一致，就改为500
                else:
                    line.UpdateMillisec = 800 #如果时间一致，就改为500
                repeat += 1
            else:
                line.UpdateMillisec = 500 #如果时间一致，就改为500
                repeat = 1
#             c.append(line)
            print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        else:
            a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
            repeat = 0
            
        
        
    for line in c:
        data_lines.remove(line)
    
    line_last = None
    line = None
#     ddatetime = datetime.strptime(data_lines[0].UpdateTime[0:8]+'.'+data_lines[0].UpdateMillisec,"%H:%M:%S %f")
    i = 0
    while True:
        if i >= len(data_lines):
            break
        line = data_lines[i]
        if line_last != None:
            if (datetime.strptime(line.UpdateTime[0:8]+' '+str(line.UpdateMillisec),"%H:%M:%S %f") - datetime.strptime(line_last.UpdateTime[0:8]+' '+str(line_last.UpdateMillisec),"%H:%M:%S %f")).seconds == 2:
                line_copy = copy.deepcopy(line_last)
                line_copy.UpdateTime = datetime.strftime(datetime.strptime(line_last.UpdateTime[0:8],"%H:%M:%S") +  timedelta(seconds =1),"%H:%M:%S")
                print 'newupdatetime: '+str(line_copy.UpdateTime)
                data_lines.insert(i,line_copy)
                print (datetime.strptime(line.UpdateTime[0:8]+' '+str(line.UpdateMillisec),"%H:%M:%S %f") - datetime.strptime(line_last.UpdateTime[0:8]+' '+str(line_last.UpdateMillisec),"%H:%M:%S %f")).seconds
        line_last = data_lines[i] 
        i+=1
                

    i = 1
    for line in data_lines:
        if i % appconsant.nticket == 0:
            diff_vol = line.Volume - pre_vol  
            pre_vol = line.Volume
            
            diff_ot = line.Turnover - pre_ot 
            pre_ot = line.Turnover
        
            if diff_vol == 0: 
                avg_pri = avg_pri+0#没有成交的话就取上一个值
            else :
#                 print "diff_ot:"+str(diff_ot)+"diff_vol:"+str(diff_vol)+"data_config.PriceTick:"+str(data_config.PriceTick)+"data_config.VolumeMultiple:"+str(data_config.VolumeMultiple)
                
                avg_pri = diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple)
#                 print "diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple):"+str(avg_pri)
#             print str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+'  '+str('avg_pri:'+str(avg_pri)) + 'BidPrice1:'+str(line.BidPrice1)+'AskPrice1:'+str(line.AskPrice1)
            try:
                newbidprice = int(round(line.BidPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError BidPrice1:'+str(line.BidPrice1) +str('avg_pri:'+str(avg_pri))
                newbidprice = 0
                
            try:
                newlastprice = round(line.LastPrice/data_config.PriceTick,3)
            except OverflowError:
                print 'OverflowError LastPrice:'+str(line.LastPrice) +str('avg_pri:'+str(avg_pri))
                newlastprice = 0
                
            try:
#                 newaskprice = int(round(line.AskPrice1*5))
#                 print instrumentId +'  '+str(line.AskPrice1)+'  '+str(data_config.PriceTick)
                newaskprice = int(round(line.AskPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError AskPrice1:'+str(line.AskPrice1) +str('avg_pri:'+str(avg_pri))
                newaskprice = 0
#             newbidprice = int(round(line.BidPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
#             newaskprice = int(round(line.AskPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
            #如果是下午的行情，把它们都减去
            
            
            writer.writerow([str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec),newbidprice,newlastprice,avg_pri,newaskprice,diff_vol,avg_pri,str(line.BidVolume1),str(line.AskVolume1)])
#             line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+' '+str(newbidprice)+' '+str(newlastprice)+' '+str(avg_pri)+' '+str(newaskprice)+' '+str(diff_vol)+' '+str(avg_pri)+' '+str(line.BidVolume1)+' '+str(line.AskVolume1)
            line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+' '+instrumentId+' '+str(newlastprice)+' '+str(diff_vol)+' '+str(newbidprice)+' '+str(line.BidVolume1)+' '+str(newaskprice)+' '+str(line.AskVolume1)
            
            date_oldformat = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
            year = int(date_oldformat[0:4])
            month = int(date_oldformat[4:6])
            day = int(date_oldformat[6:8])
            hour = int(date_oldformat[9:11])
            minute = int(date_oldformat[12:14])
            second = int(date_oldformat[15:17])
            microsecond = int(date_oldformat[18:22])*1000
            ret = datetime(year, month, day,hour,minute,second,microsecond)
            __barTime = ret.strftime('%Y-%m-%d %H:%M:%S %f')
            barTime = __barTime[0:len(__barTime)-3]
            line.date_format = barTime
            
            line.ask1_format = newaskprice
            line.bid1_format = newbidprice
            line.avg_format = avg_pri
#             print 'info: '+line.info
        i+=1        
      
    return data_lines

def guiyigai_other(instrumentId,data_lines,data_config,filename,malength=60):
    pre_vol = 0;pre_oi = 0;pre_ot = 0;avg_pri=0;newbidprice=0;newaskprice=0 #ot:ontickturnover
    idx = 0;
#     resdic={}
#     AllData = CAllData()
#     AllData.conf = data_config
#     AllData.allTicks = []
#     AllData.allSegPankous = []


    writer = csv.writer(file(filename, 'wb'))
#      
    writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close','bidvol','askvol'])
#     writer.writerow(['Date', 'bidprice', 'lastprice','avgprice','askprice','diff_vol','avgprice'])
    a=''
    c = []
    print '文件总行数:'+str(len(data_lines))  
    repeat = 0
    #去重并保存到csv
    
    for line in data_lines:
        if str(line.UpdateTime)[0:8] < '09:00:00':
            c.append(line)
#             data_lines.remove(line)
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        else:
            pass
            
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
        
    for line in c:
        data_lines.remove(line)
        
    c = []
    
    for line in data_lines:
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
        if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
            line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=2)).strftime( '%H:%M:%S' )
#         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec) :
            if repeat > 0:
                
                if repeat == 1:
                    line.UpdateMillisec = 700 #如果时间一致，就改为500
                else:
                    line.UpdateMillisec = 800 #如果时间一致，就改为500
                repeat += 1
            else:
                line.UpdateMillisec = 500 #如果时间一致，就改为500
                repeat = 1
#             c.append(line)
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        else:
            a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
            repeat = 0
            
        
        
    for line in c:
        data_lines.remove(line)
    
    

    i = 1
    for line in data_lines:
        if i % appconsant.nticket == 0:
            diff_vol = line.Volume - pre_vol  
            pre_vol = line.Volume
            
            diff_ot = line.Turnover - pre_ot 
            pre_ot = line.Turnover
        
            if diff_vol == 0: 
                avg_pri = avg_pri+0#没有成交的话就取上一个值
            else :
#                 print "diff_ot:"+str(diff_ot)+"diff_vol:"+str(diff_vol)+"data_config.PriceTick:"+str(data_config.PriceTick)+"data_config.VolumeMultiple:"+str(data_config.VolumeMultiple)
                
                avg_pri = diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple)-appconsant.realmarket_diff
#                 print "diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple):"+str(avg_pri)
#             print str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+'  '+str('avg_pri:'+str(avg_pri)) + 'BidPrice1:'+str(line.BidPrice1)+'AskPrice1:'+str(line.AskPrice1)
            try:
                newbidprice = int(round(line.BidPrice1/data_config.PriceTick))-appconsant.realmarket_diff
            except OverflowError:
                print 'OverflowError BidPrice1:'+str(line.BidPrice1) +str('avg_pri:'+str(avg_pri))
                newbidprice = 0
                
            try:
                newlastprice = round(line.LastPrice/data_config.PriceTick,3)
            except OverflowError:
                print 'OverflowError LastPrice:'+str(line.LastPrice) +str('avg_pri:'+str(avg_pri))
                newlastprice = 0
                
            try:
#                 newaskprice = int(round(line.AskPrice1*5))
#                 print instrumentId +'  '+str(line.AskPrice1)+'  '+str(data_config.PriceTick)
                newaskprice = int(round(line.AskPrice1/data_config.PriceTick))-appconsant.realmarket_diff
            except OverflowError:
                print 'OverflowError AskPrice1:'+str(line.AskPrice1) +str('avg_pri:'+str(avg_pri))
                newaskprice = 0
#             newbidprice = int(round(line.BidPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
#             newaskprice = int(round(line.AskPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
            #如果是下午的行情，把它们都减去
            
            
            writer.writerow([str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec),newbidprice,newlastprice,avg_pri,newaskprice,diff_vol,avg_pri,str(line.BidVolume1),str(line.AskVolume1)])
#             line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+' '+str(newbidprice)+' '+str(newlastprice)+' '+str(avg_pri)+' '+str(newaskprice)+' '+str(diff_vol)+' '+str(avg_pri)+' '+str(line.BidVolume1)+' '+str(line.AskVolume1)
            line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+' '+instrumentId+' '+str(newlastprice)+' '+str(diff_vol)+' '+str(newbidprice)+' '+str(line.BidVolume1)+' '+str(newaskprice)+' '+str(line.AskVolume1)
            
            date_oldformat = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
            year = int(date_oldformat[0:4])
            month = int(date_oldformat[4:6])
            day = int(date_oldformat[6:8])
            hour = int(date_oldformat[9:11])
            minute = int(date_oldformat[12:14])
            second = int(date_oldformat[15:17])
            microsecond = int(date_oldformat[18:22])*1000
            ret = datetime(year, month, day,hour,minute,second,microsecond)
            __barTime = ret.strftime('%Y-%m-%d %H:%M:%S %f')
            barTime = __barTime[0:len(__barTime)-3]
            line.date_format = barTime
            
            line.ask1_format = newaskprice
            line.bid1_format = newbidprice
            line.avg_format = avg_pri
#             print 'info: '+line.info
        i+=1        
      
    return data_lines

def processbymeaning(data_lines,data_config,filename,malength=60):
    pre_vol = 0;pre_oi = 0;pre_ot = 0;avg_pri=0;newbidprice=0;newaskprice=0 #ot:ontickturnover
    idx = 0;
#     resdic={}
#     AllData = CAllData()
#     AllData.conf = data_config
#     AllData.allTicks = []
#     AllData.allSegPankous = []


    writer = csv.writer(file(filename, 'wb'))
    writer.writerow(['日期'.decode('utf-8').encode('gb2312'), '买一价'.decode('utf-8').encode('gb2312'), '最新价'.decode('utf-8').encode('gb2312'),'卖一价'.decode('utf-8').encode('gb2312'),'数量'.decode('utf-8').encode('gb2312'),'平均价'.decode('utf-8').encode('gb2312'),'买一量'.decode('utf-8').encode('gb2312'),'卖一量'.decode('utf-8').encode('gb2312')])
#     writer.writerow(['Date', 'bidprice', 'lastprice','avgprice','askprice','diff_vol','avgprice'])
    a=''
    c = []
    print '文件总行数:'+str(len(data_lines))  
    #去重并保存到csv
    for line in data_lines:
        
#         print line.UpdateTime
#         print (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         if datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") >= datetime.strptime("13:00:00","%H:%M:%S"):
#             line.UpdateTime = (datetime.strptime(line.UpdateTime[0:8],"%H:%M:%S") - timedelta(hours=1.5)).strftime( '%H:%M:%S' )
#         print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        if a==str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec) :
            c.append(line)
#             data_lines.remove(line)
            print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        elif str(line.UpdateTime)[0:8] < '09:00:00':
            c.append(line)
#             data_lines.remove(line)
            pass
#             print " ".join([str(line.InstrumentID),str(line.TradingDay),str(line.UpdateTime)[0:8],str(line.UpdateMillisec),str(line.LastPrice),str(line.Volume),str(line.AskPrice1),str(line.AskVolume1),str(line.BidPrice1),str(line.BidVolume1)])
        else:
            pass
            
        a=str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
        
    for line in c:
        data_lines.remove(line)

    i = 1
    for line in data_lines:
        if i % appconsant.nticket == 0:
            diff_vol = line.Volume - pre_vol  
            pre_vol = line.Volume
            
            diff_ot = line.Turnover - pre_ot 
            pre_ot = line.Turnover
        
            if diff_vol == 0: 
                avg_pri = avg_pri+0#没有成交的话就取上一个值
            else :
#                 print "diff_ot:"+str(diff_ot)+"diff_vol:"+str(diff_vol)+"data_config.PriceTick:"+str(data_config.PriceTick)+"data_config.VolumeMultiple:"+str(data_config.VolumeMultiple)
                
                avg_pri = diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple)
#                 print "diff_ot/diff_vol/ (data_config.PriceTick * data_config.VolumeMultiple):"+str(avg_pri)
#             print str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+'  '+str('avg_pri:'+str(avg_pri)) + 'BidPrice1:'+str(line.BidPrice1)+'AskPrice1:'+str(line.AskPrice1)
            try:
                newbidprice = int(round(line.BidPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError BidPrice1:'+str(line.BidPrice1) +str('avg_pri:'+str(avg_pri))
                newbidprice = 0
                
            try:
                newlastprice = round(line.LastPrice/data_config.PriceTick,3)
            except OverflowError:
                print 'OverflowError LastPrice:'+str(line.LastPrice) +str('avg_pri:'+str(avg_pri))
                newlastprice = 0
                
            try:
#                 newaskprice = int(round(line.AskPrice1*5))
                newaskprice = int(round(line.AskPrice1/data_config.PriceTick))
            except OverflowError:
                print 'OverflowError AskPrice1:'+str(line.AskPrice1) +str('avg_pri:'+str(avg_pri))
                newaskprice = 0
#             newbidprice = int(round(line.BidPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
#             newaskprice = int(round(line.AskPrice1/(data_config.PriceTick * data_config.VolumeMultiple)))
            #如果是下午的行情，把它们都减去
            writer.writerow([str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec),newbidprice,newlastprice,newaskprice,diff_vol,avg_pri,str(line.BidVolume1),str(line.AskVolume1)])
            line.info = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)+str(newbidprice)+str(newlastprice)+str(avg_pri)+str(newaskprice)+str(diff_vol)+str(avg_pri)+str(line.BidVolume1)+str(line.AskVolume1)
        i+=1        
      
    return data_lines

