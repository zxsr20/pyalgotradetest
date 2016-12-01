#!/usr/bin/python
#-*- coding=utf-8 -*-
import os
import conf,data
import logging
# import StoreCsv
# import itertools
# from pyalgotrade.optimizer import local
from tradeanalyze import appconsant, StoreCsv4Nticket, mylogger

from pyalgotrade import plotter, dataseries
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import strategy
# from pyalgotrade.technical import ma
# from pyalgotrade.technical import rsi
# from pyalgotrade.technical import cross
# from pyalgotrade.dataseries import DataSeries
# import tradeanalyze.data_struct
from tradeanalyze.data_struct import *
import time

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,rangespan_nwaveticket,rangespan_ma,rangespan_range,rangespan_span,rangespan_stoploss,rangespan_y,rangespan_n):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
#         self.__price_index = 0
        
        #wave相关
        
        
        data_config = conf.getInstrumentInfo(instrument) 
        
        self.rangespan_nwaveticket = rangespan_nwaveticket
        self.rangespan_ma = rangespan_ma
        self.rangespan_range = rangespan_range
        self.rangespan_span = rangespan_span
        self.rangespan_stoploss = rangespan_stoploss * data_config.PriceTick
        self.rangespan_y = rangespan_y
        self.rangespan_n = 40
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.rangeUpperDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.rangeLowerDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        self.lastrangeupper = 0.0
        self.lastrangelower = 0.0
        
        self.xrangeUpperDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.xrangeLowerDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        self.moneyearn = []
        self.moneyearntimes = []
        self.moneyloss = []
        
        self.buyprice = 0.0
        self.nonewtop = 0
        self.topprice = 0.0
        
        
        
        #用于交易结果统计
        self.lastmymoney = 0.0
        self.losstime = 0
        self.wintime = 0
        self.winmoney = 0.0
        self.lossmoney = 0.0
        
        self.__longPos = None
        self.__shortPos = None

    def getmarketinfo(self):
        return '交易次数:'+str(self.wintime+self.losstime)+'盈利次数:'+str(self.wintime)+'亏损次数:'+str(self.losstime)+'盈利额:'+str(self.winmoney)+'亏损额:'+str(self.lossmoney)
    def getPrice(self):
        return self.__priceDS
    
    def getwavetickets(self):
        return self.wavetickets
    
    def getWave(self):
        return self.waveDS

    def getlongSMA(self):
        return self.__longSMA
    
    def getrangeupper(self):
        return self.rangeUpperDS
    
    def getrangelower(self):
        return self.rangeLowerDS

    def getxrangeupper(self):
        return self.xrangeUpperDS
    
    def getxrangelower(self):
        return self.xrangeLowerDS

    def getshortSMA(self):
        return self.__shortSMA

    def getRSI(self):
        return self.__rsi
    
    def getmoneyearn(self):
        return self.moneyearn
    def getmoneyearntimes(self):
        return self.moneyearntimes
    def getmoneyloss(self):
        return self.moneyloss
    
    

    def onEnterCanceled(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitOk(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        position.exitMarket()
        
            
    

    def onBars(self, bars):
        
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
        barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
        printLog(barLog)
        

        if len(self.__priceDS) < self.rangespan_ma:
            return
        
        
        priceds = []
        for i in range(self.rangespan_ma):
            priceds.append(round(self.__priceDS[-(i+1)],0))
        dic = {}
        for item in priceds:
            dic[item] = dic.get(item, 0) + 1
        dic = sorted(dic.items())
        numds = []
        pds = []
        for item in dic:
            numds.append(item[1]) 
            pds.append(item[0]) 
        
        ids = mymost_close_array(numds,len(numds),self.rangespan_range)

        rangeLower = pds[ids[0]]
        rangeUpper = pds[ids[1]]

        self.rangeLowerDS.appendWithDateTime(bar.getDateTime(),rangeLower)
        self.rangeUpperDS.appendWithDateTime(bar.getDateTime(),rangeUpper)
        
        if rangeUpper - rangeLower <= self.rangespan_span:
            
            self.xrangeLowerDS.appendWithDateTime(bar.getDateTime(),rangeLower)
            self.xrangeUpperDS.appendWithDateTime(bar.getDateTime(),rangeUpper)
            
            
                
        else:
            self.xrangeLowerDS.appendWithDateTime(bar.getDateTime(),None)
            self.xrangeUpperDS.appendWithDateTime(bar.getDateTime(),None)
            

        
        #交易相关
        if self.lastmymoney == 0:
            self.lastmymoney = 1000000
        
        
        if self.__longPos is not None or self.__shortPos is not None:#已入场
            
            if self.__longPos is not None:#已做多
                 
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                
                
                
            if self.__shortPos is not None:#已做空
                 
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                   
                
        else:
            if self.lastmymoney != self.getBroker().getCash():
                if self.lastmymoney - self.getBroker().getCash() > 0:
                    printLog('上一次交易亏损'+str(self.lastmymoney - self.getBroker().getCash()))
                    self.losstime += 1
                    self.moneyearn.append(self.lastmymoney - self.getBroker().getCash())
                    self.moneyearntimes.append(bar.getDateTime())
                    self.lossmoney += self.lastmymoney - self.getBroker().getCash()
                else:
                    self.wintime += 1
                    self.winmoney += self.getBroker().getCash() - self.lastmymoney 
                    self.moneyearn.append(self.lastmymoney - self.getBroker().getCash())
                    self.moneyearntimes.append(bar.getDateTime())
                    printLog('上一次交易盈利'+str(self.getBroker().getCash()-self.lastmymoney))
                self.lastmymoney = self.getBroker().getCash()
            



def mymost_close_array(array,length,n):
    
    cumarr = []
    
    for i in range(length):
#         cum = ap()
        if i == 0:
            key = 0 + array[i] 
        else:
            key = cumarr[i-1] + array[i] 
#         cum.key = cumarr[-1]
#         cum.pos = i
#         print 'i:'+str(i)+'cum.key'+str(key)
        cumarr.append(key)
    if n<1:
        n = cumarr[-1]*n
    
    i = -1
    k = length -1
    a = False
    b = False
    while True:
        if a==False:
            i=i+1
            if cumarr[k] - cumarr[i] < n:
                a = True
                i = i-1
        if b==False:
            k=k-1
            if cumarr[k] - cumarr[i] < n:
#                 k = k+1
                b = True
                k = k+1
        if a==True and b==True:
            break        
    
    
    
#     print 'i:'+str(i)+'k:'+str(k)
#     print array[i+1:k+1]
    return [i+1,k]
    

  
def printLog(log):
#     pass
    mylogger.printlog(log)

    


def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    rootdir = appconsant.rootdir
    instrumentID = appconsant.instrumentID
    date = appconsant.date
    ISOTIMEFORMAT='%Y-%m-%d%H%M%S'
#     appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+ time.strftime( ISOTIMEFORMAT, time.localtime() )+'log.txt', loglevel=1, logger="log").getlog()
#     appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+'log.txt', loglevel=1, logger="log").getlog()
    mylogger.changeLoggerFile(instrumentID+date+ time.strftime( ISOTIMEFORMAT, time.localtime() )+'log.txt')
    
    #数据转化
    for f in os.listdir(rootdir):  
        file = os.path.join(rootdir, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and filename == date:   
            print '原始文件:'+file
            data_lines = data.getDayData(instrumentID,file) #获取数据
            data_config = conf.getInstrumentInfo(instrumentID) 
            csvfile = filename + instrumentID +'.csv'
#             res=StoreCsv.process(data_lines,data_config,csvfile,malength=90)
            data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
    
    
    
#     instrumentID = appconsant.instrumentID
    
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
    
    myStrategy = MyStrategyRSI(feed,instrumentID, 660,200,100,57,45,appconsant.rangespan_nwaveticket,appconsant.rangespan_ma,appconsant.rangespan_range,appconsant.rangespan_span,appconsant.rangespan_stoploss,appconsant.rangespan_y,appconsant.rangespan_n)
     
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
    plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangeupper", myStrategy.getxrangeupper())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangelower", myStrategy.getxrangelower())
     
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
     

    printLog(myStrategy.getmarketinfo())
    
    printLog(myStrategy.getmoneyearn())
    printLog(myStrategy.getmoneyloss())


    plt.plot()



if __name__=="__main__": main()
