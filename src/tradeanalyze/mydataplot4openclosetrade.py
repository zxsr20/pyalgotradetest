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

logfile = ''

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,rangespan_nwaveticket,rangespan_ma,rangespan_range,rangespan_span,rangespan_stoploss,rangespan_y,rangespan_n,instrument_date):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__instrumentdate = instrument_date
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
#         self.__price_index = 0
        #用于交易结果统计
        self.lastmymoney = 0.0
        self.losstime = 0
        self.wintime = 0
        self.winmoney = 0.0
        self.lossmoney = 0.0
        
        self.rangeintime = 0
        self.pricejumpoutrange = 0

        self.__longPos = None
        self.__shortPos = None
        
        self.moneyearn = []
        self.moneyearntimes = []
        self.moneyloss = []
        
        self.buyprice = 0.0
        self.nonewtop = 0
        self.topprice = 0.0
        
        data_config = conf.getInstrumentInfo(instrument) 
        
        self.high = 0.0
        self.lower = 0.0
        
        
        #本策略相关
        self.openPriceDS = dataseries.SequenceDataSeries(100000)#use to draw map
        self.closePriceDS = dataseries.SequenceDataSeries(100000)#use to draw map
        self.period = 720
        
        self.wavetickets = []
        self.waveDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.rangeUpperDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.rangeLowerDS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        
        
        
        
        
        
        

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
#         printLog(barLog)
        if len(self.__priceDS) == 1: 
            logging.getLogger('trade').info(str(self.rangespan_n)+barLog)
            
        if len(self.__priceDS) % self.
        
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
#         printLog('wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave))
         
        self.wavetickets.append(tp)
         
         
        if len(self.__priceDS) < self.rangespan_ma:
            return
         
         
        priceds = []
        for i in range(self.rangespan_ma):
            priceds.append(round(self.__priceDS[-(i+1)],0))
        dic = {}
        for item in priceds:
            dic[item] = dic.get(item, 0) + 1
        dic = sorted(dic.items())
        numds = []
        pds = []
        for item in dic:
            numds.append(item[1]) 
            pds.append(item[0]) 
#         print(dic)
#         print numds
#         print 'oldpricerange:'+str(pds[0])+' '+str(pds[len(pds)-1])
         
         
        ids = mymost_close_array(numds,len(numds),self.rangespan_range)
#         print str(ids)
#         print str(pds)
        rangeLower = pds[ids[0]]
        rangeUpper = pds[ids[1]]
 
        self.rangeLowerDS.appendWithDateTime(bar.getDateTime(),rangeLower)
        self.rangeUpperDS.appendWithDateTime(bar.getDateTime(),rangeUpper)
         
        if rangeUpper - rangeLower <= self.rangespan_span:
             
            self.rangeintime += 1
            self.xrangeLowerDS.appendWithDateTime(bar.getDateTime(),rangeLower)
            self.xrangeUpperDS.appendWithDateTime(bar.getDateTime(),rangeUpper)
             
            if len(self.xrangeUpperDS) >= 2:
                if self.xrangeUpperDS[-2] == None:#如果进入了range
                    printLog('进入一个新的range')
#                     if len(self.__priceDS) - 1 - self.lastrangeinindex < self.rangedistance and :#如果这次进入range，离前一个range的ticket个数小于20，那么就合并两个的rangeup和lower做为交易的入场条件
#                         printLog('合并，新的range离上一个range的距离小于'+str(self.rangedistance))
#                         self.mergerange = 1
                    if abs(self.__priceDS[self.lastrangeinindex - 1] - self.__priceDS[-1]) < self.rangepricedistance:
                        printLog('合并，新的range离上一个range的价格距离小于'+str(self.rangepricedistance)+' '+str(self.__priceDS[self.lastrangeinindex - 1])+' '+str(self.__priceDS[-1]))
                        self.mergerange = 1
                        #如果需要合并的话，就要吧xrangeLowerDS前面填充none的数据为rangelower的数据
#                         i = -2
#                         while(True):
#                             print 'self.xrangeLowerDS[i]'+str(self.xrangeLowerDS[i])
#                             if self.xrangeLowerDS[i] == None:
#                                 self.xrangeLowerDS[i] = self.rangeLowerDS[i]
#                                 self.xrangeUpperDS[i] = self.rangeUpperDS[i]
#                                 i -= 1 
#                             else:
#                                 break
                         
                         
                    elif len(self.__priceDS) - 1 - self.lastrangeinindex >= self.rangedistance:  
                        printLog('不合并，新的range离上一个range的距离大于'+str(self.rangedistance))
                        self.mergerange = 0
                    elif abs(self.__priceDS[self.lastrangeinindex - 1] - self.__priceDS[-1]) >= self.rangepricedistance:
                        printLog('不合并，新的range离上一个range的价格距离大于'+str(self.rangedistance))
                        self.mergerange = 0
                     
