#!/usr/bin/python
#-*- coding=utf-8 -*-
import sys,os
import conf,data
import itertools
from pyalgotrade.optimizer import local
from tradeanalyze import appconsant, StoreCsv4Nticket

from pyalgotrade import plotter, dataseries
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.technical import cross
from pyalgotrade.dataseries import DataSeries
import tradeanalyze.data_struct
from tradeanalyze.data_struct import *
from astropy import logging

class MyStrategyRSI1(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,nwaveticket,wavetickets):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
        self.__priceDS4diff = dataseries.SequenceDataSeries(100000)#use to draw map

        self.wavetickets = wavetickets

        self.nwaveticket = nwaveticket
        
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.__longPos = None
        self.__shortPos = None

    def getPrice(self):
        return self.__priceDS
    
    def getPrice4diff(self):
        return self.__priceDS4diff
    
    def getwavetickets(self):
        return self.wavetickets
    
    def getWave(self):
        return self.waveDS

    def getlongSMA(self):
        return self.__longSMA

    def getshortSMA(self):
        return self.__shortSMA

    def getRSI(self):
        return self.__rsi
    
    

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
        
        logLogger = logging.getLogger('log')
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
        barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
#         appconsant.logLogger.info(barLog)
        
        if bar.getVolume != 0:
            self.__priceDS4diff.appendWithDateTime(bar.getDateTime(),bar.getPrice())
        
        
        tp = CTicketWave()
        tp.idx = len(self.wavetickets)+1
        tick_idx_start = len(self.__priceDS) - self.nwaveticket
        if tick_idx_start < 0:
            tick_idx_start = 0
        tp.tick_idx_start = tick_idx_start
        tp.tick_idx_end = len(self.__priceDS)-1
        tp.price_start = self.__priceDS[tick_idx_start]
        tp.price_end = self.__priceDS[-1]
        priceds = self.__priceDS[tick_idx_start:len(self.__priceDS)]
        tp.upper = max(priceds)
        tp.lower = min(priceds)
        tp.price_wave = tp.upper - tp.lower
        self.waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
#         appconsant.logLogger.info('wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave))
        
        self.wavetickets.append(tp)
        
    
 
    def enterLongSignal(self, bar):#当短周期上穿 长周期，就入场做多，seg也要同方向
        return self.__shortSMA[-1] > self.__longSMA[-1] and self.__shortSMA[-1] - self.__longSMA[-1] < 15 
 
    def exitLongSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 1 and bar.getBid1() != 0
 
    def enterShortSignal(self, bar):#当短周期下穿 长周期，就入场做空，seg也要同方向
        return self.__shortSMA[-1] < self.__longSMA[-1] and self.__longSMA[-1] - self.__shortSMA[-1] < 15 
 
    def exitShortSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 2 and bar.getAsk1() != 0
    
    
    
class MyStrategyRSI2(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,nwaveticket,wavetickets):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()

        self.__priceDS4diff = dataseries.SequenceDataSeries(100000)#use to draw map

        self.wavetickets = wavetickets
        
        self.nwaveticket = nwaveticket
        
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        self.__longPos = None
        self.__shortPos = None

    def getPrice(self):
        return self.__priceDS
    
    def getPrice4diff(self):
        return self.__priceDS4diff
    
    def getwavetickets(self):
        return self.wavetickets
    
    def getWave(self):
        return self.waveDS

    def getlongSMA(self):
        return self.__longSMA

    def getshortSMA(self):
        return self.__shortSMA

    def getRSI(self):
        return self.__rsi
    
    

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
        
        logLogger = logging.getLogger('log')
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
#         barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
#         appconsant.logLogger.info(barLog)

        if bar.getVolume != 0:
            self.__priceDS4diff.appendWithDateTime(bar.getDateTime(),bar.getPrice())
        
        tp = CTicketWave()
        tp.idx = len(self.wavetickets)+1
        tick_idx_start = len(self.__priceDS) - self.nwaveticket
        if tick_idx_start < 0:
            tick_idx_start = 0
        tp.tick_idx_start = tick_idx_start
        tp.tick_idx_end = len(self.__priceDS)-1
        tp.price_start = self.__priceDS[tick_idx_start]
        tp.price_end = self.__priceDS[-1]
        priceds = self.__priceDS[tick_idx_start:len(self.__priceDS)]
        tp.upper = max(priceds)
        tp.lower = min(priceds)
        tp.price_wave = tp.upper - tp.lower
        self.waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
#         appconsant.logLogger.info('wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave))
        
        self.wavetickets.append(tp)
        
    
 
    def enterLongSignal(self, bar):#当短周期上穿 长周期，就入场做多，seg也要同方向
        return self.__shortSMA[-1] > self.__longSMA[-1] and self.__shortSMA[-1] - self.__longSMA[-1] < 15 
 
    def exitLongSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 1 and bar.getBid1() != 0
 
    def enterShortSignal(self, bar):#当短周期下穿 长周期，就入场做空，seg也要同方向
        return self.__shortSMA[-1] < self.__longSMA[-1] and self.__longSMA[-1] - self.__shortSMA[-1] < 15 
 
    def exitShortSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 2 and bar.getAsk1() != 0

    



def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    
#     rootdir = appconsant.rootdir
#      
#     instrumentID = appconsant.instrumentID
#     date = appconsant.date
#     date = "20151030"
     
#     appconsant.logLogger =  Logger.Logger(logname=""+'log.txt', loglevel=1, logger="log").getlog()
      
