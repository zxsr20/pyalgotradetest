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
from pyalgotrade.technical.atr import ATR


#首先，在 speed_spread 周期内，上涨或下跌占到所有tick长度的 x%(90%)也就是 这个时间段内 90%的长度都创新高就开始记录，往前回溯整个长段。回溯的方法是 ，n个周期内的最低点

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
        self.rangespan_stoploss = 40 * data_config.PriceTick
        self.rangespan_n = 200
        self.tongji = 0
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
        
        self.priceUpDown = []
        self.priceUpDownPercent = []
        self.UpDown_n = 80#n个ticket
        self.UpDown_x = 0.75#中有0.9都是上涨或是下跌的
        self.onepercent = 1/(float)(self.UpDown_n)
        
        #seg
        self.rongren = 20 #can skip num
        self.bNewSeg = False;
        self.nDir = 0;
        self.__segmentDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.allSegPankous = []#store the pankou data
        
        self.__longSMA = ma.SMA(self.__priceDS, longSMA)
        self.__shortSMA = ma.SMA(self.__priceDS, shortSMA)
#         self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
#         self.__overBoughtThreshold = overBoughtThreshold
#         self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None
        
#         self.atrDs = ATR(feed[instrument],14) 
#         self.__longEMA = ma.SMA(self.__priceDS, 300)
#         self.__shortEMA = ma.SMA(self.__priceDS, 50)
# #         self.macdDs = macd.MACD(self.__priceDS,5,13,6)
#         self.macdDs = macd.MACD(self.__priceDS,50,300,150)
#         self.hisDs = self.macdDs.getHistogram()
    def getPrice(self):
        return self.__priceDS
    def getATR(self):
        return self.atrDs
    def getmarketinfo(self): 
        return '交易次数:'+str(self.wintime+self.losstime)+'盈利次数:'+str(self.wintime)+'亏损次数:'+str(self.losstime)+'盈利额:'+str(self.winmoney)+'亏损额:'+str(self.lossmoney)
    def getmoneyearn(self):
        return self.moneyearn
    def getmoneyloss(self):
        return self.moneyloss
    def getmacdDs(self):
        return self.macdDs
    def gethisDs(self):
        return self.hisDs
    def getwavetickets(self):
        return self.wavetickets
    
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
#         tp = CTicketWave()
#         tp.idx = len(self.wavetickets)+1
#         tick_idx_start = len(self.__priceDS) - self.nwaveticket
#         if tick_idx_start < 0:
#             tick_idx_start = 0
#         tp.tick_idx_start = tick_idx_start
#         tp.tick_idx_end = len(self.__priceDS)-1
#         tp.price_start = self.__priceDS[tick_idx_start]
#         tp.price_end = self.__priceDS[-1]
#         priceds = self.__priceDS[tick_idx_start:len(self.__priceDS)]
#         tp.upper = max(priceds)
#         tp.lower = min(priceds)
#         tp.price_wave = tp.upper - tp.lower
#         self.waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
# #         appconsant.logLogger.info('wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave))
#         
# #         appconsant.logLogger.info(self.ticketidx)
#         self.wavetickets.append(tp)
        
        if len(self.__priceDS) == 1:
            return
        if self.__priceDS[-1] > self.__priceDS[-2]:
            self.priceUpDown.append(1)
            if len(self.priceUpDown) >= self.UpDown_n:#如果大于n开始计算percent
                if len(self.priceUpDownPercent) > 0:#如果不是是第一个，可以在前面的基础上免去计算
                    if self.priceUpDown[-self.UpDown_n] == 1:
                        self.priceUpDownPercent.append(self.priceUpDownPercent[-1])
                    else:
                        self.priceUpDownPercent.append(self.priceUpDownPercent[-1]+self.onepercent)
                else:
                    z = 0
                    for i in range(self.UpDown_n):
                        if self.priceUpDown[-(i+1)] == 1:
                            z+=1
                    self.priceUpDownPercent.append(z/(float)(self.UpDown_n))
                            
        else:
            self.priceUpDown.append(2)
            if len(self.priceUpDown) >= self.UpDown_n:#如果大于n开始计算percent
                if len(self.priceUpDownPercent) > 0:#如果不是是第一个，可以在前面的基础上免去计算
                    if self.priceUpDown[-self.UpDown_n] == 2:
                        self.priceUpDownPercent.append(self.priceUpDownPercent[-1])
                    else:
                        self.priceUpDownPercent.append(self.priceUpDownPercent[-1]-self.onepercent)
                else:
                    z = 0
                    for i in range(self.UpDown_n):
                        if self.priceUpDown[-(i+1)] == 1:
                            z+=1
                    self.priceUpDownPercent.append(z/(float)(self.UpDown_n))
        
        
        
        if self.__longPos is not None or self.__shortPos is not None:#已入场
            
            if self.__longPos is not None:#已做多
                 
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                
                if self.topprice == 0:
                    self.topprice = self.__priceDS[-1]
                if self.topprice >= self.__priceDS[-1]:#没有创新高
                    self.nonewtop += 1
                else:
                    self.topprice = self.__priceDS[-1]#创新高
                    self.nonewtop =  0
                    
                if self.nonewtop > self.rangespan_n:#n个点没有创新高，离场
                    printLog('当前已经有'+str(self.rangespan_n)+'个ticket没有创新高，准备平仓')
                    self.__longPos.exitMarket()
                    
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做多平仓')
                
                elif self.buyprice - self.__priceDS[-1] >= self.rangespan_stoploss:#已亏损
                    printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
                    self.__longPos.exitMarket()
                    
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做多平仓')
                elif self.topprice - self.__priceDS[-1] > 30:
                    printLog('从最高点回撤')
                    self.__longPos.exitMarket()
                    
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做多平仓')
                    
            if self.__shortPos is not None:#已做空
                 
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                   
                #没有创新高
                if self.topprice == 0:
                    self.topprice = self.__priceDS[-1]
                if self.topprice <= self.__priceDS[-1]:#没有创新低
                    self.nonewtop += 1
                else:
                    self.topprice = self.__priceDS[-1]#没有创新低
                    self.nonewtop =  0
                if self.nonewtop > self.rangespan_n:#n个点没有创新低，离场
                    printLog('当前已经有'+str(self.rangespan_n)+'个tocket没有创新低，准备平仓')
                    self.__shortPos.exitMarket()
                    
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做空平仓') 
                    
                elif self.__priceDS[-1] - self.buyprice >= self.rangespan_stoploss:#已亏损
                    printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
                    self.__shortPos.exitMarket()
                    
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做空平仓')
                elif self.__priceDS[-1] - self.topprice > 30:
                    printLog('从最低点回测')
                    self.__shortPos.exitMarket()
                    
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做空平仓')
                    
        else:
            if self.lastmymoney != self.getBroker().getCash():
                
                if self.lastmymoney - self.getBroker().getCash() > 0:
                    printLog('上一次交易亏损'+str(self.lastmymoney - self.getBroker().getCash()))
                    self.losstime += 1
                    self.moneyearn.append(self.lastmymoney - self.getBroker().getCash())
                    self.lossmoney += self.lastmymoney - self.getBroker().getCash()
                else:
                    self.wintime += 1
                    self.winmoney += self.getBroker().getCash() - self.lastmymoney 
                    self.moneyearn.append(self.lastmymoney - self.getBroker().getCash())
                    printLog('上一次交易盈利'+str(self.getBroker().getCash()-self.lastmymoney))
                self.lastmymoney = self.getBroker().getCash()
            
        if self.__longPos is None and self.__shortPos is  None:#已入场   
            if len(self.priceUpDownPercent) > 0:
                if self.priceUpDownPercent[-1] > self.UpDown_x:
                    self.tongji = 1
                    self.topprice = 0
                elif self.priceUpDownPercent[-1] < 1-self.UpDown_x:
                    self.tongji = 2
                    self.topprice = 0
                if self.tongji == 1:
                    
                    if self.topprice == 0:
                        self.topprice = self.__priceDS[-1]
                    if self.topprice < self.__priceDS[-1]:#没有创新高
                        self.topprice = self.__priceDS[-1]#创新高
                        
                    if  self.topprice - self.__priceDS[-1] > 30:
                        shares = 1
                        printLog('做空之前我的钱'+str(self.getBroker().getCash()))
                        self.__shortPos = self.enterShort(self.__instrument, shares, True)
                        self.topprice = 0
                        self.tongji = 0
                elif self.tongji == 2:
                    if self.topprice == 0:
                        self.topprice = self.__priceDS[-1]
                    if self.topprice > self.__priceDS[-1]:#没有创新高
                        self.topprice = self.__priceDS[-1]#创新高
                        
                    if  self.__priceDS[-1] - self.topprice > 30:
                        shares = 1
                        printLog('做多之前我的钱'+str(self.getBroker().getCash()))
                        self.__longPos = self.enterLong(self.__instrument, shares, True)
                        self.topprice = 0
                        self.tongji = 0
            
                   
        
        
                        
