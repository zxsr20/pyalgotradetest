#!/usr/bin/python
#-*- coding=utf-8 -*-
import sys,os
import conf,data
import itertools
import time
from pyalgotrade.optimizer import local
from tradeanalyze import appconsant, StoreCsv4Nticket

from pyalgotrade import plotter, dataseries
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import strategy
from pyalgotrade.technical import ma, macd
from pyalgotrade.technical import rsi
from pyalgotrade.technical import cross
from pyalgotrade.dataseries import DataSeries
import tradeanalyze.data_struct
from tradeanalyze.data_struct import *
from astropy import logging



class MyStrategyRSI1(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,nwaveticket,waveseg_y,waveseg_x,rongren):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
#         self.__price_index = 0
#         self.logfile = appconsant.logfile
        self.__bigpriceDS = dataseries.SequenceDataSeries(100000)
        
#         self.ticketidx = ticketidx
        #wave相关
        self.wavetickets = []
        self.high = 0.0
        self.lower = 0.0
        
        self.nwaveticket = nwaveticket
        self.waveseg_y = waveseg_y
        self.waveseg_x = waveseg_x
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        data_config = conf.getInstrumentInfo(instrument) 
        
        self.rangespan_nwaveticket = 200
        self.rangespan_stoploss = 20 * data_config.PriceTick
        self.rangespan_n = 200
        #seg相关
        self.rongren = rongren #can skip num
        self.bNewSeg = False;
        self.nDir = 0;
        self.__segmentDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.allSegPankous = []#store the pankou data
        
        self.buyprice = 0.0
        self.nonewtop = 0
        self.topprice = 0.0
        
        self.nonewmacdtop = 0
        self.topplusmacd = 0.0
        self.topminusmacd = 0.0
        
        self.moneyearn = []
        self.moneyloss = []
        self.lastmymoney = 1000000
        self.losstime = 0
        self.wintime = 0
        self.winmoney = 0.0
        self.lossmoney = 0.0
        #测落相关
        self.wavedir = 0
        self.stoploss = 0.0
        
        
        
#         self.__longSMA = ma.SMA(self.__priceDS, longSMA)
#         self.__shortSMA = ma.SMA(self.__priceDS, shortSMA)
#         self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
#         self.__overBoughtThreshold = overBoughtThreshold
#         self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None
        
        self.shortema = 50
        self.longema = 110
        self.signema = 30
#         self.__longEMA = ma.SMA(self.__priceDS, 300)
#         self.__shortEMA = ma.SMA(self.__priceDS, 50)
#         self.macdDs = macd.MACD(self.__priceDS,5,13,6)
#         self.macdDs = macd.MACD(self.__priceDS,self.shortema,self.longema,self.signema)
#         self.hisDs = self.macdDs.getHistogram()
#         self.pingwenDs =dataseries.SequenceDataSeries(100000)#use to draw map
        
        self.lowband = -0.00022
        self.upband = 0.00032
        self.bandbl = 1.2
        self.outlowband = self.lowband * self.bandbl
        self.outupband = self.upband * self.bandbl
        
        
    def getPrice(self):
        return self.__priceDS
    def getmarketinfo(self): 
        return '交易次数:'+str(self.wintime+self.losstime)+'盈利次数:'+str(self.wintime)+'亏损次数:'+str(self.losstime)+'盈利额:'+str(self.winmoney)+'亏损额:'+str(self.lossmoney)
    def getmoneyearn(self):
        return self.moneyearn
    def getmoneyloss(self):
        return self.moneyloss
    def getmacdDs(self):
        return self.macdDs
    def getpingwenDs(self):
        return self.pingwenDs
    
    def gethisDs(self):
        return self.hisDs
    def getwavetickets(self):
        return self.wavetickets
    
    def getallseg(self):
        return self.allSegPankous
    
    def getWave(self):
        return self.waveDS
    
    def getseg(self):
        return self.__segmentDS

    def getlongSMA(self):
        return self.__longSMA

    def getshortSMA(self):
        return self.__shortSMA
    
    def getlongEMA(self):
        return self.__longEMA

    def getshortEMA(self):
        return self.__shortEMA

    def getRSI(self):
        return self.__rsi
    
    def getbigprice(self):
        return self.__bigpriceDS

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
        

#         
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
#             appconsant.logLogger.info('endseg1 idx:'+str(tp.idx-1)+' tick_idx_end:'+ str(self.allSegPankous[-1].tick_idx_end) +' dir:'+ str(self.allSegPankous[-1].dir)+' DateTime:'+barTime+' Price:'+str(bar.getPrice())+' seglow:'+ str(self.allSegPankous[-1].lower) +' segHigh:'+ str(self.allSegPankous[-1].upper) +' diffpri:'+ str(self.allSegPankous[-1].diffpri))
             