#             if self.rangeintime > 10:
            self.lastrangeupper = rangeUpper
            self.lastrangelower = rangeLower
             
            if  self.mergerange == 1:
                if self.mergerangeUpper < rangeUpper:
                    printLog('新的range离上一个range的距离小于'+str(self.rangedistance)+',并且原来的上线小于当前上线，更新为当前mergerangeUpper为'+str(rangeUpper))
                    self.mergerangeUpper = rangeUpper
                if self.mergerangeLower == 0:
                    self.mergerangeLower = rangeLower   
                if self.mergerangeLower > rangeLower:
                    printLog('新的range离上一个range的距离小于'+str(self.rangedistance)+',并且原来的下线线大于当前下线，更新为当前mergerangeLower为'+str(rangeLower))
                    self.mergerangeLower = rangeLower
            else:
                self.mergerangeUpper = rangeUpper
                self.mergerangeLower = rangeLower
                 
        else:
            self.rangeintime = 0
            self.xrangeLowerDS.appendWithDateTime(bar.getDateTime(),None)
            self.xrangeUpperDS.appendWithDateTime(bar.getDateTime(),None)
            if len(self.xrangeUpperDS) >= 2:
                if self.xrangeUpperDS[-2] != None:#如果当前是离开了一个range，记录下离开的位置
                    printLog('离开range，记录下离开的点为'+str(len(self.__priceDS) - 1))
                    self.lastrangeinindex = len(self.__priceDS) - 1
 
        printLog('当前rangeUpper为 '+str(rangeUpper)+'当前rangeLower为'+str(rangeLower))
        printLog('当前mergerangeUpper为 '+str(self.mergerangeUpper)+'当前mergerangeLower为'+str(self.mergerangeLower))
        #交易相关
        if self.lastmymoney == 0:
            self.lastmymoney = 1000000
         
#         if rangeUpper - rangeLower > self.rangespan_span:#趋势
#             printLog('当前为趋势，价格范围为'+str(rangeLower)+'到 '+str(rangeUpper))
#         else:
#             printLog('当前为盘整，价格范围为'+str(rangeLower)+'到 '+str(rangeUpper))
         
        if self.__longPos is not None or self.__shortPos is not None:#已入场
             
            if self.__longPos is not None:#已做多
                  
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                    print self.buyprice
                    print self.__longPos.getEntryOrder().getAvgFillPrice()
                 
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
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做多平仓')
                    self.buyticketrangeLower = 0
                    self.buyticketrangeUpper = 0