#         printLog(self.priceUpDown)
#         printLog(self.priceUpDownPercent) 

def printLog(log):
    pass

def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    
    rootdir = appconsant.rootdir
    
    instrumentID = appconsant.instrumentID
    date = appconsant.date
    
    ISOTIMEFORMAT='%Y-%m-%d%H%M%S'
     
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
    myStrategy1 = MyStrategyRSI1(feed,instrumentID, 660,200,100,57,45,appconsant.waveseg_nwaveticket,appconsant.waveseg_y,appconsant.waveseg_x,appconsant.waveseg_rongren)
    
    returnsAnalyzer = returns.Returns()
    myStrategy1.attachAnalyzer(returnsAnalyzer)
    plt = plotter.StrategyPlotter(myStrategy1,plotOrder=True)
    
    plt.getInstrumentSubplot(instrumentID).addDataSeries("longma", myStrategy1.getlongSMA())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("smallEma", myStrategy1.getshortSMA())
#     plt.getOrCreateSubplot("atr").addDataSeries("atr", myStrategy1.getATR())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("big", myStrategy1.getbigprice())
#     plt.getOrCreateSubplot("macd").addDataSeries("sign", myStrategy1.getmacdDs())
# #     plt.getOrCreateSubplot("his").addDataSeries("his", myStrategy1.gethisDs())
# #     plt.getOrCreateSubplot("seg").addDataSeries("his", myStrategy1.getseg())
#     plt.getOrCreateSubplot("rsi").addDataSeries("rsi", myStrategy1.getRSI())
#     
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("longEma", myStrategy1.getlongEMA())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("smallEma", myStrategy1.getshortEMA())
    
    myStrategy1.run()
    myStrategy1.info("Final portfolio value: $%.2f" % myStrategy1.getResult())
    
    printLog(myStrategy1.getmarketinfo())
     
    printLog(myStrategy1.getmoneyearn())
    printLog(myStrategy1.getmoneyloss())
    plt.plot()
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