#             appconsant.logLogger.info('newseg1 idx:'+str(tp.idx)+' tick_idx_start:'+ str(self.allSegPankous[-1].tick_idx_end) +' dir:'+str(self.nDir)+' DateTime:'+barTime+' Price:'+str(bar.getPrice()))
             
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


def printLog(log):
    pass
def main(rongren):
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    
    rootdir = appconsant.rootdir
    
    instrumentID = appconsant.instrumentID
    date = appconsant.date
    
    ISOTIMEFORMAT='%Y-%m-%d%H%M%S'
    
     
#     instrumentID = "rb1510"
    
    
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
    
#     feed = yahoofeed.Feed()
#     feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
#     
# #     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
#      
# #     logfile = appconsant.logfile
#     # Evaluate the strategy with the feed's bars.
#     #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
#     myStrategy4 = MyStrategyRSI4(feed,instrumentID, 660,200,100,57,45,appconsant.waveseg_nwaveticket,appconsant.waveseg_y,appconsant.waveseg_x,appconsant.waveseg_rongren)
#     
#     # Attach a returns analyzers to the strategy.
# #     returnsAnalyzer = returns.Returns()
# #     myStrategy.attachAnalyzer(returnsAnalyzer)
# #      
# #     # Attach the plotter to the strategy.
# #     plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
# #     # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
# #      
# #     plt.getOrCreateSubplot("wave").addDataSeries("waveds", myStrategy.getWave())
#     # plt.getInstrumentSubplot("orcl").addDataSeries("longSMA", myStrategy.getlongSMA())
#     # plt.getInstrumentSubplot("orcl").addDataSeries("shortSMA", myStrategy.getshortSMA())
# #     plt.getInstrumentSubplot(instrumentID).addDataSeries("segmentDS", myStrategy.getsegment())
#     # plt.getInstrumentSubplot("orcl").addDataSeries("RSI", myStrategy.getRSI())
#      
#     # Plot the simple returns on each bar.
#     # plt.getInstrumentSubplot("returns").addDataSeries("rsi", myStrategy.getRSI())
#     # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
#      
#     # Run the strategy. 
#     myStrategy4.run()
    
    
    
#     myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
#     if len(myStrategy4.getticketidx())%2 == 1:
#         myStrategy4.getticketidx().append(len(data_lines)-1)
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
    myStrategy1 = MyStrategyRSI1(feed,instrumentID, 660,200,100,57,45,appconsant.waveseg_nwaveticket,appconsant.waveseg_y,appconsant.waveseg_x,rongren)
    
    returnsAnalyzer = returns.Returns()
    myStrategy1.attachAnalyzer(returnsAnalyzer)
#     plt = plotter.StrategyPlotter(myStrategy1,plotOrder=True)
#     
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("big", myStrategy1.getbigprice())
#     plt.getOrCreateSubplot("macd").addDataSeries("sign", myStrategy1.getmacdDs())
# #     plt.getOrCreateSubplot("his").addDataSeries("his", myStrategy1.gethisDs())
# #     plt.getOrCreateSubplot("seg").addDataSeries("his", myStrategy1.getseg())
# #     plt.getOrCreateSubplot("rsi").addDataSeries("rsi", myStrategy1.getRSI())
#     plt.getOrCreateSubplot("pingwen").addDataSeries("pingwen", myStrategy1.getpingwenDs())
    
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("longEma", myStrategy1.getlongEMA())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("smallEma", myStrategy1.getshortEMA())
    
    myStrategy1.run()
    myStrategy1.info("Final portfolio value: $%.2f" % myStrategy1.getResult())
    
#     printLog(myStrategy1.getmarketinfo())
#      
#     printLog(myStrategy1.getmoneyearn())
#     printLog(myStrategy1.getmoneyloss())
    
    allseg = myStrategy1.getallseg()
    segdiff = []
    for seg in allseg:
        segdiff.append(round(seg.diffpri))
    segseries = dataseries.SequenceDataSeries(50000)
    segdiff.sort()
    diff = segdiff[0]
    frequency = 0
    for w in segdiff:
        if w != diff:
#             print ' '+str(wave)+' '+str(frequency)
            segseries.appendWithDateTime(diff,frequency)
            frequency = 0
        frequency += 1
        diff = w
    
    printLog('容忍度为'+str(rongren)+'时，segdiff的情况：')
    diffs = segseries.getDateTimes()
    frequencys = segseries.getValues()
    
    good = 0
    bad = 0
    for i in range(len(diffs)):
        if diffs[i] < 0:
            bad += frequencys[i]
        else:
            good += frequencys[i]
        printLog('长度为'+str(diffs[i])+'的有'+str(frequencys[i])+'个')
    printLog('正的有'+str(good)+'个，负的有'+str(bad)+'个,百分比是'+str(good/(float)(bad)))
#     plt.plotdiffbar(segseries)
    
#     plt.plot()
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

if __name__=="__main__": 
    rootdir = appconsant.rootdir
    
    instrumentID = appconsant.instrumentID
    date = appconsant.date
    for i in range(100):
        main(i)
