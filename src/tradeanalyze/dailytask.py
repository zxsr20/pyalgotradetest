#!/usr/bin/python
#-*- coding=utf-8 -*-
import sys,os,zipfile,gzip
import conf,data
import itertools
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed
import logging
from tradeanalyze import StoreCsv4Nticket, mydataplot4RangeSpan,mydataplot4LeaveByWaveZ, appconsant,\
    mydataplot4macd
import pyalgotrade.logger



def dodailywork():
    print sys.path[0]
    
    rootdir = 'D:\pyTest_yh\data\\'
    instruments = ['IF1508']
    finishfilename = "dailyworkfinish.txt"
    file_object = open(finishfilename)
    try:
        all_the_text = file_object.read( )
        print 'has run date:'+all_the_text
    finally:
        file_object.close( )
    
    for f in os.listdir(rootdir):  
        file = os.path.join(rootdir, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and '.zip' in file and filename not in all_the_text:   
            print '原始文件:'+file
            process_data(rootdir,filename,instruments)
            file_object = open(finishfilename, 'a')
            file_object.write(filename)
            file_object.close( )
    
    print 'complete'
    
def dotestwork():
    print sys.path[0]
    
    
#     instruments = ['IF1508']
    finishfilename = "dailyworkfinish.txt"
    file_object = open(finishfilename)
    try:
        all_the_text = file_object.read( )
        print 'has run date:'+all_the_text
    finally:
        file_object.close( )
        
    file_object = open(finishfilename, 'a')
    #'20160715','20160718','20160719','20160720','20160721',
    dates = ['20160722','20160725','20160726','20160727','20160728','20160729']
    for test_date in dates:
        pyalgotrade.logger.celue = "rangespan"
        pyalgotrade.logger.celuedate = test_date
        runtestRangeSpan(dir,test_date,'j09')
        
        file_object.write(test_date+'j09')
    file_object.close( )
    
    print 'complete'
    
def runtestRangeSpan(dir,date,instrument):
#     mylogger.setlogfile(dir+'/'+date+instrument+'RangeSpanlog.txt')
#     mylogger.changeLoggerFile(dir+'/'+date+instrument+'RangeSpanlog.txt')
#     appconsant.lresultLogger.changefile(dir+'/'+date+instrument+'RangeSpanresult.txt')
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, "../ctpdataanalyze/"+date+instrument+".csv")
    local.run(mydataplot4RangeSpan.MyStrategyRSI, feed, rangespan_parameters_generator(instrument,date))
            
            
def process_data(rootdir,filename,instruments):
            
    date = filename
    
    for instrument in instruments:
        
        needprocess = generateDataFile(rootdir,date,instrument)   
        if needprocess == 1:
            pyalgotrade.logger.celue = "rangespan"
            pyalgotrade.logger.celuedate = date
            runRangeSpan(dir,date,instrument)
            pyalgotrade.logger.celue = "LeaveByWaveZ"
            pyalgotrade.logger.celuedate = date
            runLeaveByWaveZ(dir,date,instrument)
            pyalgotrade.logger.celue = "macd"
            pyalgotrade.logger.celuedate = date
            runmacd(dir,date,instrument)
        
        
        
        
        
#                      



def generateDataFile(rootdir,date,instrument):
    
    for f in os.listdir(rootdir):  
        file = os.path.join(rootdir, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and filename == date:   
            print '原始文件:'+file
            data_lines = data.getDayData(instrument,file) #获取数据
            if len(data_lines) > 100:
                data_config = conf.getInstrumentInfo(instrument) 
                csvfile = filename + instrument +'.csv'
    #             res=StoreCsv.process(data_lines,data_config,csvfile,malength=90)
                data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
                return 1
    return 0
    

def runRangeSpan(dir,date,instrument):
#     mylogger.setlogfile(dir+'/'+date+instrument+'RangeSpanlog.txt')
#     mylogger.changeLoggerFile(dir+'/'+date+instrument+'RangeSpanlog.txt')
#     appconsant.lresultLogger.changefile(dir+'/'+date+instrument+'RangeSpanresult.txt')
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, date+instrument+".csv")
    local.run(mydataplot4RangeSpan.MyStrategyRSI, feed, rangespan_parameters_generator(instrument,date))
    
