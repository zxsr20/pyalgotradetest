#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import conf,data,process
import StoreCsv
import itertools
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed, tusharefeed
import rsi2
import tushare as ts

def main():
#     open("stock.csv",'a')
    #获取100个股票代码
#     ll = ts.get_concept_classified()
#     ll.to_csv('stock.csv',encoding='utf-8',columns=['code','name','c_name'])
    
    
#     file_object = open('thefile.txt', 'w')
#      
#     file_object.write(str(ll))
#     file_object.close()

#获取每个股票的每日价格全部历史数据
# dateTime = self.__parseDate(csvRowDict["Date"])
#         close = float(csvRowDict["Close"])
#         open_ = float(csvRowDict["Open"])
#         high = float(csvRowDict["High"])
#         low = float(csvRowDict["Low"])
#         volume = float(csvRowDict["Volume"])
#         adjClose = float(csvRowDict["Adj Close"])


    stock_list = ['002151','000156']
    for stock in stock_list:
        df = ts.get_hist_data(stock)
        open(stock+".csv",'a')
        df. to_csv(stock+'.csv',encoding='utf-8',columns=['open', 'high','low','close','volume','close'])
        feed = tusharefeed.Feed()
        feed.addBarsFromCSV(stock, stock+'.csv')
        local.run(rsi2.RSI2, feed, parameters_generator(stock))
        
        
        
        
        
#     for l in ll:
#         print str(l.code)+l.name+l.c_name
    
    
    
    
    
    #进行策略分析，取三年和全部数据都获利较强的股票
    #对单个股票进行画图，看是否在买点
    
#     rootdir = 'D:\pyTest_yh\data\\'
#      
#     instrumentID = "IF1506"
#     
#     #数据转化
#     feed = yahoofeed.Feed()
#     for f in os.listdir(rootdir):  
#         file = os.path.join(rootdir, f)  
#         if os.path.isfile(file):   
#             print '原始文件:'+file
#             data_lines = data.getDayData(instrumentID,file) #获取数据
#             data_config = conf.getInstrumentInfo(instrumentID) 
#             csvfile = file.split("\\")[-1].split(".")[0] +'.csv'
#             res=StoreCsv.process(data_lines,data_config,csvfile,malength=90)
#             print '有效行数:'+str(res)
#             feed.addBarsFromCSV(instrumentID, csvfile)
#     #数据处理
#     local.run(rsi2.RSI2, feed, parameters_generator())
    
def parameters_generator(stock):
    instrument = [str(stock)]
    entrySMA = [150]
    exitSMA = [6]
    rsiPeriod = range(2, 6)
    overBoughtThreshold = range(85, 96)
    overSoldThreshold = range(5, 15)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)



if __name__=="__main__": main()

