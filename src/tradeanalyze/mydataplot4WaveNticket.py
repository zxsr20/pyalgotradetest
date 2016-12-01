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
from spyderlib import DATAPATH

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
#         self.__price_index = 0
        self.wavetickets = []
        self.high = 0.0
        self.lower = 0.0
        
        self.__nwaveticket = 2000
        
        self.equalcount = 0
        self.equalcount2 = 0
        self.stress = 0
        self.mincha = 0.0
        self.beginmarket = 0
        
        self.__waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        self.__longPos = None
        self.__shortPos = None

    def getPrice(self):
        return self.__priceDS
    
    def getwavetickets(self):
        return self.wavetickets
    
    def getWave(self):
        return self.__waveDS

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
#         print >> self.logfile,barLog
        if len(self.__priceDS) == 100:
            chalist = []
            for i in range(99):
                if abs(self.__priceDS[i+1] - self.__priceDS[i]) != 0:
                    chalist.append(abs(self.__priceDS[i+1] - self.__priceDS[i]))
            print chalist
            self.mincha = min(chalist)
            print self.mincha
        
        
        tp = CTicketWave()
        tp.idx = len(self.wavetickets)+1
        tick_idx_start = len(self.__priceDS) - self.__nwaveticket
        if tick_idx_start < 0:
            tick_idx_start = 0
        tp.tick_idx_start = tick_idx_start
        tp.tick_idx_end = len(self.__priceDS)-1
        tp.price_start = self.__priceDS[tick_idx_start]
        tp.price_end = self.__priceDS[-1]
        priceds = self.__priceDS[tick_idx_start:len(self.__priceDS)]
        tp.upper = max(priceds)
        tp.lower = min(priceds)
        i1 = priceds.index(tp.upper)
        i2 = priceds.index(tp.lower)
        if i1 > i2:
            tp.price_wave =  tp.upper - tp.lower
        else:
            tp.price_wave =  -(tp.upper - tp.lower)
#         print ' '+str(tp.price_wave)
        self.__waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
#         print >> self.logfile,'wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave)
        
        self.wavetickets.append(tp)
        
        if len(self.__waveDS) > 1:
                if ((self.__waveDS[-2] > 0 and self.__waveDS[-1] < 0) or (self.__waveDS[-1] < 0 and self.__waveDS[-2] > 0)) :
                    self.stress = self.__waveDS[-1]
                    self.beginmarket = 1
                    print 'self.stress'+str(self.stress)
                    print 'abs(self.__waveDS[-1]) - abs(self.stress)'+str(abs(self.__waveDS[-1]) - abs(self.stress))
                if ((self.stress < 0 and self.__waveDS[-1] < 0) or (self.stress > 0 and self.__waveDS[-1] > 0)) and abs(self.__waveDS[-1]) - abs(self.stress) >=3*self.mincha:
                    
                    if self.__waveDS[-2] == self.__waveDS[-1]:
                        self.equalcount += 1
                    else:
                        self.equalcount = 0
                    print 'self.equalcount'+str(self.equalcount)
                    if self.equalcount > 3 and self.beginmarket == 1:
                        if self.__waveDS[-1] > 0:
                            shares = 1
                            printLog(self.__instrument+'self.equalcount > 6做空之前我的钱'+str(self.getBroker().getCash()))
                            self.__shortPos11 = self.enterShort(self.__instrument, shares, True)
                            self.beginmarket = 0
                        elif self.__waveDS[-1] < 0:
                            shares = 1
                            printLog(self.__instrument+'self.equalcount > 6做多之前我的钱'+str(self.getBroker().getCash()))
                            self.__longPos11 = self.enterLong(self.__instrument, shares, True)
                            self.beginmarket = 0
                else:
                    self.equalcount = 0
                    
        
