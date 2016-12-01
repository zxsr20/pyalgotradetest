#!/usr/bin/python
#-*- coding=utf-8 -*-
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

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
        
        self.rongren = 4 #can skip num
        self.skipNum = 0
        self.maprice = 0
        self.preid = -1 #remember the preid
        self.bNewSeg = False;
        self.nDir = 0;
        self.__segmentDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.allSegPankous = []#store the pankou data
        self.__entrySMA = ma.SMA(self.__priceDS, entrySMA)
        self.__exitSMA = ma.SMA(self.__priceDS, exitSMA)
        self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
        self.__overBoughtThreshold = overBoughtThreshold
        self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None

    def getPrice(self):
        return self.__priceDS
    
    def getsegment(self):
        return self.__segmentDS

    def getEntrySMA(self):
        return self.__entrySMA

    def getExitSMA(self):
        return self.__exitSMA

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

    def generateSegPankoubyNum(self,datetime,price):
        if self.skipNum == 0:#if the turn is first
            self.preid = len(self.__priceDS)
            self.skipNum = 1
        elif self.preid == len(self.__priceDS)-1: 
            self.skipNum += 1#if the turn is close to preid
        else:#if the turn is far from preid
            self.skipNum = 1
            self.preid = len(self.__priceDS)
        print 'self.skipNum:'+str(self.skipNum)
        if self.skipNum >= self.rongren:#if turn number is bigger than rongren
            tp = CSegPankou()
            tp.idx = len(self.allSegPankous)+1
            tp.tick_idx_start = len(self.__priceDS)
            tp.tick_idx_end = 0
            if self.__priceDS[-2] > self.__priceDS[-1]:
                tp.dir = 2
            elif self.__priceDS[-2] < self.__priceDS[-1]:
                tp.dir = 1
            else:
                tp.dir = 3
            self.skipNum = 0
            self.__segmentDS.appendWithDateTime(datetime,price)
            self.allSegPankous[-1].tick_idx_end = len(self.__priceDS) #set prepankou end 
            self.allSegPankous.append(tp)
            
#     def generateSegPankou(self,datetime,price):
        
            
    

    def onBars(self, bars):
        
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        
#         print 'self.__priceDS[-1]'+str(self.__priceDS[-1])
        self.bNewSeg = False;
        self.nDir = 0
        if len(self.__priceDS) == 1:
            op = CSegPankou()
            op.idx = 1
            op.tick_idx_start = 1
            op.tick_idx_end = 1
            op.dir = -1
             
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
            self.__segmentDS.appendWithDateTime(bar.getDateTime(),bar.getPrice())
#             print 'endseg DateTime:'+str(bar.getDateTime())+'Price:'+str(bar.getPrice())
#             print 'newseg dir:'+str(self.nDir)+'DateTime:'+str(bar.getDateTime())+'Price:'+str(bar.getPrice())
            self.allSegPankous[-1].tick_idx_end = len(self.__priceDS) #set prepankou end 
            self.allSegPankous.append(tp)
        else:
            #不是最新的段
            if (self.allSegPankous[-1].dir == 1) :
                #本段还是在上涨
                if(self.allSegPankous[-1].upper < self.__priceDS[-1]) :
                    self.allSegPankous[-1].upper = self.__priceDS[-1];
            elif (self.allSegPankous[-1].dir == 2) :
                if(self.allSegPankous[-1].lower > self.__priceDS[-1]) :
                    self.allSegPankous[-1].lower = self.__priceDS[-1];
            
        
        
#         if self.allSegPankous[-1].dir == 1 and self.__priceDS[-2] >= self.__priceDS[-1]:#when turn occur
#             self.generateSegPankoubyNum(bar.getDateTime(),bar.getPrice())
#         if self.allSegPankous[-1].dir == 2 and self.__priceDS[-2] <= self.__priceDS[-1]:#when turn occur
#             self.generateSegPankoubyNum(bar.getDateTime(),bar.getPrice())
#         if self.allSegPankous[-1].dir == 3 and self.__priceDS[-2] != self.__priceDS[-1]:#when turn occur
#             self.generateSegPankoubyNum(bar.getDateTime(),bar.getPrice())
        
        
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__exitSMA[-1] is None or self.__entrySMA[-1]  is None or self.__rsi[-1] is None:
            return
