#!/usr/bin/python
#-*- coding=utf-8 -*-
import os
import conf,data
import logging
# import StoreCsv
# import itertools
# from pyalgotrade.optimizer import local
from tradeanalyze import appconsant, StoreCsv4Nticket

from pyalgotrade import plotter, dataseries
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import strategy
from pyalgotrade.technical import ma
# from pyalgotrade.technical import rsi
# from pyalgotrade.technical import cross
# from pyalgotrade.dataseries import DataSeries
# import tradeanalyze.data_struct
from tradeanalyze.data_struct import *
import time
from pyalgotrade.technical import cross

logfile = ''

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, firstSMA, secondSMA, thirdSMA):
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
        
        self.__firstSMA = ma.SMA(self.__priceDS, firstSMA)
        self.__secondSMA = ma.SMA(self.__priceDS, secondSMA)
        self.__thirdSMA = ma.SMA(self.__priceDS, thirdSMA)
        
        
        
        
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
        
        self.rangeintime = 0
        self.pricejumpoutrange = 0
        
#        

        
#         self.__longewMA = ma.WMA(self.__priceDS, longSMA)
#         self.__shortWMA = ma.WMA(self.__priceDS, shortSMA)

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
    
    def getshortSMA(self):
        return self.__shortSMA
    
    def getlongEMA(self):
        return self.__longEMA
    
    def getfirstSMA(self):
        return self.__firstSMA
    def getsecondSMA(self):
        return self.__secondSMA
    def getthirdSMA(self):
        return self.__thirdSMA
    
    def getshortEMA(self):
        return self.__shortEMA
    
    def getlongWMA(self):
        return self.__longWMA
    
    def getshortWMA(self):
        return self.__shortWMA
    
    def getrangeupper(self):
        return self.rangeUpperDS
    
    def getrangelower(self):
        return self.rangeLowerDS

    def getxrangeupper(self):
        return self.xrangeUpperDS
    
    def getxrangelower(self):
        return self.xrangeLowerDS

    

    def getRSI(self):
        return self.__rsi
    
    def getmoneyearn(self):
        return self.moneyearn
    def getmoneyearntimes(self):
        return self.moneyearntimes
    def getmoneyloss(self):
        return self.moneyloss
    
    

    def onBars(self, bars):
        
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
        barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
#         printLog(barLog)
        
         
         
         
         
        #交易相关
        if self.lastmymoney == 0:
            self.lastmymoney = 1000000
         
         
        if self.__longPos is not None or self.__shortPos is not None:#已入场
             
            if self.__longPos is not None:#已做多
                  
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                 
                 
                if self.topprice == 0:
                    self.topprice = self.__priceDS[-1]
                if self.topprice > self.__priceDS[-1]:#没有创新高
                    self.nonewtop += 1
                else:
                    self.topprice = self.__priceDS[-1]#创新高
                    self.nonewtop =  0
                
                
                if self.__priceDS[-1] - self.buyprice > 50:
                    printLog('大于50，平仓')
                    self.__longPos.exitMarket()
                elif self.buyprice - self.__priceDS[-1] > 15:
                    printLog('亏损，则平仓')
                    self.__longPos.exitMarket()
#                 
            if self.__shortPos is not None:#已做空
                  
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                    
                #没有创新高
                if self.topprice == 0:
                    self.topprice = self.__priceDS[-1]
                if self.topprice < self.__priceDS[-1]:#没有创新低
                    self.nonewtop += 1
                else:
                    self.topprice = self.__priceDS[-1]#没有创新低
                    self.nonewtop =  0
                    
                if self.buyprice - self.__priceDS[-1] > 50:
                    printLog('大于50，平仓')
                    self.__shortPos.exitMarket()
                elif self.buyprice - self.__priceDS[-1] > 15:
                    printLog('亏损，则平仓')
                    self.__shortPos.exitMarket()
