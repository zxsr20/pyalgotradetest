#!/usr/bin/python
#-*- coding=utf-8 -*-
import sys,os
import conf,data,process
import StoreCsv
import itertools
from pyalgotrade.optimizer import local
import mydatasplot
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
import Logger

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
#         self.__price_index = 0
        
        #wave相关
        self.wavetickets = []
        self.high = 0.0
        self.lower = 0.0
        
        self.nwaveticket = 5
#         self.waveseg_y = waveseg_y
#         self.waveseg_x = waveseg_x
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
#         self.buyprice = 0.0
#         self.stoploss = stoploss
        
        self.topwaves = []
        self.maxwave = None
        self.rongren = 0.0
        self.y = 0.5
        
        #seg相关
#         self.rongren = rongren #can skip num
#         self.bNewSeg = False;
#         self.nDir = 0;
#         self.__segmentDS =  dataseries.SequenceDataSeries(100000)#use to draw map
#         self.allSegPankous = []#store the pankou data
#         
#         #测落相关
#         self.wavedir = 0
#         self.stoploss = 0.0
        
        self.__longSMA = ma.SMA(self.__priceDS, longSMA)
        self.__shortSMA = ma.SMA(self.__priceDS, shortSMA)
        self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
        self.__overBoughtThreshold = overBoughtThreshold
        self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None

    def getPrice(self):
        return self.__priceDS
    
    def getwavetickets(self):
        return self.wavetickets
    
    def getTopwaves(self):
        return self.topwaves
    
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
        
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
        barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
        printLog(barLog)
        
        
        
        
        
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
        
        if self.__priceDS[-1] == tp.upper:
            tp.dir = 1
        elif self.__priceDS[-1] == tp.lower:
            tp.dir = 2
        else:
            tp.dir = 3
            
        
        
        tp.price_wave = tp.upper - tp.lower
        self.waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
        printLog('wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave))
        
        self.wavetickets.append(tp)
        
        if self.maxwave == None:
            self.maxwave = self.wavetickets[-1]
        if self.wavetickets[-1].price_wave > self.maxwave.price_wave:
            self.maxwave = self.wavetickets[-1]
        if self.wavetickets[-1].price_wave - self.maxwave.price_wave < (0-self.rongren) and self.maxwave.price_wave > self.y:
            self.topwaves.append(self.maxwave)
            self.maxwave = None
        
        
                      
        
        
        
        
        # Wait for enough bars to be available to calculate SMA and RSI.
        
 
    def enterLongSignal(self, bar):#当短周期上穿 长周期，就入场做多，seg也要同方向
        return self.__shortSMA[-1] > self.__longSMA[-1] and self.__shortSMA[-1] - self.__longSMA[-1] < 15 
 
    def exitLongSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 1 and bar.getBid1() != 0
 
    def enterShortSignal(self, bar):#当短周期下穿 长周期，就入场做空，seg也要同方向
        return self.__shortSMA[-1] < self.__longSMA[-1] and self.__longSMA[-1] - self.__shortSMA[-1] < 15 
 
    def exitShortSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 2 and bar.getAsk1() != 0

    

def printLog(log):
    appconsant.logLogger.info(log)


def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    
    rootdir = appconsant.rootdir
    
    instrumentID = appconsant.instrumentID
    date = appconsant.date
    
    appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+'log.txt', loglevel=1, logger="log").getlog()
    
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
    
#     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
     
#     logfile = appconsant.logfile
    # Evaluate the strategy with the feed's bars.
    #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    myStrategy = MyStrategyRSI(feed,instrumentID, 660,200,100,57,45)
     
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
    plt.getOrCreateSubplot("wave").addDataSeries("waveds", myStrategy.getWave())
    # plt.getInstrumentSubplot("orcl").addDataSeries("longSMA", myStrategy.getlongSMA())
    # plt.getInstrumentSubplot("orcl").addDataSeries("shortSMA", myStrategy.getshortSMA())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("segmentDS", myStrategy.getsegment())
    # plt.getInstrumentSubplot("orcl").addDataSeries("RSI", myStrategy.getRSI())
     
    # Plot the simple returns on each bar.
    # plt.getInstrumentSubplot("returns").addDataSeries("rsi", myStrategy.getRSI())
    # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
     
    # Run the strategy. 
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
     
    
    waves = []
    u = 0
    x = 0
    for waveticket in myStrategy.getwavetickets():
        u += 1
        
        waves.append(round(waveticket.price_wave,2))
        
    waveseries = dataseries.SequenceDataSeries(50000)
    waves.sort()
    wave = waves[0]
    frequency = 0
    for w in waves:
        if w != wave:
#             print ' '+str(wave)+' '+str(frequency)
            waveseries.appendWithDateTime(wave,frequency)
            frequency = 0
        frequency += 1
        wave = w
    
    
    
    plt.plotdiff(waveseries)
#     plt.plot()
    print '总数:'+str(len(myStrategy.getTopwaves()))
    
    


#     print 'money_in = '+str(appconsant.money_in)+'money_out = '+str(appconsant.money_out)+'money_earn = '+str(appconsant.money_earn)+'market_time ='+str(appconsant.market_time)


# g = 
# print 

if __name__=="__main__": main()
