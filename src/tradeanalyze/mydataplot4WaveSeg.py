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

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,nwaveticket,waveseg_y,waveseg_x,rongren):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
#         self.__price_index = 0
#         self.logfile = appconsant.logfile
        
        #wave相关
        self.wavetickets = []
        self.high = 0.0
        self.lower = 0.0
        
        self.nwaveticket = nwaveticket
        self.waveseg_y = waveseg_y
        self.waveseg_x = waveseg_x
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        #seg相关
        self.rongren = rongren #can skip num
        self.bNewSeg = False;
        self.nDir = 0;
        self.__segmentDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.allSegPankous = []#store the pankou data
        
        #测落相关
        self.wavedir = 0
        self.stoploss = 0.0
        
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
        appconsant.logLogger.info(barLog)
        
        
        
        
        
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
        appconsant.logLogger.info('wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave))
        
        self.wavetickets.append(tp)
        
        self.bNewSeg = False;
        self.nDir = 0
        
        if len(self.__priceDS) == 1:
            op = CSegPankou()
            op.idx = 1
            op.tick_idx_start = 1
            op.tick_idx_end = 1
            op.dir = -1
            op.price_start = bar.getPrice()
            self.__segmentDS.appendWithDateTime(bar.getDateTime(),bar.getPrice()) #store into segmentds
            self.allSegPankous.append(op)
            return
        if len(self.__priceDS) == 2:#the second point

            if self.__priceDS[-2] < self.__priceDS[-1]:
                self.allSegPankous[-1].dir = 1 #up
            if self.__priceDS[-2] > self.__priceDS[-1]:
                self.allSegPankous[-1].dir = 2 #down
#             if self.__priceDS[-2] == self.__priceDS[-1]:
#                 self.allSegPankous[-1].dir = 3 #equal
            self.allSegPankous[-1].upper = self.allSegPankous[-1].lower = self.__priceDS[-2] 
            
            
            return
        
        if(self.allSegPankous[-1].dir == 1):
            #在上涨中
            if (self.allSegPankous[-1].upper - self.__priceDS[-1] > self.rongren) :
                self.bNewSeg = True;
                self.nDir = 2;   #下降太多，开始下跌

        elif (self.allSegPankous[-1].dir == 2) :
            #下跌中
            if (self.__priceDS[-1] - self.allSegPankous[-1].lower > self.rongren) :
                self.bNewSeg = True;
                self.nDir = 1;   #下降太多，开始下跌
                
        if self.bNewSeg:
            tp = CSegPankou()
            tp.idx = len(self.allSegPankous)+1
            tp.dir = self.nDir;
            tp.tick_idx_start = tp.tick_idx_end = len(self.__priceDS)
            tp.lower = tp.upper = self.__priceDS[-1];
            tp.price_start = bar.getPrice()
            self.__segmentDS.appendWithDateTime(bar.getDateTime(),bar.getPrice())
            
            self.allSegPankous[-1].price_end = bar.getPrice()
            if self.allSegPankous[-1].dir == 1:
                self.allSegPankous[-1].diffpri = self.allSegPankous[-1].price_end-self.allSegPankous[-1].price_start
            else:
                self.allSegPankous[-1].diffpri = self.allSegPankous[-1].price_start-self.allSegPankous[-1].price_end
#             if self.__shortSMA[-1] != None and self.__longSMA[-1] != None and cross.cross_above(self.__shortSMA,self.__longSMA) and self.nDir == 1:
            
            self.allSegPankous[-1].tick_idx_end = len(self.__priceDS) #set prepankou end 
            appconsant.logLogger.info('endseg1 idx:'+str(tp.idx-1)+' tick_idx_end:'+ str(self.allSegPankous[-1].tick_idx_end) +' dir:'+ str(self.allSegPankous[-1].dir)+' DateTime:'+barTime+' Price:'+str(bar.getPrice())+' seglow:'+ str(self.allSegPankous[-1].lower) +' segHigh:'+ str(self.allSegPankous[-1].upper) +' diffpri:'+ str(self.allSegPankous[-1].diffpri))
            
            appconsant.logLogger.info('newseg1 idx:'+str(tp.idx)+' tick_idx_start:'+ str(self.allSegPankous[-1].tick_idx_end) +' dir:'+str(self.nDir)+' DateTime:'+barTime+' Price:'+str(bar.getPrice()))
            
            tp.tongji = 1
#             if self.__shortSMA[-1] != None and self.__longSMA[-1] != None and self.__shortSMA[-1]>self.__longSMA[-1]  and self.__shortSMA[-1] > self.__shortSMA[-2]  and self.nDir == 1:
#     
#                 print >> self.logfile,'本段需要统计：self.__shortSMA[-1]>self.__longSMA[-1] and self.__shortSMA[-1] > self.__shortSMA[-2] and self.nDir == 1'+' self.__shortSMA[-1]:'+str(self.__shortSMA[-1])+'self.__longSMA[-1]:'+str(self.__longSMA[-1])
#                 tp.tongji = 1
# #             elif self.__shortSMA[-1] != None and self.__longSMA[-1] != None and cross.cross_below(self.__longSMA,self.__shortSMA) and self.nDir == 2:
#             elif self.__shortSMA[-1] != None and self.__longSMA[-1] != None and self.__longSMA[-1]>self.__shortSMA[-1] and self.__shortSMA[-1] < self.__shortSMA[-2] and self.nDir == 2:
#            
#                 print >> self.logfile,'本段需要统计：self.__shortSMA[-1]<self.__longSMA[-1] and self.__shortSMA[-1] < self.__shortSMA[-2] and self.nDir == 2'+' self.__shortSMA[-1]:'+str(self.__shortSMA[-1])+'self.__longSMA[-1]:'+str(self.__longSMA[-1])
#                 tp.tongji = 1
            self.allSegPankous.append(tp)
        else:
            #不是最新的段
            if (self.allSegPankous[-1].dir == 1) :
                #本段还是在上涨
                if(self.allSegPankous[-1].upper < self.__priceDS[-1]) :
                    self.allSegPankous[-1].upper = self.__priceDS[-1];
                if(self.allSegPankous[-1].lower > self.__priceDS[-1]) :
                    self.allSegPankous[-1].lower = self.__priceDS[-1];
            elif (self.allSegPankous[-1].dir == 2) :
                if(self.allSegPankous[-1].lower > self.__priceDS[-1]) :
                    self.allSegPankous[-1].lower = self.__priceDS[-1];
                if(self.allSegPankous[-1].upper < self.__priceDS[-1]) :
                    self.allSegPankous[-1].upper = self.__priceDS[-1];
        
        
        
        #当wave
        if self.__longPos is not None or self.__shortPos is not None:
            if self.__longPos is not None:
                if self.__priceDS[-1] < self.stoploss:
                    appconsant.logLogger.info('当前价格小于止损点,准备离场'+str(self.__priceDS[-1])+' <'+str(self.stoploss))
                    self.__longPos.exitMarket()
                    self.wavedir = 0
                    appconsant.logLogger.info('做多平仓')
                elif self.allSegPankous[-1].dir == 2:
                    appconsant.logLogger.info('当前seg为降，准备离场')
                    self.__longPos.exitMarket()
                    self.wavedir = 0
                    appconsant.logLogger.info('做多平仓')
            if self.__shortPos is not None:
                if self.__priceDS[-1] > self.stoploss:
                    appconsant.logLogger.info('当前价格大于止损点,准备离场'+str(self.__priceDS[-1])+' >'+str(self.stoploss))
                    self.__shortPos.exitMarket()
                    self.wavedir = 0
                    appconsant.logLogger.info('做空平仓')
                elif self.allSegPankous[-1].dir == 1:
                    appconsant.logLogger.info('当前seg为升，准备离场')
                    self.__shortPos.exitMarket()
                    self.wavedir = 0
                    appconsant.logLogger.info('做空平仓')
        else:  
            if self.wavedir == 0:
                if self.wavetickets[-1].price_wave > self.waveseg_y:
                    if self.__priceDS[-1] == self.wavetickets[-1].upper:
                        appconsant.logLogger.info('当前波动大于y'+str(self.waveseg_y)+'，并且当前价格为最高点，开始记录')
                        self.wavedir = 1
        #                 self.stoploss = self.__priceDS[-1]
                    if self.__priceDS[-1] == self.wavetickets[-1].lower:
                        appconsant.logLogger.info('当前波动大于y'+str(self.waveseg_y)+'，并且当前价格为最低点，开始记录')
                        self.wavedir = 2
        #                 self.stoploss = self.__priceDS[-1]
            elif self.wavedir != 0:
                if  self.wavetickets[-1].price_wave < self.waveseg_x:
                    if self.wavedir == 1:
                        appconsant.logLogger.info('当前波动开始小于x'+str(self.waveseg_x)+'，准备做空,止损点为本波段最大值'+str(self.wavetickets[-1].upper))
                        shares = 1
    #                     if self.__shortSMA[-1] is not None and  self.__longSMA[-1]  is not None and self.__rsi[-1] is  not None:
    #                         print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))
                        appconsant.logLogger.info('做空之前我的钱'+str(self.getBroker().getCash()))
                        self.stoploss = self.wavetickets[-1].upper
                        self.__shortPos = self.enterShort(self.__instrument, shares, True)
                        
                    if self.wavedir == 2:
                        appconsant.logLogger.info('当前波动开始小于x'+str(self.waveseg_x)+'，准备做多，止损点为本波段最小值'+str(self.wavetickets[-1].lower))
                        shares = 1
    #                     if self.__shortSMA[-1] is not None and  self.__longSMA[-1]  is not None and self.__rsi[-1] is  not None:
    #                         print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))
                        appconsant.logLogger.info('做多之前我的钱:'+str(self.getBroker().getCash()))
                        self.stoploss = self.wavetickets[-1].lower
                        self.__longPos = self.enterLong(self.__instrument, shares, True)
                      
        
        
        
        
        # Wait for enough bars to be available to calculate SMA and RSI.
        
 
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
    
    rootdir = appconsant.rootdir
    
    instrumentID = appconsant.instrumentID
    date = appconsant.date
    
    appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+'log.txt', loglevel=1, logger="log").getlog()
     
#     instrumentID = "rb1510"
    
    
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
    myStrategy = MyStrategyRSI(feed,instrumentID, 660,200,100,57,45,appconsant.waveseg_nwaveticket,appconsant.waveseg_y,appconsant.waveseg_x,appconsant.waveseg_rongren)
    
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
    
    
    
#     plt.plotdiff(waveseries)
    plt.plot()


#     print 'money_in = '+str(appconsant.money_in)+'money_out = '+str(appconsant.money_out)+'money_earn = '+str(appconsant.money_earn)+'market_time ='+str(appconsant.market_time)


# g = 
# print 

if __name__=="__main__": main()