#                 
        else:
            if self.lastmymoney != self.getBroker().getCash():
                if self.lastmymoney - self.getBroker().getCash() > 0:
                    printLog('上一次交易亏损'+str(self.lastmymoney - self.getBroker().getCash()))
                    self.losstime += 1
                    self.moneyearn.append(-(self.lastmymoney - self.getBroker().getCash()))
                    self.moneyearntimes.append(bar.getDateTime())
                    self.lossmoney += self.lastmymoney - self.getBroker().getCash()
                else:
                    self.wintime += 1
                    self.winmoney += self.getBroker().getCash() - self.lastmymoney 
                    self.moneyearn.append(-(self.lastmymoney - self.getBroker().getCash()))
                    self.moneyearntimes.append(bar.getDateTime())
                    printLog('上一次交易盈利'+str(self.getBroker().getCash()-self.lastmymoney))
                self.lastmymoney = self.getBroker().getCash()
             
             
        #入场条件 
        if self.__longPos is  None and self.__shortPos is  None:#已入场
            if cross.cross_above(self.__secondSMA,self.__firstSMA) and self.__thirdSMA[-2] > self.__thirdSMA[-1]:
    #                 printLog('当前为趋势，但价格大于最后一个盘整的范围价格加y'+str(self.rangespan_y)+'，准备做多')
                shares = 1
                 
                printLog('做多之前我的钱'+str(self.getBroker().getCash()))
                self.__longPos = self.enterLong(self.__instrument, shares, True)
                self.buyprice = 0
            elif cross.cross_below(self.__secondSMA,self.__firstSMA) and self.__thirdSMA[-2] < self.__thirdSMA[-1]:
                shares = 1
                     
                printLog('做空之前我的钱'+str(self.getBroker().getCash()))
                self.__shortPos = self.enterShort(self.__instrument, shares, True)
                self.buyprice = 0
            


        
        
        
                      
        
        
        
        
        # Wait for enough bars to be available to calculate SMA and RSI.
        
 
    

def printLog(log):
#     print log
    logging.getLogger('trade').info(log)


    


def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    print os.path.sep
    rootdir = appconsant.rootdir
    instrumentID = "IF1509"
    date = "20150730"
#     ISOTIMEFORMAT='%Y-%m-%d%H%M%S'
# #     appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+ time.strftime( ISOTIMEFORMAT, time.localtime() )+'log.txt', loglevel=1, logger="log").getlog()
# #     appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+'log.txt', loglevel=1, logger="log").getlog()
#     mylogger.changeLoggerFile(instrumentID+date+ time.strftime( ISOTIMEFORMAT, time.localtime() )+'log.txt')
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',                                  
        filename="main.log",
        filemode='a+')
 
    _logger = logging.getLogger('trade')
    fh = logging.FileHandler(date + instrumentID +'log.log')
    fh.setLevel(logging.DEBUG)
    formatter1 = logging.Formatter('%(message)s')
    fh.setFormatter(formatter1)
    _logger.addHandler(fh)
    
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
    myStrategy = MyStrategyRSI(feed,instrumentID, 50,20,5)
     
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangeupper", myStrategy.getxrangeupper())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangelower", myStrategy.getxrangelower())
# #     plt.getOrCreateSubplot("wave").addDataSeries("waveds", myStrategy.getWave())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("firstSMA", myStrategy.getfirstSMA())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("secondSMA", myStrategy.getsecondSMA())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("thirdSMA", myStrategy.getthirdSMA())
#     plt.getOrCreateSubplot("WMA").addDataSeries("SWMA", myStrategy.getshortWMA())
#     plt.getInstrumentSubplot("test").addDataSeries("rangeupper", myStrategy.getrangeupper())
#     plt.getInstrumentSubplot("test").addDataSeries("rangelower", myStrategy.getrangelower())
    
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("segmentDS", myStrategy.getsegment())
    # plt.getInstrumentSubplot("orcl").addDataSeries("RSI", myStrategy.getRSI())
     
    # Plot the simple returns on each bar.
    # plt.getInstrumentSubplot("returns").addDataSeries("rsi", myStrategy.getRSI())
    # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
     
    # Run the strategy. 
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
     
    
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
    
    
    printLog(myStrategy.getmarketinfo())
    
    printLog(myStrategy.getmoneyearn())
    printLog(myStrategy.getmoneyloss())
    
    
#     plt.plotdiffbarbytwo(myStrategy.getmoneyearntimes(), myStrategy.moneyearn)
#     plt.plotdiff(waveseries)
    plt.plot()




# g = 
# print 

if __name__=="__main__": main()