#                 elif self.nonewtop > self.rangespan_n/4 and self.buyprice - self.__priceDS[-1] > 0:
#                     printLog('四分之一的n没有突破，反而价亏了')
#                     self.__longPos.exitMarket()
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做多平仓')
#                 elif rangeUpper - rangeLower < self.rangespan_span:#当前还是盘整
#                     if self.__priceDS[-1] < rangeUpper:
#                         printLog('做多，但是价格重新进入范围内，则平仓')
#                         self.__longPos.exitMarket()
#                         self.buyprice = 0
#                         self.nonewtop =  0
#                         self.topprice = 0.0
#                         printLog('做多平仓')
#                 elif self.buyprice - self.__priceDS[-1] >= self.rangespan_stoploss:#已亏损
#                     printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
#                     self.__longPos.exitMarket()
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做多平仓')
                elif self.__priceDS[-1] - self.buyticketrangeLower  <= 0:#已亏损
                    printLog('当前价格低于下线,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
                    self.__longPos.exitMarket()
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做多平仓')
                    self.buyticketrangeLower = 0
                    self.buyticketrangeUpper = 0
#                 elif self.__priceDS[-1] < self.__priceDS[-2] and self.__priceDS[-1] < self.buyprice:
#                     printLog('价格开始下跌超过买价')
#                     self.__longPos.exitMarket()
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做多平仓')
            if self.__shortPos is not None:#已做空
                  
                if self.buyprice == 0:#获得购买价格
                    self.buyprice = self.__priceDS[-1]
                    print self.buyprice
                    print self.__shortPos.getEntryOrder().getAvgFillPrice()
                    
                #没有创新高
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
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做空平仓') 
                    self.buyticketrangeLower = 0
                    self.buyticketrangeUpper = 0
                     
#                 elif self.nonewtop > self.rangespan_n/2 and self.__priceDS[-1] - self.buyprice > 0:
#                     printLog('二分之一的n没有突破，反而价亏了')
#                     self.__shortPos.exitMarket()
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做空平仓')
#                 elif rangeUpper - rangeLower < self.rangespan_span:
#                     if self.__priceDS[-1] > rangeLower:
#                         printLog('做空，但是价格重新进入范围内，则平仓')
#                         self.__shortPos.exitMarket()
#                         self.buyprice = 0
#                         self.nonewtop =  0
#                         self.topprice = 0.0
#                         printLog('做空平仓')
#                 elif self.__priceDS[-1] - self.buyprice >= self.rangespan_stoploss:#已亏损
#                     printLog('当前亏损大于止损点,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
#                     self.__shortPos.exitMarket()
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做空平仓')
                elif self.__priceDS[-1] - self.buyticketrangeUpper >= 0:
                    printLog('当前价格大于上线,准备离场self.buyticketrangeUpper'+str(self.buyticketrangeUpper)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
                    self.__shortPos.exitMarket()
                    self.buyprice = 0
                    self.nonewtop =  0
                    self.topprice = 0.0
                    printLog('做空平仓')
                    self.buyticketrangeLower = 0
                    self.buyticketrangeUpper = 0
#                 elif  self.lastrangelower - self.__priceDS[-1] >= 0:#已亏损
#                     printLog('当前亏损大于下线,准备离场buyprice'+str(self.buyprice)+' -price'+str(self.__priceDS[-1])+' >=stoploss'+str(self.rangespan_stoploss))
#                     self.__shortPos.exitMarket()
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做空平仓')
#                 elif self.__priceDS[-1] > self.__priceDS[-2] and self.__priceDS[-1] > self.buyprice:
#                     printLog('价格开始上升超过买价')
#                     self.__shortPos.exitMarket()
#                     self.buyprice = 0
#                     self.nonewtop =  0
#                     self.topprice = 0.0
#                     printLog('做空平仓')
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
             
             
             
            if rangeUpper - rangeLower < self.rangespan_span and self.rangeintime > 20:#趋势
                 
                if self.__priceDS[-1] > rangeUpper:
                    self.pricejumpoutrange = 1
                if self.__priceDS[-1] < rangeLower:
                    self.pricejumpoutrange = 2
                 
                 
                if self.__priceDS[-1] > self.mergerangeUpper+self.rangespan_y:
                    printLog('当前价格大于范围价格加y'+str(self.rangespan_y)+'，准备做多')
                    shares = 1
                     
                    printLog('做多之前我的钱'+str(self.getBroker().getCash()))
                    self.__longPos = self.enterLong(self.__instrument, shares, True)
                    self.buyticketrangeLower = self.lastrangelower
                    self.buyticketrangeUpper = self.lastrangeupper
                     
                    printLog('self.buyticketrangeLower'+str(self.buyticketrangeLower)+'self.buyticketrangeUpper'+str(self.buyticketrangeUpper))
                elif self.__priceDS[-1] < self.mergerangeLower - self.rangespan_y:
                    printLog('当前价格小于于范围价格减y'+str(self.rangespan_y)+'，准备做空')
                    shares = 1
                     
                    printLog('做空之前我的钱'+str(self.getBroker().getCash()))
                    self.__shortPos = self.enterShort(self.__instrument, shares, True)
                    self.buyticketrangeLower = self.lastrangelower
                    self.buyticketrangeUpper = self.lastrangeupper
                    printLog('self.buyticketrangeLower'+str(self.buyticketrangeLower)+'self.buyticketrangeUpper'+str(self.buyticketrangeUpper))
#                 elif self.__priceDS[-1] > rangeLower + self.rangespan_span/10 and self.pricejumpoutrange == 2:#如果价格超过下限后又重新进入范围
#                     printLog('如果价格超过下限后又重新进入范围'+'，准备做多')
#                     shares = 1
#                     
#                     printLog('做多之前我的钱'+str(self.getBroker().getCash()))
#                     self.__longPos = self.enterLong(self.__instrument, shares, True)
#                     self.pricejumpoutrange = 0
#                 elif self.__priceDS[-1] < rangeUpper - self.rangespan_span/10 and self.pricejumpoutrange == 1:#如果价格超过上限后又重新进入范围
#                     printLog('如果价格超过上限后又重新进入范围'+'，准备做空')
#                     shares = 1
#                     
#                     printLog('做空之前我的钱'+str(self.getBroker().getCash()))
#                     self.__shortPos = self.enterShort(self.__instrument, shares, True)
#                     self.pricejumpoutrange = 0
            elif self.lastrangeupper != 0.0 and self.lastrangelower != 0.0:
                if self.__priceDS[-1] > self.mergerangeUpper+self.rangespan_y and self.__priceDS[-1] < self.lastrangeupper+self.rangespan_y+20:
                    printLog('当前为趋势，但价格大于最后一个盘整的范围价格加y'+str(self.rangespan_y)+'，准备做多')
                    shares = 1
                     
                    printLog('做多之前我的钱'+str(self.getBroker().getCash()))
                    self.__longPos = self.enterLong(self.__instrument, shares, True)
 
                    self.buyticketrangeLower = self.lastrangelower
                    self.buyticketrangeUpper = self.lastrangeupper
                    self.lastrangeupper = 0.0
                    self.lastrangelower = 0.0
                    printLog('self.buyticketrangeLower'+str(self.buyticketrangeLower)+'self.buyticketrangeUpper'+str(self.buyticketrangeUpper))
                elif self.__priceDS[-1] < self.mergerangeLower - self.rangespan_y and self.__priceDS[-1] > self.lastrangeupper-self.rangespan_y-20:
                    printLog('当前为趋势，但价格小于最后一个盘整的范围价格减y'+str(self.rangespan_y)+'，准备做空')
                    shares = 1
                     
                    printLog('做空之前我的钱'+str(self.getBroker().getCash()))
                    self.__shortPos = self.enterShort(self.__instrument, shares, True)
                    self.buyticketrangeLower = self.lastrangelower
                    self.buyticketrangeUpper = self.lastrangeupper
                    self.lastrangeupper = 0.0
                    self.lastrangelower = 0.0


        
        
        
                      
        
        
        
        
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
    pass
#     logging.getLogger('trade').info(log)

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
    

  

#     mylogger.printlog(log)

    


def main():
    # Load the yahoo feed from the CSV file
    # feed = yahoofeed.Feed()toting
    # feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    print os.path.sep
    rootdir = appconsant.rootdir
    instrumentID = appconsant.instrumentID
    date = appconsant.date
#     ISOTIMEFORMAT='%Y-%m-%d%H%M%S'
# #     appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+ time.strftime( ISOTIMEFORMAT, time.localtime() )+'log.txt', loglevel=1, logger="log").getlog()
# #     appconsant.logLogger =  Logger.Logger(logname=instrumentID+date+'log.txt', loglevel=1, logger="log").getlog()
#     mylogger.changeLoggerFile(instrumentID+date+ time.strftime( ISOTIMEFORMAT, time.localtime() )+'log.txt')
    
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
    ids = ['pp1701','ru1701','v1701','y1701','zn1701','WH1701','SR705']
    for id in ids:
        
    
        feed = yahoofeed.Feed()
        feed.addBarsFromCSV(instrumentID, "../ctpdataanalyze/"+date+instrumentID+".csv")
         
        
    #     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
         
    #     logfile = appconsant.logfile
        # Evaluate the strategy with the feed's bars.
        #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
        myStrategy = MyStrategyRSI(feed,instrumentID, 660,200,100,57,45,appconsant.rangespan_nwaveticket,appconsant.rangespan_ma,appconsant.rangespan_range,appconsant.rangespan_span,appconsant.rangespan_stoploss,appconsant.rangespan_y,appconsant.rangespan_n,date)
         
        # Attach a returns analyzers to the strategy.
        returnsAnalyzer = returns.Returns()
        myStrategy.attachAnalyzer(returnsAnalyzer)
         
        # Attach the plotter to the strategy.
        plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
        # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
         
        plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangeupper", myStrategy.getxrangeupper())
        plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangelower", myStrategy.getxrangelower())
    #     plt.getOrCreateSubplot("wave").addDataSeries("waveds", myStrategy.getWave())
        plt.getOrCreateSubplot("EMA").addDataSeries("LEMA", myStrategy.getlongEMA())
        plt.getOrCreateSubplot("EMA").addDataSeries("SEMA", myStrategy.getshortEMA())
    #     plt.getOrCreateSubplot("WMA").addDataSeries("LWMA", myStrategy.getlongWMA())
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