#         print  'rsi:'+str(self.__rsi[-1])
        if self.__longPos is not None:
            if self.exitLongSignal():
                self.__longPos.exitMarket()
#                 print 'shortSMA:'+str(self.__exitSMA[-1])+'longSMA:'+str(self.__entrySMA[-1])+'minus:'+str(self.__exitSMA[-1] - self.__entrySMA[-1])+'rsi:'+str(self.__rsi[-1])
#                 print '做多平仓'
        elif self.__shortPos is not None:
            if self.exitShortSignal():
                self.__shortPos.exitMarket()
#                 print 'shortSMA:'+str(self.__exitSMA[-1])+'longSMA:'+str(self.__entrySMA[-1])+'minus:'+str(self.__entrySMA[-1] - self.__exitSMA[-1])+'rsi:'+str(self.__rsi[-1])
#                 print '做空平仓'
        else:
            if self.enterLongSignal(bar):
#                 print 'stragety'+str(bars[self.__instrument].getPrice())
                shares = 1
#                 print 'shortSMA:'+str(self.__exitSMA[-1])+'longSMA:'+str(self.__entrySMA[-1])
#                 print '做多之前我的钱:'+str(self.getBroker().getCash())
                self.__longPos = self.enterLong(self.__instrument, shares, True)
                    
            elif self.enterShortSignal(bar):
                shares = 1
#                 print 'shortSMA:'+str(self.__exitSMA[-1])+'longSMA:'+str(self.__entrySMA[-1])
#                 print '做空之前我的钱'+str(self.getBroker().getCash())
                self.__shortPos = self.enterShort(self.__instrument, shares, True)
 
    def enterLongSignal(self, bar):#当短周期上穿 长周期，就入场做多，seg也要同方向
        return self.__exitSMA[-1] > self.__entrySMA[-1] and self.__exitSMA[-1] - self.__entrySMA[-1] < 15 and self.__rsi[-1] <= self.__overSoldThreshold and self.allSegPankous[-1].dir == 1
 
    def exitLongSignal(self):#seg转向就平仓
        return self.allSegPankous[-1].dir != 1
 
    def enterShortSignal(self, bar):#当短周期下穿 长周期，就入场做空，seg也要同方向
        return self.__exitSMA[-1] < self.__entrySMA[-1] and self.__entrySMA[-1] - self.__exitSMA[-1] < 15 and self.__rsi[-1] >= self.__overBoughtThreshold and self.allSegPankous[-1].dir == 2
 
    def exitShortSignal(self):#seg转向就平仓
        return self.allSegPankous[-1].dir != 2

    



# Load the yahoo feed from the CSV file
# feed = yahoofeed.Feed()toting
# feed.addBarsFromCSV("orcl", "orcl-2000.csv")

# feed = yahoofeed.Feed()
# feed.addBarsFromCSV("orcl", "20150518.csv")
# 
# # Evaluate the strategy with the feed's bars.
# #(self, feed, instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
# myStrategy = MyStrategyRSI(feed, "orcl", 660,200,100,57,45)
# 
# # Attach a returns analyzers to the strategy.
# returnsAnalyzer = returns.Returns()
# myStrategy.attachAnalyzer(returnsAnalyzer)
# 
# # Attach the plotter to the strategy.
# plt = plotter.StrategyPlotter(myStrategy)
# # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
# 
# # plt.getInstrumentSubplot("orcl").addDataSeries("price", myStrategy.getPrice())
# plt.getInstrumentSubplot("orcl").addDataSeries("entrySMA", myStrategy.getEntrySMA())
# plt.getInstrumentSubplot("orcl").addDataSeries("exitSMA", myStrategy.getExitSMA())
# plt.getInstrumentSubplot("orcl").addDataSeries("segmentDS", myStrategy.getsegment())
# # plt.getInstrumentSubplot("orcl").addDataSeries("RSI", myStrategy.getRSI())
# 
# # Plot the simple returns on each bar.
# plt.getInstrumentSubplot("returns").addDataSeries("rsi", myStrategy.getRSI())
# # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
# 
# # Run the strategy. 
# myStrategy.run()
# myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
# 
# # for x in myStrategy.getsegment():
# #     print x
# # myStrategy.getsegment().pprint()
# # Plot the strategy.
# plt.plot()





# g = 
# print 
