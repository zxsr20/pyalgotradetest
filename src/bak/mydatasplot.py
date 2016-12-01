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
import appconsant

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
        
        self.data_config = conf.getInstrumentInfo(instrument) 
        self.logfile = appconsant.logfile
        self.rongren = appconsant.rongren1 #can skip num
        self.rongren1 = appconsant.rongren2 #can skip num
        self.skipNum = 0
        self.maprice = 0
        self.preid = -1 #remember the preid
        self.bNewSeg = False;
        self.nDir = 0;
        self.__segmentDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.allSegPankous = []#store the pankou data
        
        self.bNewSeg1 = False;
        self.nDir1 = 0;
        self.__segmentDS1 =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.allSegPankous1 = []#store the pankou data
        
        self.__longSMA = ma.SMA(self.__priceDS, longSMA)
        self.__shortSMA = ma.SMA(self.__priceDS, shortSMA)
        self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
        self.__overBoughtThreshold = overBoughtThreshold
        self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None

    def getPrice(self):
        return self.__priceDS
    
    def getsegment(self):
        return self.__segmentDS

    def getlongSMA(self):
        return self.__longSMA

    def getshortSMA(self):
        return self.__shortSMA

    def getRSI(self):
        return self.__rsi
    
    def getAllSeg(self):
        return self.allSegPankous
    
    def getAllSeg1(self):
        return self.allSegPankous1

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
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
        barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
        if (bar.getAsk1()-bar.getBid1()) > self.data_config.PriceTick:
            barLog += ' bigthanOnePriceTick:True'
        if bar.getPrice() > bar.getAsk1():
            barLog += ' priceBigThanAsk1:True'
        if bar.getPrice() < bar.getBid1():
            barLog += ' priceSmallThanBid1:True'
        if bar.getLastPrice() > bar.getAsk1():
            barLog += ' lastpriceBigThanAsk1:True'
        if bar.getLastPrice() < bar.getBid1():
            barLog += ' lastpriceSmallThanBid1:True'
        print >> self.logfile,barLog
        self.bNewSeg = False;
        self.nDir = 0
        
        self.bNewSeg1 = False;
        self.nDir1 = 0
        if len(self.__priceDS) == 1:
            op = CSegPankou()
            op.idx = 1
            op.tick_idx_start = 1
            op.tick_idx_end = 1
            op.dir = -1
            op.price_start = bar.getPrice()
            self.__segmentDS.appendWithDateTime(bar.getDateTime(),bar.getPrice()) #store into segmentds
            self.allSegPankous.append(op)
            
            self.__segmentDS1.appendWithDateTime(bar.getDateTime(),bar.getPrice()) #store into segmentds
            self.allSegPankous1.append(op)
            
            return
        if len(self.__priceDS) == 2:#the second point

            if self.__priceDS[-2] < self.__priceDS[-1]:
                self.allSegPankous[-1].dir = 1 #up
            if self.__priceDS[-2] > self.__priceDS[-1]:
                self.allSegPankous[-1].dir = 2 #down
