#!/usr/bin/python
#-*- coding=utf-8 -*-
import sys,os
import conf,data,process
import time
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
import math
#判断当前tick均价和移动平均价之间的距离
#当距离大于一定参数，并且，移动平均线已经不是最高价，就入场

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
        self.wavetickets = []
        self.high = 0.0
        self.lower = 0.0
        
        data_config = conf.getInstrumentInfo(instrument) 
        
        self.rangespan_nwaveticket = 200
        self.rangespan_ma = rangespan_ma
        self.rangespan_range = rangespan_range
        self.rangespan_span = rangespan_span
        self.rangespan_stoploss = rangespan_stoploss * data_config.PriceTick
        self.rangespan_y = rangespan_y
        self.rangespan_n = 50
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
#         self.bigUpDownDS =  dataseries.SequenceDataSeries(100000)#use to draw map
#         
#         self.rangeUpperDS =  dataseries.SequenceDataSeries(100000)#use to draw map
#         self.rangeLowerDS =  dataseries.SequenceDataSeries(100000)#use to draw map
#         
#         self.lastrangeupper = 0.0
#         self.lastrangelower = 0.0
#         
#         self.xrangeUpperDS =  dataseries.SequenceDataSeries(100000)#use to draw map
#         self.xrangeLowerDS =  dataseries.SequenceDataSeries(100000)#use to draw map

        self.smapricediffDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        self.moneyearn = []
        self.moneyloss = []
        
        self.buyprice = 0.0
        self.nonewtop = 0
        self.topprice = 0.0
        
        self.topsma = 0.0
        self.nonewsmatop = 0
        #用于交易结果统计
        self.lastmymoney = 1000000
        self.losstime = 0
        self.wintime = 0
        self.winmoney = 0.0
        self.lossmoney = 0.0
        
        self.rangeintime = 0
        
        self.qushi_buy = 0
        self.panzheng_buy = 0
        
        self.panzheng_huiguitime = 0
        self.panzheng_huiguitime2 = 0
        self.qushi_huiguitime = 0
        self.qushi_huiguitime2 = 0
        self.qitatime = 0
        self.huigui_idx = 0
        
        
        self.jilu = 0
        
        
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
        
        self.__longSMA = ma.SMA(self.__priceDS, self.rangespan_ma)
        self.__shortSMA = ma.SMA(self.__priceDS, shortSMA)
        self.__rsi = rsi.RSI(self.__priceDS, rsiPeriod)
        self.__overBoughtThreshold = overBoughtThreshold
        self.__overSoldThreshold = overSoldThreshold
        self.__longPos = None
        self.__shortPos = None

    def gethuiguiinfo(self):
        return ('在盘整中超过y做空或做多，最后平仓的时候处于盘整中，之前做多现在平仓价格低于盘整上线平仓和之前做空现在平仓价格高于盘整下线平仓的次数是:'+str(self.panzheng_huiguitime)+
                '在盘整中超过y做空或做多，最后平仓的时候不处于盘整中，之前做多现在平仓价格低于最后的盘整上线平仓和之前做空现在平仓价格高于最后的盘整下线平仓的次数是'+str(self.panzheng_huiguitime2)+
                '不在盘整中，超过最后一次盘整y做空或做多，最后平仓的时候处于盘整中，之前做多现在平仓价格低于盘整上线平仓和之前做空现在平仓价格高于盘整下线平仓的次数是'+str(self.qushi_huiguitime)+
                '不在盘整中，超过最后一次盘整y做空或做多，最后平仓的时候也不在处于盘整中，之前做多现在平仓价格低于最后盘整上线平仓和之前做空现在平仓价格高于最后盘整下线平仓的次数是'+str(self.qushi_huiguitime2)+' '+str(self.qitatime))
    
    def getPrice(self):
        return self.__priceDS
    
    def getmarketinfo(self):
        return '交易次数:'+str(self.wintime+self.losstime)+'盈利次数:'+str(self.wintime)+'亏损次数:'+str(self.losstime)+'盈利额:'+str(self.winmoney)+'亏损额:'+str(self.lossmoney)
    def getsmapricediffDS(self):
        return self.smapricediffDS
    
    def getwavetickets(self):
        return self.wavetickets
    
    def getBigUpDown(self):
        return self.bigUpDownDS
    
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
        
        tp = CTicketWave()
        tp.idx = len(self.wavetickets)+1
        tick_idx_start = len(self.__priceDS) - self.rangespan_nwaveticket
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
        printLog('wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave))
        
        if self.__longSMA[-1] is None:
            return
        
        self.smapricediffDS.appendWithDateTime(bar.getDateTime(),abs(self.__longSMA[-1] - self.__priceDS[-1]))
        
        printLog('self.__longSMA[-1]'+str(self.__longSMA[-1])+'self.__priceDS[-1]'+str(self.__priceDS[-1]))
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
                     
                if self.nonewtop > self.rangespan_n:#n个点没有创新高，离场
                    printLog('当前已经有'+str(self.rangespan_n)+'个ticket没有创新高，准备平仓')
                    self.__longPos.exitMarket()
                elif self.buyprice - self.__priceDS[-1] >= self.rangespan_stoploss:#已亏损
                    printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
                    self.__longPos.exitMarket()
                    
            if self.__shortPos is not None:#已做空
                  
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                
                if self.topprice == 0:
                    self.topprice = self.__priceDS[-1]
                if self.topprice < self.__priceDS[-1]:#没有创新低
                    self.nonewtop += 1
                else:
                    self.topprice = self.__priceDS[-1]#没有创新低
                    self.nonewtop =  0
                if self.nonewtop > self.rangespan_n:#n个点没有创新低，离场
                    printLog('当前已经有'+str(self.rangespan_n)+'个tocket没有创新低，准备平仓')
                    self.__shortPos.exitMarket()
                elif self.__priceDS[-1] - self.buyprice >= self.rangespan_stoploss:#已亏损
                    printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
                    self.__shortPos.exitMarket()
                
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
            
            
            if abs(self.__longSMA[-1] - self.__priceDS[-1]) > 70:
                printLog('abs (self.__longSMA[-1] - self.__priceDS[-1]) > 70'+str(self.__longSMA[-1] - self.__priceDS[-1]))        
                if self.__longSMA[-1] > self.__priceDS[-1]:#如果sma大于价格，就是下跌中
                    self.jilu = 2
                else:#如果sma大于价格，就是上涨中
                    self.jilu = 1
            if self.jilu == 1:
                if self.topsma == 0:
                    self.topsma = self.__longSMA[-1]
                    printLog('self.topsma = self.__longSMA[-1]'+str(self.topsma))
                if self.topsma > self.__longSMA[-1]:#没有创新高
                    self.nonewsmatop += 1
                    printLog('self.topsma > self.__longSMA[-1]'+str(self.topsma)+'self.__longSMA[-1]'+str(self.__longSMA[-1]))
                else:
                    self.topsma = self.__longSMA[-1]#创新高
                    self.nonewsmatop =  0
                    printLog('self.topsma <= self.__longSMA[-1]'+str(self.topsma)+'self.__longSMA[-1]'+str(self.__longSMA[-1]))
            if self.jilu == 2:
                if self.topsma == 0:
                    self.topsma = self.__longSMA[-1]
                if self.topsma < self.__longSMA[-1]:#没有创新高
                    self.nonewsmatop += 1
                else:
                    self.topsma = self.__longSMA[-1]#创新高
                    self.nonewsmatop =  0
            printLog('self.jilu'+str(self.jilu)+'self.nonewsmatop'+str(self.nonewsmatop))  
            if self.nonewsmatop > 3 and tp.price_wave >150:
                if self.jilu == 2:
                    shares = 1
                    printLog('做多之前我的钱'+str(self.getBroker().getCash()))
                    self.__longPos = self.enterLong(self.__instrument, shares, True)
                    self.buyprice = 0
                    self.jilu = 0
                    self.nonewsmatop = 0
                    self.topsma = 0.0
                    self.topprice = 0.0
                    self.nonewtop = 0
                else:
                    shares = 1
                    printLog('做空之前我的钱'+str(self.getBroker().getCash()))
                    self.__shortPos = self.enterShort(self.__instrument, shares, True)
                    self.buyprice = 0
                    self.jilu = 0
                    self.nonewsmatop = 0
                    self.topsma = 0.0
                    self.topprice = 0.0
                    self.nonewtop = 0
        
             
#         if tp.price_wave > 50:
#             self.bigUpDownDS.appendWithDateTime(bar.getDateTime(),self.__priceDS[-1])
#         else:
#             self.bigUpDownDS.appendWithDateTime(bar.getDateTime(),None)
#         
#         self.wavetickets.append(tp)
#         
#         
#         if len(self.__priceDS) < self.rangespan_ma:
#             return
#         
#         
#         priceds = []
#         for i in range(self.rangespan_ma):
#             priceds.append(round(self.__priceDS[-(i+1)],0))
#         dic = {}
#         for item in priceds:
#             dic[item] = dic.get(item, 0) + 1
#         dic = sorted(dic.items())
#         numds = []
#         pds = []
#         for item in dic:
#             numds.append(item[1]) 
#             pds.append(item[0]) 
# #         print(dic)
# #         print numds
# #         print 'oldpricerange:'+str(pds[0])+' '+str(pds[len(pds)-1])
#         
#         
#         ids = mymost_close_array(numds,len(numds),self.rangespan_range)
# #         print str(ids)
# #         print str(pds)
#         rangeLower = pds[ids[0]] 
#         rangeUpper = pds[ids[1]]
# 
#         self.rangeLowerDS.appendWithDateTime(bar.getDateTime(),rangeLower)
#         self.rangeUpperDS.appendWithDateTime(bar.getDateTime(),rangeUpper)
#         
#         if rangeUpper - rangeLower <= self.rangespan_span:
#             self.rangeintime += 1
#             self.xrangeLowerDS.appendWithDateTime(bar.getDateTime(),rangeLower)
#             self.xrangeUpperDS.appendWithDateTime(bar.getDateTime(),rangeUpper)
# #             if self.rangeintime > 10:
#             self.lastrangeupper = rangeUpper
#             self.lastrangelower = rangeLower
#         else:
#             self.rangeintime = 0
#             self.xrangeLowerDS.appendWithDateTime(bar.getDateTime(),None)
#             self.xrangeUpperDS.appendWithDateTime(bar.getDateTime(),None)
# 
#         
#         #交易相关
#         if self.lastmymoney == 0:
#             self.lastmymoney = 1000000
#         
#         if rangeUpper - rangeLower > self.rangespan_span:#趋势
#             printLog('当前为趋势，价格范围为'+str(rangeLower)+'到 '+str(rangeUpper))
#         else:
#             printLog('当前为盘整，价格范围为'+str(rangeLower)+'到 '+str(rangeUpper))
#         
#         
#         
#         #再加个反向操作
#         if self.__longPos is not None or self.__shortPos is not None:#已入场
#             
#             if self.__longPos is not None:#已做多
#                  
#                 if self.buyprice == 0:#获得购买价格
#                     self.buyprice = self.__priceDS[-1]
#                 
#                 if self.topprice == 0:
#                     self.topprice = self.__priceDS[-1]
#                 if self.topprice >= self.__priceDS[-1]:#没有创新高
#                     self.nonewtop += 1
#                 else:
#                     self.topprice = self.__priceDS[-1]#创新高
#                     self.nonewtop =  0
#                     
#                     
#                 
#                     
#                 
#                 if self.nonewtop > self.rangespan_n:#n个点没有创新高，离场
#                     printLog('当前已经有'+str(self.rangespan_n)+'个ticket没有创新高，准备平仓')
#                     self.__longPos.exitMarket()
#                     
# #                     if  self.__priceDS[-1] < rangeUpper and rangeUpper - rangeLower < self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime += 1
# #                         printLog('self.panzheng_huiguitime += 1')
# #                     elif self.__priceDS[-1] < self.lastrangeupper and rangeUpper - rangeLower > self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime2 += 1
# #                         printLog('self.panzheng_huiguitime2 += 1')
# #                     elif self.__priceDS[-1] < rangeUpper and rangeUpper - rangeLower < self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime += 1
# #                         printLog('self.qushi_huiguitime += 1')
# #                     elif self.__priceDS[-1] < self.lastrangeupper and rangeUpper - rangeLower > self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime2 += 1
# #                         printLog('self.qushi_huiguitime2 += 1')
# #                     else:
# #                         self.qitatime += 1
# #                         printLog('self.qitatime += 1'+str(self.__priceDS[-1]))
# #                     self.qushi_buy = 0
# #                     self.panzheng_buy = 0
#                     
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做多平仓')
#                 
# #                 elif self.nonewtop > self.rangespan_n/4 and self.buyprice - self.__priceDS[-1] > 0:
# #                     printLog('二分之一的n没有突破，反而价亏了')
# #                     self.__longPos.exitMarket()
# #                     self.buyprice = 0
# #                     self.nonewtop =  0
# #                     self.topprice = 0.0
# #                     printLog('做多平仓')
# #                 elif rangeUpper - rangeLower < self.rangespan_span:
# #                     if self.__priceDS[-1] < rangeUpper:
# #                         printLog('做多，但是价格重新进入范围内，则平仓')
# #                         self.__longPos.exitMarket()
# #                         self.buyprice = 0
# #                         self.nonewtop =  0
# #                         self.topprice = 0.0
# #                         printLog('做多平仓')
#                 elif self.buyprice - self.__priceDS[-1] >= self.rangespan_stoploss:#已亏损
#                     printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
#                     self.__longPos.exitMarket()
#                     
# #                     if  self.__priceDS[-1] < rangeUpper and rangeUpper - rangeLower < self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime += 1
# #                         printLog('self.panzheng_huiguitime += 1')
# #                     elif self.__priceDS[-1] < self.lastrangeupper and rangeUpper - rangeLower > self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime2 += 1
# #                         printLog('self.panzheng_huiguitime2 += 1')
# #                     elif self.__priceDS[-1] < rangeUpper and rangeUpper - rangeLower < self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime += 1
# #                         printLog('self.qushi_huiguitime += 1')
# #                     elif self.__priceDS[-1] < self.lastrangeupper and rangeUpper - rangeLower > self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime2 += 1
# #                         printLog('self.qushi_huiguitime2 += 1')
# #                     else:
# #                         self.qitatime += 1
# #                         printLog('self.qitatime += 1'+str(self.__priceDS[-1]))
# #                     self.qushi_buy = 0
# #                     self.panzheng_buy = 0
#                     
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做多平仓')
#                 elif self.__priceDS[-1] < self.lastrangelower:
#                     printLog('当前价格小于最后一次盘整的下线')
#                     self.__longPos.exitMarket()
#                     
# #                     if  self.__priceDS[-1] < rangeUpper and rangeUpper - rangeLower < self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime += 1
# #                         printLog('self.panzheng_huiguitime += 1')
# #                     elif self.__priceDS[-1] < self.lastrangeupper and rangeUpper - rangeLower > self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime2 += 1
# #                         printLog('self.panzheng_huiguitime2 += 1')
# #                     elif self.__priceDS[-1] < rangeUpper and rangeUpper - rangeLower < self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime += 1
# #                         printLog('self.qushi_huiguitime += 1')
# #                     elif self.__priceDS[-1] < self.lastrangeupper and rangeUpper - rangeLower > self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime2 += 1
# #                         printLog('self.qushi_huiguitime2 += 1')
# #                     else:
# #                         self.qitatime += 1
# #                         printLog('self.qitatime += 1'+str(self.__priceDS[-1]))
# #                     self.qushi_buy = 0
# #                     self.panzheng_buy = 0
#                     
#                     
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做多平仓')
#                     
#                     
# #                 if self.buyprice == 0:#如果已经平仓
# #                     if rangeUpper - rangeLower > self.rangespan_span:#如果已经出了盘整
# #                         self.lastrangeupper = 0.0
# #                         self.lastrangelower = 0.0
# #                 elif self.__priceDS[-1] < self.__priceDS[-2] and self.__priceDS[-1] < self.buyprice:
# #                     printLog('价格开始下跌超过买价')
# #                     self.__longPos.exitMarket()
# #                     self.buyprice = 0
# #                     self.nonewtop =  0
# #                     self.topprice = 0.0
# #                     printLog('做多平仓')
#             if self.__shortPos is not None:#已做空
#                  
#                 if self.buyprice == 0:#获得购买价格
#                     self.buyprice = self.__priceDS[-1]
#                    
#                 #没有创新高
#                 if self.topprice == 0:
#                     self.topprice = self.__priceDS[-1]
#                 if self.topprice <= self.__priceDS[-1]:#没有创新低
#                     self.nonewtop += 1
#                 else:
#                     self.topprice = self.__priceDS[-1]#没有创新低
#                     self.nonewtop =  0
#                 if self.nonewtop > self.rangespan_n:#n个点没有创新低，离场
#                     printLog('当前已经有'+str(self.rangespan_n)+'个tocket没有创新低，准备平仓')
#                     self.__shortPos.exitMarket()
#                     
# #                     if  self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime += 1
# #                         printLog('self.panzheng_huiguitime += 1')
# #                     elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime2 += 1
# #                         printLog('self.panzheng_huiguitime2 += 1')
# #                     elif self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime += 1
# #                         printLog('self.qushi_huiguitime += 1')
# #                     elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime2 += 1
# #                         printLog('self.qushi_huiguitime2 += 1')
# #                     else:
# #                         self.qitatime += 1
# #                         printLog('self.qitatime += 1'+str(self.__priceDS[-1]))
# #                     self.qushi_buy = 0
# #                     self.panzheng_buy = 0
#                     
#                     
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做空平仓') 
#                     
# #                 elif self.nonewtop > self.rangespan_n/2 and self.__priceDS[-1] - self.buyprice > 0:
# #                     printLog('二分之一的n没有突破，反而价亏了')
# #                     self.__shortPos.exitMarket()
# #                     self.buyprice = 0
# #                     self.nonewtop =  0
# #                     self.topprice = 0.0
# #                     printLog('做空平仓')
# #                 elif rangeUpper - rangeLower < self.rangespan_span:
# #                     if self.__priceDS[-1] > rangeLower:
# #                         printLog('做空，但是价格重新进入范围内，则平仓')
# #                         self.__shortPos.exitMarket()
# #                         self.buyprice = 0
# #                         self.nonewtop =  0
# #                         self.topprice = 0.0
# #                         printLog('做空平仓')
#                 elif self.__priceDS[-1] - self.buyprice >= self.rangespan_stoploss:#已亏损
#                     printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
#                     self.__shortPos.exitMarket()
#                     
# #                     if  self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime += 1
# #                         printLog('self.panzheng_huiguitime += 1')
# #                     elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime2 += 1
# #                         printLog('self.panzheng_huiguitime2 += 1')
# #                     elif self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime += 1
# #                         printLog('self.qushi_huiguitime += 1')
# #                     elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime2 += 1
# #                         printLog('self.qushi_huiguitime2 += 1')
# #                     else:
# #                         self.qitatime += 1
# #                         printLog('self.qitatime += 1'+str(self.__priceDS[-1]))
# #                     self.qushi_buy = 0
# #                     self.panzheng_buy = 0
#                     
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做空平仓')
#                 elif self.__priceDS[-1] > self.lastrangeupper:
#                     printLog('当前价格小于最后一次盘整的上线')
#                     self.__shortPos.exitMarket()
#                     
# #                     if  self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime += 1
# #                         printLog('self.panzheng_huiguitime += 1')
# #                     elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.panzheng_buy == 1:
# #                         self.panzheng_huiguitime2 += 1
# #                         printLog('self.panzheng_huiguitime2 += 1')
# #                     elif self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime += 1
# #                         printLog('self.qushi_huiguitime += 1')
# #                     elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.qushi_buy == 1:
# #                         self.qushi_huiguitime2 += 1
# #                         printLog('self.qushi_huiguitime2 += 1')
# #                     else:
# #                         self.qitatime += 1
# #                         printLog('self.qitatime += 1'+str(self.__priceDS[-1]))
#                     
#                     
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做空平仓')
#                     
# #                 if self.buyprice == 0:#如果已经平仓
# #                     if rangeUpper - rangeLower > self.rangespan_span:#如果已经出了盘整
# #                         self.lastrangeupper = 0.0
# #                         self.lastrangelower = 0.0
#                     
# #                 elif self.__priceDS[-1] > self.__priceDS[-2] and self.__priceDS[-1] > self.buyprice:
# #                     printLog('价格开始上升超过买价')
# #                     self.__shortPos.exitMarket()
# #                     self.buyprice = 0
# #                     self.nonewtop =  0
# #                     self.topprice = 0.0
# #                     printLog('做空平仓')
#         else:
#             if self.lastmymoney != self.getBroker().getCash():
#                 
# #                 if  self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.panzheng_buy == 1:
# #                     self.panzheng_huiguitime += 1
# #                     printLog('self.panzheng_huiguitime += 1')
# #                 elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.panzheng_buy == 1:
# #                     self.panzheng_huiguitime2 += 1
# #                     printLog('self.panzheng_huiguitime2 += 1')
# #                 elif self.__priceDS[-1] > rangeLower and rangeUpper - rangeLower < self.rangespan_span and self.qushi_buy == 1:
# #                     self.qushi_huiguitime += 1
# #                     printLog('self.qushi_huiguitime += 1')
# #                 elif self.__priceDS[-1] > self.lastrangelower and rangeUpper - rangeLower > self.rangespan_span and self.qushi_buy == 1:
# #                     self.qushi_huiguitime2 += 1
# #                     printLog('self.qushi_huiguitime2 += 1')
# #                 else:
# #                     self.qitatime += 1
# #                     printLog('self.qitatime += 1'+str(self.__priceDS[-1]))
# #                 self.qushi_buy = 0
# #                 self.panzheng_buy = 0
#                 
#                 if self.lastmymoney - self.getBroker().getCash() > 0:
#                     printLog('上一次交易亏损'+str(self.lastmymoney - self.getBroker().getCash()))
#                     self.losstime += 1
#                     self.moneyearn.append(self.lastmymoney - self.getBroker().getCash())
#                     self.lossmoney += self.lastmymoney - self.getBroker().getCash()
#                 else:
#                     self.wintime += 1
#                     self.winmoney += self.getBroker().getCash() - self.lastmymoney 
#                     self.moneyearn.append(self.lastmymoney - self.getBroker().getCash())
#                     printLog('上一次交易盈利'+str(self.getBroker().getCash()-self.lastmymoney))
#                 self.lastmymoney = self.getBroker().getCash()
#             
#             if rangeUpper - rangeLower < self.rangespan_span:#趋势
#                 if self.__priceDS[-1] > rangeUpper+self.rangespan_y:
#                     printLog('当前价格大于范围价格加y'+str(self.rangespan_y)+'，准备做多')
#                     shares = 1
#                     
#                     printLog('做多之前我的钱'+str(self.getBroker().getCash()))
#                     self.__longPos = self.enterLong(self.__instrument, shares, True)
#                     self.panzheng_buy = 1
#                 elif self.__priceDS[-1] < rangeLower - self.rangespan_y:
#                     printLog('当前价格小于于范围价格减y'+str(self.rangespan_y)+'，准备做空')
#                     shares = 1
#                     
#                     printLog('做空之前我的钱'+str(self.getBroker().getCash()))
#                     self.__shortPos = self.enterShort(self.__instrument, shares, True)
#                     self.panzheng_buy = 2
#             elif self.lastrangeupper != 0.0 and self.lastrangelower != 0.0:
#                 if self.__priceDS[-1] > self.lastrangeupper+self.rangespan_y:
#                     printLog('当前为趋势，但价格大于最后一个盘整的范围价格加y'+str(self.rangespan_y)+'，准备做多')
#                     shares = 1
#                     
#                     printLog('做多之前我的钱'+str(self.getBroker().getCash()))
#                     self.__longPos = self.enterLong(self.__instrument, shares, True)
#                     self.lastrangeupper = 0.0
#                     self.lastrangelower = 0.0
#                     self.qushi_buy = 1
#                 elif self.__priceDS[-1] < self.lastrangelower - self.rangespan_y:
#                     printLog('当前为趋势，但价格小于最后一个盘整的范围价格减y'+str(self.rangespan_y)+'，准备做空')
#                     shares = 1
#                     
#                     printLog('做空之前我的钱'+str(self.getBroker().getCash()))
#                     self.__shortPos = self.enterShort(self.__instrument, shares, True)
#                     self.lastrangeupper = 0.0
#                     self.lastrangelower = 0.0
#                     self.qushi_buy = 2


        
        
        
                      
        
        
        
        
        # Wait for enough bars to be available to calculate SMA and RSI.
        
 
    def enterLongSignal(self, bar):#当短周期上穿 长周期，就入场做多，seg也要同方向
        return self.__shortSMA[-1] > self.__longSMA[-1] and self.__shortSMA[-1] - self.__longSMA[-1] < 15 
 
    def exitLongSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 1 and bar.getBid1() != 0
 
    def enterShortSignal(self, bar):#当短周期下穿 长周期，就入场做空，seg也要同方向
        return self.__shortSMA[-1] < self.__longSMA[-1] and self.__longSMA[-1] - self.__shortSMA[-1] < 15 
 
    def exitShortSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 2 and bar.getAsk1() != 0


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
    appconsant.logLogger.info(log)


def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    
    rootdir = appconsant.rootdir
    
    instrumentID = appconsant.instrumentID
    date = appconsant.date
    
    ISOTIMEFORMAT='%Y-%m-%d%H%M%S'
    appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+ time.strftime( ISOTIMEFORMAT, time.localtime() )+'log.txt', loglevel=1, logger="log").getlog()
    
    
    
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
    myStrategy = MyStrategyRSI(feed,instrumentID, 660,200,100,57,45,appconsant.rangespan_nwaveticket,appconsant.rangespan_ma,appconsant.rangespan_range,appconsant.rangespan_span,appconsant.rangespan_stoploss,appconsant.rangespan_y,appconsant.rangespan_n)
     
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangeupper", myStrategy.getxrangeupper())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangelower", myStrategy.getxrangelower())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("SMA", myStrategy.getlongSMA())
    plt.getOrCreateSubplot("diff").addDataSeries("smadiff", myStrategy.getsmapricediffDS())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("bigupdown", myStrategy.getBigUpDown())
    plt.getOrCreateSubplot("diff").addDataSeries("waveds", myStrategy.getWave())
#     plt.getInstrumentSubplot("test").addDataSeries("rangeupper", myStrategy.getrangeupper())
#     plt.getInstrumentSubplot("test").addDataSeries("rangelower", myStrategy.getrangelower())
    
#     plt.getOrCreateSubplot("big").addDataSeries("price", myStrategy.getBigUpDown())
    
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
#     
    printLog(myStrategy.getmoneyearn())
    printLog(myStrategy.getmoneyloss())
#     
#     printLog(myStrategy.gethuiguiinfo())
#     plt.plotdiffbar(waveseries)
    plt.plot()




# g = 
# print 

if __name__=="__main__": main()