def runRangeSpan1(dir,date,instrument): 
#     mylogger.setlogfile(dir+'/'+date+instrument+'RangeSpanlog1.txt')
#     mylogger.changeLoggerFile(dir+'/'+date+instrument+'RangeSpanlog1.txt')
#     appconsant.lresultLogger.changefile(dir+'/'+date+instrument+'RangeSpanresult1.txt')
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, date+instrument+".csv")
    local.run(mydataplot4RangeSpan.MyStrategyRSI, feed, rangespan_parameters_generator(instrument))
    
def rangespan_parameters_generator(instrumentID,date):
    """
        rangespan_ma,range取前面多少个点
        rangespan_range,range的面积范围
        rangespan_span,range的上下值小于为盘整
        rangespan_stoploss,止损金额
        rangespan_priceinrange,盘整段的头尾价格的范围
        rangespan_y,超过多少买入
        rangespan_n多少个点没有创新高
        ragnespan_d盘整大于为有效盘整
        rangespan_distanceprice和前一个盘整的价格距离小于则合并上下限
        rangespan_distance和前一个盘整的ticket距离大于则不合并上下限
        """
    instrument = [instrumentID]
    rangespan_ma= [50,100,150,200]#range(50,150,50)
    rangespan_range= [0.7,0.9]#[0.6,0.7]#floatrange(0.6,0.9,4)
    rangespan_span= range(2,15,3)   
    rangespan_stoploss= [3,5,8,10]#range(20,60,10)#range(10,60,20)   
    rangespan_priceinrange = [3,4]#range(2,10,1)
    rangespan_y= floatrange(1,5,3)
    rangespan_n= [30,60]#floatrange(30,100,2) 
    ragnespan_d = [20,40,60,70]#floatrange(50,300,6) 
    rangespan_distanceprice = [2]#floatrange(2,20,5) 
    rangespan_distance = [20]
    
    return itertools.product(instrument, rangespan_ma,rangespan_range,rangespan_span,rangespan_stoploss,rangespan_priceinrange,rangespan_y,rangespan_n,ragnespan_d,rangespan_distanceprice,rangespan_distance)

def runLeaveByWaveZ(dir,date,instrument):
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, date+instrument+".csv")
    local.run(mydataplot4LeaveByWaveZ.MyStrategy4LeaveByWaveZ, feed, LeaveByWaveZ_parameters_generator(instrument,date))
    
def LeaveByWaveZ_parameters_generator(instrumentID,date):
    instrument = [instrumentID]
    entrySMA = [660]
    exitSMA = [200]
    rsiPeriod = [100]
    overBoughtThreshold = [57]
    overSoldThreshold = [45]
    nwaveticket= [40,100,20]
    waveseg_y=[40,100,20]
    waveseg_x=[40,100,20]
    stoploss=[10,50,20]
    
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,nwaveticket,waveseg_y,waveseg_x,stoploss)

def runmacd(dir,date,instrument):
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, date+instrument+".csv")
    local.run(mydataplot4macd.MyStrategyRSI4macd, feed, macd_parameters_generator(instrument,date))
    
def macd_parameters_generator(instrumentID,date):
    instrument = [instrumentID]
    entrySMA = [660]
    exitSMA = [200]
    rsiPeriod = [100]
    overBoughtThreshold = [57]
    overSoldThreshold = [45]
    lowband = floatrange(-0.00010,-0.00040,4)
    upband = floatrange(0.00012,0.00042,4)
    bandbl = floatrange(0.8,1.5,4)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,lowband,upband,bandbl)




def floatrange(start,stop,steps):
    ''' Computes a range of floating value.
        
        Input:
            start (float)  : Start value.
            end   (float)  : End value
            steps (integer): Number of values
        
        Output:
            A list of floats
        
        <a href="https://www.baidu.com/s?wd=Example&tn=44039180_cpr&fenlei=mv6quAkxTZn0IZRqIHckPjm4nH00T1YdP1bzPjKhnWf3mH7Bn16L0ZwV5Hcvrjm3rH6sPfKWUMw85HfYnjn4nH6sgvPsT6K1TL0qnfK1TL0z5HD0IgF_5y9YIZ0lQzqlpA-bmyt8mh7GuZR8mvqVQL7dugPYpyq8Q1DvrH0YPWTLnj61PH6YnjD4nj6" target="_blank" class="baidu-highlight">Example</a>:
            >>> print floatrange(0.25, 1.3, 5)
            [0.25, 0.51249999999999996, 0.77500000000000002, 1.0375000000000001, 1.3]
    '''
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]

if __name__=="__main__": 
    dotestwork()
    #dodailywork()