#             if self.__priceDS[-2] == self.__priceDS[-1]:
#                 self.allSegPankous[-1].dir = 3 #equal
            self.allSegPankous[-1].upper = self.allSegPankous[-1].lower = self.__priceDS[-2] 
            
            self.allSegPankous1[-1].upper = self.allSegPankous1[-1].lower = self.__priceDS[-2] 
            return
        
        if self.__shortSMA[-1] != None and self.__longSMA[-1] != None:
            print >> self.logfile,'shortSMA:'+str(self.__shortSMA[-1])+' longSMA:'+str(self.__longSMA[-1])
            
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
            print >> self.logfile,'endseg1 idx:'+ str(self.allSegPankous[-1].tick_idx_end) +' dir:'+ str(self.allSegPankous[-1].dir)+' DateTime:'+barTime+' Price:'+str(bar.getPrice())+' seglow:'+ str(self.allSegPankous[-1].lower) +' segHigh:'+ str(self.allSegPankous[-1].upper) +' diffpri:'+ str(self.allSegPankous[-1].diffpri)
            
            print >> self.logfile,'newseg1 idx:'+ str(self.allSegPankous[-1].tick_idx_end) +' dir:'+str(self.nDir)+' DateTime:'+barTime+' Price:'+str(bar.getPrice())
            
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
                    
                    
                    
        
#         if len(self.__priceDS) == 1:
#             op = CSegPankou()
#             op.idx = 1
#             op.tick_idx_start = 1
#             op.tick_idx_end = 1
#             op.dir = -1
#             op.price_start = bar.getPrice()
#             self.__segmentDS1.appendWithDateTime(bar.getDateTime(),bar.getPrice()) #store into segmentds
#             self.allSegPankous1.append(op)
#             
#             return
#         if len(self.__priceDS) == 2:#the second point
# 
#             if self.__priceDS[-2] < self.__priceDS[-1]:
#                 self.allSegPankous1[-1].dir = 1 #up
#             if self.__priceDS[-2] > self.__priceDS[-1]:
#                 self.allSegPankous1[-1].dir = 2 #down
# #             if self.__priceDS[-2] == self.__priceDS[-1]:
# #                 self.allSegPankous[-1].dir = 3 #equal
#             self.allSegPankous1[-1].upper = self.allSegPankous1[-1].lower = self.__priceDS[-2] 
#             return
        
        
            
        if(self.allSegPankous1[-1].dir == 1):
            #在上涨中
            if (self.allSegPankous1[-1].upper - self.__priceDS[-1] > self.rongren1) :
                self.bNewSeg1 = True;
                self.nDir1 = 2;   #下降太多，开始下跌

        elif (self.allSegPankous1[-1].dir == 2) :
            #下跌中
            if (self.__priceDS[-1] - self.allSegPankous1[-1].lower > self.rongren1) :
                self.bNewSeg1 = True;
                self.nDir1 = 1;   #下降太多，开始下跌
            
        
        if self.bNewSeg1:
            tp = CSegPankou()
            tp.idx = len(self.allSegPankous1)+1
            tp.dir = self.nDir1;
            tp.tick_idx_start = tp.tick_idx_end = len(self.__priceDS)
            tp.lower = tp.upper = self.__priceDS[-1];
            tp.price_start = bar.getPrice()
            self.__segmentDS1.appendWithDateTime(bar.getDateTime(),bar.getPrice())
            
            self.allSegPankous1[-1].price_end = bar.getPrice()
            if self.allSegPankous1[-1].dir == 1:
                self.allSegPankous1[-1].diffpri = self.allSegPankous1[-1].price_end-self.allSegPankous1[-1].price_start
            else:
                self.allSegPankous1[-1].diffpri = self.allSegPankous1[-1].price_start-self.allSegPankous1[-1].price_end
#             if self.__shortSMA[-1] != None and self.__longSMA[-1] != None and cross.cross_above(self.__shortSMA,self.__longSMA) and self.nDir == 1:
            
            self.allSegPankous1[-1].tick_idx_end = len(self.__priceDS) #set prepankou end 
            print >> self.logfile,'endseg2 idx:'+ str(self.allSegPankous1[-1].tick_idx_end) +' dir:'+ str(self.allSegPankous1[-1].dir)+' DateTime:'+barTime+' Price:'+str(bar.getPrice())+' seglow:'+ str(self.allSegPankous1[-1].lower) +' segHigh:'+ str(self.allSegPankous1[-1].upper) +' diffpri:'+ str(self.allSegPankous1[-1].diffpri)
            
            print >> self.logfile,'newseg2 idx:'+ str(self.allSegPankous1[-1].tick_idx_end) +' dir:'+str(self.nDir1)+' DateTime:'+barTime+' Price:'+str(bar.getPrice())
            
            tp.tongji = 1