#         if self.__shortSMA[-1] is  None or  self.__longSMA[-1]  is  None:
#             return        
#         
#         
#         if self.__longPos is not None or self.__shortPos is not None:
#             if self.__priceDS[-1] > self.high:
#                 self.high = self.__priceDS[-1]
# #                 print >> self.logfile,' newhigh:'+str(self.high)
#             if self.__priceDS[-1] < self.lower:
#                 self.lower = self.__priceDS[-1]
# #                 print >> self.logfile,' newlower:'+str(self.lower)
#         
#         if self.__longPos is not None:
#             print >> self.logfile,' 从最大值回撤:'+str(self.high - self.__priceDS[-1])+'小于'+str(self.__wave_a)
#             if self.high - self.__priceDS[-1] >= self.__wave_a:
#                 print >> self.logfile,'从最大值回撤'+str(self.high - self.__priceDS[-1])+' high:'+str(self.high)+' price:'+str(self.__priceDS[-1])
#                 self.__longPos.exitMarket()
# #                 if self.__shortSMA[-1] is not None and  self.__longSMA[-1]  is not None and self.__rsi[-1] is  not None:
# #                     print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))+' minus:'+str(round((self.__shortSMA[-1] - self.__longSMA[-1]),3))+' rsi:'+str(round(self.__rsi[-1],3))
#                 print >> self.logfile,'做多平仓'
#             
#         elif self.__shortPos is not None:
#             print >> self.logfile,' 从最小值回撤:'+str(self.high - self.__priceDS[-1])+'小于'+str(self.__wave_a)
#             if self.__priceDS[-1] - self.lower >= self.__wave_a:
#                 print >> self.logfile,'从最小值回撤'+str(self.__priceDS[-1] - self.lower)+' lower:'+str(self.lower)+' price:'+str(self.__priceDS[-1])
#                 self.__shortPos.exitMarket()
# #                 if self.__shortSMA[-1] is not None and  self.__longSMA[-1]  is not None and self.__rsi[-1] is  not None:
# #                     print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))+' minus:'+str(round((self.__shortSMA[-1] - self.__longSMA[-1]),3))+' rsi:'+str(round(self.__rsi[-1],3))
#                 print >> self.logfile,'做空平仓'
#         else:
#             if self.wavetickets[-1].price_wave >= self.__wave_y:
#                 if self.__priceDS[-1] == self.wavetickets[-1].upper and self.enterLongSignal(bar):
#                     shares = 1
# #                     if self.__shortSMA[-1] is not None and  self.__longSMA[-1]  is not None and self.__rsi[-1] is  not None:
# #                         print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))
#                     print >> self.logfile,'做多之前我的钱:'+str(self.getBroker().getCash())
#                     self.__longPos = self.enterLong(self.__instrument, shares, True)
#                 elif self.__priceDS[-1] == self.wavetickets[-1].lower and self.enterShortSignal(bar):
#                     shares = 1
# #                     if self.__shortSMA[-1] is not None and  self.__longSMA[-1]  is not None and self.__rsi[-1] is  not None:
# #                         print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))
#                     print >> self.logfile,'做空之前我的钱'+str(self.getBroker().getCash())
#                     self.__shortPos = self.enterShort(self.__instrument, shares, True)
# #                 else:
# # #                     print >> self.logfile,'wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave)
# #                     
# #                     print >> self.logfile,''
#                 self.high = self.__priceDS[-1]
#                 self.lower = self.__priceDS[-1]
        
        
        
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
    print log


def main(datestr,instru):
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    
    rootdir = 'D:\pyTest_yh\data\\'
     
    instrumentID = appconsant.instrumentID
    instrumentID = instru
    date = datestr
    
    #数据转化
#     for f in os.listdir(rootdir):  
#         file = os.path.join(rootdir, f)  
#         filename = file.split("\\")[-1].split(".")[0]
#         
#         if os.path.isfile(file) and filename == date:   
#             print '原始文件:'+file
#             data_lines = data.getDayData(instrumentID,file) #获取数据
#             data_config = conf.getInstrumentInfo(instrumentID) 
#             csvfile = filename + instrumentID +'.csv'
# #             res=StoreCsv.process(data_lines,data_config,csvfile,malength=90)
#             data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
    
    
    
#     instrumentID = appconsant.instrumentID
    
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
    
#     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
     
    # Evaluate the strategy with the feed's bars.
    #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    myStrategy = MyStrategyRSI(feed,instrumentID)
     
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
     
    
    
    
#     plt.plotdiff(waveseries)
    plt.plot()




# g = 
# print 

if __name__=="__main__": 
#     mydatapath = 'E:\\Users\\ct\\workspace\\PyBuilder\\pyalgotradetest\\src\\tradeanalyze\\' 
#     datestr = '20151030'
#     for f in os.listdir(mydatapath):  
#         filecompletepath = os.path.join(mydatapath, f)  
#         filename = filecompletepath.split("\\")[-1].split(".")[0]
#         
#         if datestr in filename:
#             print filename[0:8]+' '+filename[8:]
#             main(filename[0:8],filename[8:])
    main('20131218','y1405')