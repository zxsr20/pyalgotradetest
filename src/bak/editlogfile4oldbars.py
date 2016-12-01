#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import conf,data,process
import StoreCsv
import itertools
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed
import mydatasplot
from tradeanalyze import appconsant, StoreCsvNticket

def main():
    
    
            
    
    rootdir = 'D:\pyTest_yh\data\\'
     
    instrumentID = appconsant.instrumentID
#     instrumentID = "rb1510"
    date = "20150717"
    
    #数据转化
#     feed = yahoofeed.Feed()
    for f in os.listdir(rootdir):  
        file = os.path.join(rootdir, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and filename == date:   
            print '原始文件:'+file
            data_lines = data.getDayData(instrumentID,file) #获取数据
            data_config = conf.getInstrumentInfo(instrumentID)
            
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
        
#     for line in c:
#         data_lines.remove(line) 
#     
#     for index in range(len(lines)):
#         if lines[index][0:3]=='bar':
#            lines 
            
    
        
#     lines.insert(1, 'a new line') # 在第二行插入
#     s = '\n'.join(lines)
#     fp = file('data.txt', 'w')
#     fp.write(s)
#     fp.close()
    
if __name__=="__main__": main()