#             if self.__shortSMA[-1] != None and self.__longSMA[-1] != None and self.__shortSMA[-1]>self.__longSMA[-1]  and self.__shortSMA[-1] > self.__shortSMA[-2]  and self.nDir1 == 1:
#     
#                 print >> self.logfile,'本段需要统计：self.__shortSMA[-1]>self.__longSMA[-1] and self.__shortSMA[-1] > self.__shortSMA[-2] and self.nDir == 1'+' self.__shortSMA[-1]:'+str(self.__shortSMA[-1])+'self.__longSMA[-1]:'+str(self.__longSMA[-1])
#                 tp.tongji = 1
# #             elif self.__shortSMA[-1] != None and self.__longSMA[-1] != None and cross.cross_below(self.__longSMA,self.__shortSMA) and self.nDir == 2:
#             elif self.__shortSMA[-1] != None and self.__longSMA[-1] != None and self.__longSMA[-1]>self.__shortSMA[-1] and self.__shortSMA[-1] < self.__shortSMA[-2] and self.nDir == 2:
#            
#                 print >> self.logfile,'本段需要统计：self.__shortSMA[-1]<self.__longSMA[-1] and self.__shortSMA[-1] < self.__shortSMA[-2] and self.nDir == 2'+' self.__shortSMA[-1]:'+str(self.__shortSMA[-1])+'self.__longSMA[-1]:'+str(self.__longSMA[-1])
#                 tp.tongji = 1
            self.allSegPankous1.append(tp)
        else:
            #不是最新的段
            if (self.allSegPankous1[-1].dir == 1) :
                #本段还是在上涨
                if(self.allSegPankous1[-1].upper < self.__priceDS[-1]) :
                    self.allSegPankous1[-1].upper = self.__priceDS[-1];
                if(self.allSegPankous1[-1].lower > self.__priceDS[-1]) :
                    self.allSegPankous1[-1].lower = self.__priceDS[-1];
            elif (self.allSegPankous1[-1].dir == 2) :
                if(self.allSegPankous1[-1].lower > self.__priceDS[-1]) :
                    self.allSegPankous1[-1].lower = self.__priceDS[-1];
                if(self.allSegPankous1[-1].upper < self.__priceDS[-1]) :
                    self.allSegPankous1[-1].upper = self.__priceDS[-1];
            
        
        
#         if self.allSegPankous[-1].dir == 1 and self.__priceDS[-2] >= self.__priceDS[-1]:#when turn occur
#             self.generateSegPankoubyNum(bar.getDateTime(),bar.getPrice())
#         if self.allSegPankous[-1].dir == 2 and self.__priceDS[-2] <= self.__priceDS[-1]:#when turn occur
#             self.generateSegPankoubyNum(bar.getDateTime(),bar.getPrice())
#         if self.allSegPankous[-1].dir == 3 and self.__priceDS[-2] != self.__priceDS[-1]:#when turn occur
#             self.generateSegPankoubyNum(bar.getDateTime(),bar.getPrice())
        
        
        # Wait for enough bars to be available to calculate SMA and RSI.
        if self.__shortSMA[-1] is None or self.__longSMA[-1]  is None or self.__rsi[-1] is None:
            return
#         print  'rsi:'+str(self.__rsi[-1])
        if self.__longPos is not None:
            if self.exitLongSignal(bar):
                self.__longPos.exitMarket()
                print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))+' minus:'+str(round((self.__shortSMA[-1] - self.__longSMA[-1]),3))+' rsi:'+str(round(self.__rsi[-1],3))
                print >> self.logfile,'做多平仓'
        elif self.__shortPos is not None:
            if self.exitShortSignal(bar):
                self.__shortPos.exitMarket()
                print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))+' minus:'+str(round((self.__shortSMA[-1] - self.__longSMA[-1]),3))+' rsi:'+str(round(self.__rsi[-1],3))
                print >> self.logfile,'做空平仓'
        else:
            if self.enterLongSignal(bar):
#                 print 'stragety'+str(bars[self.__instrument].getPrice())
                shares = 1
                print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))
                print >> self.logfile,'做多之前我的钱:'+str(self.getBroker().getCash())
                self.__longPos = self.enterLong(self.__instrument, shares, True)
                    
            elif self.enterShortSignal(bar):
                shares = 1
                print >> self.logfile,' shortSMA:'+str(round(self.__shortSMA[-1],3))+' longSMA:'+str(round(self.__longSMA[-1],3))
                print >> self.logfile,'做空之前我的钱'+str(self.getBroker().getCash())
                self.__shortPos = self.enterShort(self.__instrument, shares, True)
 
    def enterLongSignal(self, bar):#当短周期上穿 长周期，就入场做多，seg也要同方向
        return self.__shortSMA[-1] > self.__longSMA[-1] and self.__shortSMA[-1] - self.__longSMA[-1] < 15 and self.__rsi[-1] <= self.__overSoldThreshold and self.allSegPankous[-1].dir == 1 and bar.getAsk1() != 0
 
    def exitLongSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 1 and bar.getBid1() != 0
 
    def enterShortSignal(self, bar):#当短周期下穿 长周期，就入场做空，seg也要同方向
        return self.__shortSMA[-1] < self.__longSMA[-1] and self.__longSMA[-1] - self.__shortSMA[-1] < 15 and self.__rsi[-1] >= self.__overBoughtThreshold and self.allSegPankous[-1].dir == 2 and bar.getBid1() != 0
 
    def exitShortSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 2 and bar.getAsk1() != 0

    