#     instrumentID = "rb1510"
     
     
#     #数据转化
#     for f in os.listdir(rootdir):  
#         file = os.path.join(rootdir, f)  
#         filename = file.split("\\")[-1].split(".")[0]
#           
#         if os.path.isfile(file) and filename == date:   
#             print '原始文件:'+file
#             data_lines = data.getDayData(instrumentID,file) #获取数据
#             data_config = conf.getInstrumentInfo(instrumentID) 
#             csvfile = filename + instrumentID +'.csv'
# # #             res=StoreCsv.process(data_lines,data_config,csvfile,malength=90)
#             data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
# #             
#     for f in os.listdir(rootdir):  
#         file = os.path.join(rootdir, f)  
#         filename = file.split("\\")[-1].split(".")[0]
#           
#         if os.path.isfile(file) and filename == date:   
#             print '原始文件:'+file
#             data_lines2 = data.getDayData(instrumentID2,file) #获取数据
#             data_config2 = conf.getInstrumentInfo(instrumentID2) 
#             csvfile2 = filename + instrumentID +'.csv'
# #             res=StoreCsv.process(data_lines,data_config,csvfile,malength=90)
#             data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
#  
      
     
     
#     instrumentID = appconsant.instrumentID
    
    waveds1 = []
    waveds2 = []
    
#     instruments = ['IF1603','IF1512']
#     cu1512   rb1605
#     instruments = ['cu1609','rb1605']
    instruments = ['y1601','p1601']
#     instruments = ['rb1607','J1601']
#     instruments = []
#     instruments = []
    datestr = '20151126'
    
    feed1 = yahoofeed.Feed()
    feed1.addBarsFromCSV(instruments[0], datestr+instruments[0]+".csv")
    myStrategy1 = MyStrategyRSI1(feed1,instruments[0], 660,200,100,57,45,appconsant.waveseg_nwaveticket,waveds1)
    
    feed2 = yahoofeed.Feed()
    feed2.addBarsFromCSV(instruments[1], datestr+instruments[1]+".csv")
    myStrategy2 = MyStrategyRSI2(feed2,instruments[1], 660,200,100,57,45,appconsant.waveseg_nwaveticket,waveds2)
    
    
    # Attach a returns analyzers to the strategy.
#     returnsAnalyzer = returns.Returns()
#     myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    
#     print 'geshu:'+str(len(myStrategy2.getWave()))
#     for i in range(len(myStrategy2.getWave())):
#         print myStrategy2.getWave()[i]
    myStrategy2.run()
    plt1 = plotter.StrategyPlotter(myStrategy1,plotOrder=True)
#     plt1.getOrCreateSubplot("wave").addDataSeries("waveds", myStrategy1.getWave())
#     plt1.getOrCreateSubplot("wave2").addDataSeries("waveds2", myStrategy2.getWave())
    myStrategy1.run()
    
    priceDS = dataseries.SequenceDataSeries(100000)
    datetimes = myStrategy2.getPrice().getDateTimes()
    values = myStrategy2.getPrice().getValues()
    for i in range(len(datetimes)):
        priceDS.appendWithDateTime(datetimes[i], values[i]+1500)
    plt1.plotdiff2line(myStrategy1.getPrice(),priceDS)
    plt1.plotdiff2line(myStrategy1.getWave(),myStrategy2.getWave())
    
    #画一下价差的图，首先因为两个时间是相同的，所以我们这边可以做一个循环，如果时间相同，就把价格减一下，画图，但是成交为0的这样就要单独做一个数组，把成交为0的去掉，如果有一个成交为0，那么就跳到下一个
    datetimes1 = myStrategy1.getPrice4diff().getDateTimes()
    datetimes2 = myStrategy2.getPrice4diff().getDateTimes()
    prices1 = myStrategy1.getPrice4diff().getValues()
    prices2 = myStrategy2.getPrice4diff().getValues()
    pricediff = dataseries.SequenceDataSeries(100000)#use to draw map
    i = 0
    j = 0
    while True:
        if datetimes1[i] == datetimes2[j]:#不能找近似值，只能相等才行
            pricediff.appendWithDateTime(datetimes1[i], prices1[i] - prices2[j])
            i += 1
            j += 1
        elif datetimes1[i] > datetimes2[j]:
            j+=1
        elif datetimes1[i] < datetimes2[j]:
            i+=1
        if i >=len(datetimes1) or j >= len(datetimes2):
            break
        
    plt1.plotdiffline(pricediff)
            
    
#     myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
     
    
    
    
    
#     waves = []
#     u = 0
#     x = 0
#     for waveticket in myStrategy.getwavetickets():
#         u += 1
#         
#         waves.append(round(waveticket.price_wave,2))
#         
#     waveseries = dataseries.SequenceDataSeries(50000)
#     waves.sort()
#     wave = waves[0]
#     frequency = 0
#     for w in waves:
#         if w != wave:
# #             print ' '+str(wave)+' '+str(frequency)
#             waveseries.appendWithDateTime(wave,frequency)
#             frequency = 0
#         frequency += 1
#         wave = w
    
    
    
#     plt.plotdiff(waveseries)
    


#     print 'money_in = '+str(appconsant.money_in)+'money_out = '+str(appconsant.money_out)+'money_earn = '+str(appconsant.money_earn)+'market_time ='+str(appconsant.market_time)


# g = 
# print 

if __name__=="__main__": main()