def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    instrumentID = appconsant.instrumentID
    
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrumentID, "20150717"+instrumentID+".csv")
    
#     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
     
    logfile = appconsant.logfile
    # Evaluate the strategy with the feed's bars.
    #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    myStrategy = MyStrategyRSI(feed,instrumentID, 660,200,100,57,45)
     
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=False)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
    # plt.getInstrumentSubplot("orcl").addDataSeries("price", myStrategy.getPrice())
    # plt.getInstrumentSubplot("orcl").addDataSeries("longSMA", myStrategy.getlongSMA())
    # plt.getInstrumentSubplot("orcl").addDataSeries("shortSMA", myStrategy.getshortSMA())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("segmentDS", myStrategy.getsegment())
    # plt.getInstrumentSubplot("orcl").addDataSeries("RSI", myStrategy.getRSI())
     
    # Plot the simple returns on each bar.
    # plt.getInstrumentSubplot("returns").addDataSeries("rsi", myStrategy.getRSI())
    # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
     
    # Run the strategy. 
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
     
    # for x in myStrategy.getsegment():
    #     print x
    # myStrategy.getsegment().pprint()
    
    allseglen = 0.0
    seg_diffs = []
    u = 0
    x = 0
    for seg in myStrategy.getAllSeg():
        allseglen += seg.diffpri
        u += 1
        if seg.tongji == 1:
            x+=1
            seg_diffs.append(round(seg.diffpri))
    print >>logfile,'allseglen1:'+str(allseglen)+'alldiffprinum:'+str(u) + 'needcountdiffcount:'+str(x)
    
    allseglen1 = 0.0
    seg_diffs1 = []
    u1 = 0
    x1 = 0
    for seg in myStrategy.getAllSeg1():
        allseglen1 += seg.diffpri
        u1 += 1
        if seg.tongji == 1:
            x1+=1
            seg_diffs1.append(round(seg.diffpri))
    print >>logfile,'allseglen2:'+str(allseglen1)+'alldiffprinum:'+str(u1) + 'needcountdiffcount:'+str(x1)
    
    
    
    diffseries = dataseries.SequenceDataSeries(10000)
    
    diffseries1 = dataseries.SequenceDataSeries(10000)
    
    # seg_diffs.sort()
    # for diff in seg_diffs:
    #      diffseries.appendWithDateTime(diff,1)
    
    seg_diffs.sort()
    diffpri = seg_diffs[0]
    frequency = 0
    for diff in seg_diffs:
        if diff != diffpri:
            diffseries.appendWithDateTime(diffpri,frequency)
            frequency = 0
        frequency += 1
        diffpri = diff
        
        
    seg_diffs1.sort()
    diffpri = seg_diffs1[0]
    frequency = 0
    for diff in seg_diffs1:
        if diff != diffpri:
            diffseries1.appendWithDateTime(diffpri,frequency)
            frequency = 0
        frequency += 1
        diffpri = diff
    
    
#     diffseries.pprint()
    
    big0 = 0
    small0 = 0
    for diff in seg_diffs:
        if diff>0:
            big0 += 1
        else:
            small0 += 1
            
    print str(big0)+'  '+str(small0)
         
    
    plt.plotdiff(diffseries)
    
    plt.plotdiff(diffseries1)
    
    logfile.close()
    #     print x
    # Plot the strategy.
#     plt.plot()





# g = 
# print 

if __name__=="__main__": main()
