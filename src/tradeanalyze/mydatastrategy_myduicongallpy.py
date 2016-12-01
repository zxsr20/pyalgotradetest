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
from pyalgotrade.technical import ma, macd
# from pyalgotrade.technical import rsi
# from pyalgotrade.technical import cross
# from pyalgotrade.dataseries import DataSeries
# import tradeanalyze.data_struct
from tradeanalyze.data_struct import *
import time
from pyalgotrade.technical import cross
import codecs
logfile = ''

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument1,instrument2, longSMA, shortSMA, rsiPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument1 = instrument1
        self.__instrument2 = instrument2
#         self.__instrumentdate = instrument_date
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS1 = feed[instrument1].getPriceDataSeries()
        self.__priceDS2 = feed[instrument2].getPriceDataSeries()
#         self.__price_index = 0
        
        
        data_config = conf.getInstrumentInfo(instrument1) 
        
        
        
        #交易统计相关
        self.moneyearn = []
        self.moneyearntimes = []
        self.moneyloss = []
        
        self.buyprice1 = 0.0
        self.buyprice2 = 0.0
        self.nonewtop11 = 0
        self.nonewtop12 = 0
        self.topprice11 = 0.0
        self.topprice12 = 0.0
        
        self.nonewtop13 = 0
        self.nonewtop14 = 0
        self.topprice13 = 0.0
        self.topprice14 = 0.0
        
        self.nonewtop21 = 0
        self.topprice21 = 0.0
        self.nonewtop22 = 0
        self.topprice22 = 0.0
        self.huice_during1 = 0.0
        self.huice_during2 = 0.0
        self.outhuice_during1 = 0
        self.outhuice_during2 = 0

        self.lastmymoney = 0.0
        self.losstime = 0
        self.wintime = 0
        self.winmoney = 0.0
        self.lossmoney = 0.0
        
        self.equalcount = 0
        self.equalcount2 = 0
        self.stress = 0
        
        
        #指标相关
#         self.__longEMA = ma.EMA(self.__priceDS, longSMA)
#         self.__shortEMA = ma.EMA(self.__priceDS, shortSMA)
        
        

        #交易元素
        self.__longPos11 = None
        self.__shortPos11 = None
        self.__longPos12 = None
        self.__shortPos12 = None
        self.__longPos13 = None
        self.__shortPos13 = None
        self.__longPos14 = None
        self.__shortPos14 = None
        
        
        self.__longPos21 = None
        self.__shortPos21 = None
        self.__longPos22 = None
        self.__shortPos22 = None
        
        #策略相关元素
        
        self.__nwaveticket=300
        
        self.lastbar1 = None
        self.lastbar2 = None
        self.bid1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.ask1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.bid1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.ask1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.pricechaDS =  dataseries.SequenceDataSeries(100000)
        self.pricechawaveDS =  dataseries.SequenceDataSeries(100000)
        self.price1waveDS =  dataseries.SequenceDataSeries(100000)
        self.price2waveDS =  dataseries.SequenceDataSeries(100000)
        self.maxcha = 0
        self.mincha = 0
        self.pricemax1 = 0
        self.pricemin2 = 0
        
        self.speed1 = 0.0
        self.speed2 = 0.0
        self.outspeed1 = 0
        self.outspeed2 = 0
        self.duicong = 0
        
        self.ruchang1 = 0
        self.waven = 4
        self.n = 30#有n个点没有创新高
        self.a = 5 #亏损了a个点平仓
        self.b = 4 #盈利了b个点，并且c个点没有创新高，平
        self.c = 10
#         self.e = 2
        self.d = 4 #盈利了d个点，并且f个点没有创新高，平
        self.f = 10 
        self.g = 6 #盈利了g个点，并且h个点没有创新高，平
        self.h = 5 
        self.p = 3#在100个点从最高点回撤了p个点，并且价格大于之前做空的点，继续做空
        
        
        self.x = 3 #价差的macd小于x，开始向外对冲
#         self.y = 0.25 #价差dmacd大于y，开始向内对冲
        self.shortema = 50
        self.longema = 110
        self.signema = 30
        self.pricechamacdDs = macd.MACD(self.__priceDS1,self.shortema,self.longema,self.signema)
        self.pricechahisDs = self.pricechamacdDs.getHistogram()
        
            
    

    def onBars(self, bars):
        
        # when dirction is change ,then save the price in segmentds
#         bar = bars[self.__instrument]
        bardateTime = None
        if bars.getBar(self.__instrument1)!=None:#品种一，价格高的
            self.whichticket = 1
            bar = bars.getBar(self.__instrument1)
            self.lastbar1 = bar
            bardateTime = bar.getDateTime()
            
            self.bid1DS.appendWithDateTime(bar.getDateTime(), bar.getBid1())
            self.ask1DS.appendWithDateTime(bar.getDateTime(), bar.getAsk1())
            
            if len(self.__priceDS1) > 10:
                priceds = self.__priceDS1[-9:]
                upper = max(priceds)
                lower = min(priceds)
                self.speed1 = (upper - lower)
                if self.speed1 > self.p:
                    self.outspeed1 = 1
                
            tp = CTicketWave()
            tp.idx = len(self.bid1DS)+1 
            tick_idx_start = len(self.bid1DS) - self.__nwaveticket
            if tick_idx_start < 0:
                tick_idx_start = 0
            tp.tick_idx_start = tick_idx_start
            tp.tick_idx_end = len(self.bid1DS)-1
#             tp.price_start = self.__priceDS[tick_idx_start]
#             tp.price_end = self.__priceDS[-1]
            priceds = self.bid1DS[tick_idx_start:len(self.bid1DS)]
            tp.upper = max(priceds)
            tp.lower = min(priceds)
            i1 = priceds.index(tp.upper)
            i2 = priceds.index(tp.lower)
            if i1 > i2:
                tp.price_wave =  tp.upper - tp.lower
            else:
                tp.price_wave =  -(tp.upper - tp.lower)
    #         print ' '+str(tp.price_wave)
            self.price1waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
#             if bar.getPrice() > self.pricemax1:
#                 self.pricemax1 = bar.getPrice()
            __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
            barTime = __barTime[0:len(__barTime)-3]
            barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
            if barTime > '2013-12-18 10:42:08' and barTime < '2013-12-18 11:00:08':
                printLog(self.__instrument1+barLog)
            
            
            if len(self.price1waveDS) > 1:
                print 'wave '+str(self.price1waveDS[-2])+' '+str(self.price1waveDS[-1])
                if ((self.price1waveDS[-2] > 0 and self.price1waveDS[-1] < 0) or (self.price1waveDS[-2] < 0 and self.price1waveDS[-1] > 0)) :
                    self.stress = self.price1waveDS[-1]
                    self.beginmarket = 1
                    print 'self.stress'+str(self.stress)
                
                if ((self.stress < 0 and self.price1waveDS[-1] < 0) or (self.stress > 0 and self.price1waveDS[-1] > 0)) and abs(self.price1waveDS[-1]) - abs(self.stress) >=3 :
                    if self.price1waveDS[-2] == self.price1waveDS[-1]:
                        self.equalcount += 1
                    else:
                        self.equalcount = 0 
                    print 'abs(self.price1waveDS[-1]) - abs(self.stress)'+str(abs(self.price1waveDS[-1]) - abs(self.stress))+'self.equalcount'+str(self.equalcount)
                    if self.equalcount > 3 and self.beginmarket == 1:
                        if self.price1waveDS[-1] > 0 and self.__shortPos11 == None:
                            shares = 1
                            printLog(self.__instrument1+'self.equalcount > 6做空之前我的钱'+str(self.getBroker().getCash()))
                            self.__shortPos11 = self.enterShort(self.__instrument1, shares, True)
                            self.continuein = 1
                            self.beginmarket = 0
                        elif self.price1waveDS[-1] < 0 and self.__longPos11 == None:
                            shares = 1
                            printLog(self.__instrument1+'self.equalcount > 6做多之前我的钱'+str(self.getBroker().getCash()))
                            self.__longPos11 = self.enterLong(self.__instrument1, shares, True)
                            self.continuein = 1
                            self.beginmarket = 0
                else:
                    self.equalcount = 0
                    self.continuein = 0 #如果wave波段不是当前的波段，那么就不再二次入场
                    
                
                    
                
                
                if self.__shortPos11 != None and self.__shortPos11.entryFilled() and self.continuein == 1:
                    if self.__priceDS1[-1] - self.__shortPos11.getEntryOrder().getAvgFillPrice() > 3 :
                        if self.price1waveDS[-2] == self.price1waveDS[-1]:
                            self.equalcount2 += 1
                        else:
                            self.equalcount2 = 0
                    else:
                        self.equalcount2 = 0
                    if self.equalcount2 > 3 and self.__shortPos12 == None:
                        shares = 1
                        printLog(self.__instrument1+'self.equalcount2 > 3做空之前我的钱'+str(self.getBroker().getCash()))
                        self.__shortPos12 = self.enterShort(self.__instrument1, shares, True)
                        
                if self.__longPos11 != None and self.__longPos11.entryFilled() and self.continuein == 1:
                    if self.__longPos11.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1] > 3 :
                        if self.price1waveDS[-2] == self.price1waveDS[-1]:
                            self.equalcount2 += 1
                        else:
                            self.equalcount2 = 0
                    else:
                        self.equalcount2 = 0
                    if self.equalcount2 > 3 and self.__longPos12 == None:
                        shares = 1
                        printLog(self.__instrument1+'self.equalcount2 > 3做多之前我的钱'+str(self.getBroker().getCash()))
                        self.__longPos12 = self.enterLong(self.__instrument1, shares, True)
                
            
            #出场
            if self.__shortPos11 != None and self.__shortPos11.entryFilled():

                if self.topprice11 == 0:
                    self.topprice11 = self.__priceDS1[-1]
                if self.topprice11 < self.__priceDS1[-1]:#没有创新高
                    self.nonewtop11 += 1
                else:
                    self.topprice11 = self.__priceDS1[-1]#创新高
                    self.nonewtop11 =  0   
                    
                if self.nonewtop11 > self.n:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经有'+str(self.nonewtop11)+'个ticket没有创新低，准备平仓')
                    self.__shortPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                    
                    
                elif self.__priceDS1[-1] - self.__shortPos11.getEntryOrder().getAvgFillPrice() > self.a:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经亏损'+str(self.a)+'，准备平仓')
                    self.__shortPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                    
                    #然后如果继续亏损，就继续做空
                    shares = 1
                    printLog(self.__instrument1+'做空之前我的钱'+str(self.getBroker().getCash()))
                    self.__shortPos13 = self.enterShort(self.__instrument1, shares, True)

                    
                elif  self.__priceDS1[-1] - self.topprice11 > self.x and self.__shortPos11.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > 0:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经回撤'+str(self.b)+'，准备平仓')
                    self.__shortPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif self.__shortPos11.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.d and self.nonewtop11 > self.f:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__shortPos11.exitMarket()
                    self.nonewtop11 =  0 
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif self.__shortPos11.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.g:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经盈利'+str(self.g)+'，准备平仓')
                    self.__shortPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做空平仓')
            
                    
                    
#                     if self.price1waveDS[-1] >= self.waven and self.__priceDS1[-1] == tp.upper:
#                         print priceds
#                         shares = 1
#                         printLog(self.__instrument1+'做空之前我的钱'+str(self.getBroker().getCash()))
#                         self.__shortPos11 = self.enterShort(self.__instrument1, shares, True)
#                         self.ruchang1 = 1#向外对冲
                    
            if self.__shortPos12 != None and self.__shortPos12.entryFilled():
                if self.topprice12 == 0:
                    self.topprice12 = self.__priceDS1[-1]
                if self.topprice12 < self.__priceDS1[-1]:#没有创新高
                    self.nonewtop12 += 1
                else:
                    self.topprice12 = self.__priceDS1[-1]#创新高
                    self.nonewtop12 =  0   
                    
                if self.nonewtop12 > self.n:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经有'+str(self.nonewtop12)+'个ticket没有创新低，准备平仓')
                    self.__shortPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                    
                elif self.__priceDS1[-1] - self.__shortPos12.getEntryOrder().getAvgFillPrice() >= self.a:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经亏损'+str(self.a)+'，准备平仓')
                    self.__shortPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif  self.__priceDS1[-1] - self.topprice12 > self.x and self.__shortPos12.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > 0:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__shortPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif self.__shortPos12.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.d and self.nonewtop12 > self.f:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经盈利'+str(self.d)+'，准备平仓')
                    self.__shortPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif self.__shortPos12.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.g:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经盈利'+str(self.g)+'，准备平仓')
                    self.__shortPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做空平仓')
            
                
            #出场
            if self.__longPos11 != None and self.__longPos11.entryFilled():

                if self.topprice11 == 0:
                    self.topprice11 = self.__priceDS1[-1]
                if self.topprice11 > self.__priceDS1[-1]:#没有创新高
                    self.nonewtop11 += 1
                else:
                    self.topprice11 = self.__priceDS1[-1]#创新高
                    self.nonewtop11 =  0   
                    
                if self.nonewtop11 > self.n:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经有'+str(self.nonewtop11)+'个ticket没有创新低，准备平仓')
                    self.__longPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                    
                elif self.__longPos11.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.a:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经亏损'+str(self.a)+'，准备平仓')
                    self.__longPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                    
                    shares = 1
                    printLog(self.__instrument1+'self.equalcount > 6做多之前我的钱'+str(self.getBroker().getCash()))
                    self.__longPos13 = self.enterLong(self.__instrument1, shares, True)

                elif  self.topprice11 - self.__priceDS1[-1]  > self.x and self.__priceDS1[-1] - self.__longPos11.getEntryOrder().getAvgFillPrice() > 0:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__longPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                elif self.__priceDS1[-1] - self.__longPos11.getEntryOrder().getAvgFillPrice()  > self.d and self.nonewtop11 > self.f:
                    printLog(self.__instrument1+'self.equalcount > 6当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__longPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                elif self.__priceDS1[-1] - self.__longPos11.getEntryOrder().getAvgFillPrice()  > self.g :
                    printLog(self.__instrument1+'self.equalcount > 6当前已经盈利'+str(self.g)+'，准备平仓')
                    self.__longPos11.exitMarket()
                    self.nonewtop11 =  0
                    self.topprice11 = 0.0
                    printLog(self.__instrument1+'做多平仓')
            
                    
                    
#                     if self.price1waveDS[-1] >= self.waven and self.__priceDS1[-1] == tp.upper:
#                         print priceds
#                         shares = 1
#                         printLog(self.__instrument1+'做空之前我的钱'+str(self.getBroker().getCash()))
#                         self.__shortPos11 = self.enterShort(self.__instrument1, shares, True)
#                         self.ruchang1 = 1#向外对冲
                    
            if self.__longPos12 != None and self.__longPos12.entryFilled():
                if self.topprice12 == 0:
                    self.topprice12 = self.__priceDS1[-1]
                if self.topprice12 > self.__priceDS1[-1]:#没有创新高
                    self.nonewtop12 += 1
                else:
                    self.topprice12 = self.__priceDS1[-1]#创新高
                    self.nonewtop12 =  0   
                    
                if self.nonewtop12 > self.n:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经有'+str(self.nonewtop12)+'个ticket没有创新低，准备平仓')
                    self.__longPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                    
                elif self.__longPos12.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  >= self.a:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经亏损'+str(self.a)+'，准备平仓')
                    self.__longPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                elif  self.topprice12 - self.__priceDS1[-1]  > self.x and self.__priceDS1[-1] - self.__longPos12.getEntryOrder().getAvgFillPrice()  > 0:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__longPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                elif self.__priceDS1[-1] - self.__longPos12.getEntryOrder().getAvgFillPrice()  > self.d and self.nonewtop12 > self.f:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经盈利'+str(self.d)+'，准备平仓')
                    self.__longPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                elif self.__priceDS1[-1] - self.__longPos12.getEntryOrder().getAvgFillPrice()  > self.g:
                    printLog(self.__instrument1+'self.equalcount2 > 3当前已经盈利'+str(self.g)+'，准备平仓')
                    self.__longPos12.exitMarket()
                    self.nonewtop12 =  0
                    self.topprice12 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                    
                    
                
            if self.__shortPos13 != None and self.__shortPos13.entryFilled():
                if self.topprice13 == 0:
                    self.topprice13 = self.__priceDS1[-1]
                if self.topprice13 < self.__priceDS1[-1]:#没有创新高
                    self.nonewtop13 += 1
                else:
                    self.topprice13 = self.__priceDS1[-1]#创新高
                    self.nonewtop13 =  0   
                    
                if self.nonewtop13 > self.n:
                    printLog(self.__instrument1+'当前已经有'+str(self.nonewtop13)+'个ticket没有创新低，准备平仓')
                    self.__shortPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                    
                elif self.__priceDS1[-1] - self.__shortPos13.getEntryOrder().getAvgFillPrice() >= self.a:
                    printLog(self.__instrument1+'当前已经亏损'+str(self.a)+'，准备平仓')
                    self.__shortPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif  self.__priceDS1[-1] - self.topprice113  > self.x and self.__shortPos13.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > 0:
                    printLog(self.__instrument1+'当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__shortPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif self.__shortPos13.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.d and self.nonewtop13 > self.f:
                    printLog(self.__instrument1+'当前已经盈利'+str(self.d)+'，准备平仓')
                    self.__shortPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做空平仓')
                elif self.__shortPos13.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.g:
                    printLog(self.__instrument1+'当前已经盈利'+str(self.g)+'，准备平仓')
                    self.__shortPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做空平仓')
            
                
            #出场
            if self.__longPos13 != None and self.__longPos13.entryFilled():

                if self.topprice13 == 0:
                    self.topprice13 = self.__priceDS1[-1]
                if self.topprice13 > self.__priceDS1[-1]:#没有创新高
                    self.nonewtop13 += 1
                else:
                    self.topprice13 = self.__priceDS1[-1]#创新高
                    self.nonewtop13 =  0   
                    
                if self.nonewtop13 > self.n:
                    printLog(self.__instrument1+'当前已经有'+str(self.nonewtop13)+'个ticket没有创新低，准备平仓')
                    self.__longPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                    
                elif self.__longPos13.getEntryOrder().getAvgFillPrice() - self.__priceDS1[-1]  > self.a:
                    printLog(self.__instrument1+'当前已经亏损'+str(self.a)+'，准备平仓')
                    self.__longPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                    

                elif  self.topprice13 - self.__priceDS1[-1]   > self.x and self.__priceDS1[-1] - self.__longPos13.getEntryOrder().getAvgFillPrice()   > 0:
                    printLog(self.__instrument1+'当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__longPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                elif self.__priceDS1[-1] - self.__longPos13.getEntryOrder().getAvgFillPrice()   > self.d and self.nonewtop13 > self.f:
                    printLog(self.__instrument1+'当前已经盈利'+str(self.b)+'，准备平仓')
                    self.__shortPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做多平仓')
                elif self.__priceDS1[-1] - self.__longPos13.getEntryOrder().getAvgFillPrice()   > self.g:
                    printLog(self.__instrument1+'当前已经盈利'+str(self.g)+'，准备平仓')
                    self.__longPos13.exitMarket()
                    self.nonewtop13 =  0
                    self.topprice13 = 0.0
                    printLog(self.__instrument1+'做多平仓')
            
                    
                    
#                     if self.price1waveDS[-1] >= self.waven and self.__priceDS1[-1] == tp.upper:
#                         print priceds
#                         shares = 1
#                         printLog(self.__instrument1+'做空之前我的钱'+str(self.getBroker().getCash()))
#                         self.__shortPos11 = self.enterShort(self.__instrument1, shares, True)
#                         self.ruchang1 = 1#向外对冲
    

                    
            
        
        if bars.getBar(self.__instrument2)!=None:#品种二，价格低的
            self.whichticket = 2
            bar = bars.getBar(self.__instrument2)
            self.lastbar2 = bar
            bardateTime = bar.getDateTime()
            
            self.bid1DS_another.appendWithDateTime(bar.getDateTime(), bar.getBid1())
            self.ask1DS_another.appendWithDateTime(bar.getDateTime(), bar.getAsk1())
            
            if len(self.__priceDS2) > 10:
                priceds = self.__priceDS2[-9:]
                upper = max(priceds)
                lower = min(priceds)
                self.speed2 = (upper - lower)
                if self.speed2 > self.p:
                    self.outspeed2 = 1
                
            
#             if bar.getPrice() > self.pricemax1:
#                 self.pricemax1 = bar.getPrice()
            __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
            barTime = __barTime[0:len(__barTime)-3]
            barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
#             printLog(self.__instrument2+barLog)
            
            
            tp = CTicketWave()
            tp.idx = len(self.bid1DS_another)+1
            tick_idx_start = len(self.bid1DS_another) - self.__nwaveticket
            if tick_idx_start < 0:
                tick_idx_start = 0
            tp.tick_idx_start = tick_idx_start
            tp.tick_idx_end = len(self.bid1DS_another)-1
#             tp.price_start = self.__priceDS[tick_idx_start]
#             tp.price_end = self.__priceDS[-1]
            priceds = self.bid1DS_another[tick_idx_start:len(self.bid1DS_another)]
            tp.upper = max(priceds)
            tp.lower = min(priceds)
            i1 = priceds.index(tp.upper)
            i2 = priceds.index(tp.lower)
            if i1 > i2:
                tp.price_wave =  tp.upper - tp.lower
            else:
                tp.price_wave =  -(tp.upper - tp.lower)
    #         print ' '+str(tp.price_wave)
            self.price2waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
            
            
            
        
                
#         if len(self.__priceDS1) == 1 and len(self.__priceDS2) == 1:
#             shares = 1
#             printLog(self.__instrument1+'做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getOpen()))
#             self.__longPos1 = self.enterLongLimit(self.__instrument1, self.lastbar1.getOpen(), shares, True)
#             self.buyprice = 0
#             shares = 1
#             printLog(self.__instrument2+'做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getClose()))
#             self.__shortPos2 = self.enterShortLimit(self.__instrument2, self.lastbar2.getClose(), shares, True)
#             self.buyprice2 = 0
#             self.duicong = 1#向外对冲
         
        if self.lastbar2 != None and self.lastbar1 != None:
            self.pricecha = self.lastbar1.getPrice() - self.lastbar2.getPrice()
            self.pricechaDS.appendWithDateTime(bardateTime, self.pricecha)
            if self.pricecha > self.maxcha:
                self.maxcha = self.pricecha
            elif self.pricecha < self.mincha or self.mincha == 0:
                self.mincha = self.pricecha    
#             if  len(self.pricechahisDs) > 0 and self.pricechahisDs[-1] > self.y:
#                 printLog('当前价差的macd为'+str(self.pricechahisDs[-1]))
                
            tp = CTicketWave()
            tp.idx = len(self.pricechaDS)+1
            tick_idx_start = len(self.pricechaDS) - self.__nwaveticket
            if tick_idx_start < 0:
                tick_idx_start = 0
            tp.tick_idx_start = tick_idx_start
            tp.tick_idx_end = len(self.pricechaDS)-1
#             tp.price_start = self.__priceDS[tick_idx_start]
#             tp.price_end = self.__priceDS[-1]
            priceds = self.pricechaDS[tick_idx_start:len(self.pricechaDS)]
            tp.upper = max(priceds)
            tp.lower = min(priceds)
            tp.price_wave = tp.upper - tp.lower
    #         print ' '+str(tp.price_wave)
            self.pricechawaveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
#             print >> self.logfile,'wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave)
            
            

    

    
    def onEnterOk(self, position):   
        if self.duicong == 1:
            if self.__longPos1 == position:#如果品种一对冲买多成功，品种二取消订单并且对冲挂单
                self.__shortPos2.cancelEntry()
                shares = 1
                printLog(self.__instrument2+'做空之前我的钱'+str(self.getBroker().getCash()))
                self.__shortPos2 = self.enterShort(self.__instrument2, shares, True)
                self.buyprice2 = 0
                self.duicong = 0
            elif self.__shortPos1 == position:
                self.__longPos2.cancelEntry()
                shares = 1
                printLog(self.__instrument2+'做多之前我的钱'+str(self.getBroker().getCash()))
                self.__longPos2 = self.enterLong(self.__instrument2, shares, True)
                self.buyprice2 = 0
                self.duicong = 0
            elif self.__shortPos2 == position:
                self.__longPos1.cancelEntry()
                shares = 1
                printLog(self.__instrument1+'做多之前我的钱'+str(self.getBroker().getCash()))
                self.__longPos1 = self.enterLong(self.__instrument1, shares, True)
                self.buyprice1 = 0
                self.duicong = 0
            elif self.__longPos2 == position:
                self.__shortPos1.cancelEntry()
                shares = 1
                printLog(self.__instrument1+'做空之前我的钱'+str(self.getBroker().getCash()))
                self.__shortPos1 = self.enterShort(self.__instrument1, shares, True)
                self.buyprice1 = 0
                self.duicong = 0
                
    def onExitOk(self, position):
        if self.__longPos11 == position:
            self.__longPos11 = None
        elif self.__shortPos11 == position:
            self.__shortPos11 = None
        elif self.__shortPos12 == position:
            self.__shortPos12 = None
        elif self.__longPos12 == position:
            self.__longPos12 = None
        elif self.__shortPos13 == position:
            self.__shortPos13 = None
        elif self.__longPos13 == position:
            self.__longPos13 = None
        elif self.__shortPos21 == position:
            self.__shortPos21 = None
        elif self.__longPos21 == position:
            self.__longPos21 = None
        else:
            assert(False)   
    def getmarketinfo(self):
        return '交易次数:'+str(self.wintime+self.losstime)+'盈利次数:'+str(self.wintime)+'亏损次数:'+str(self.losstime)+'盈利额:'+str(self.winmoney)+'亏损额:'+str(self.lossmoney)
    def getPrice(self):
        return self.__priceDS
    
    def getmacd(self):
        return self.pricechamacdDs
    
    def getchamacd(self):
        return self.pricechahisDs
    
    def getpricecha(self):
        return self.pricechaDS
    
    def getpricechawaveDS(self):
        return self.pricechawaveDS
    
    def getprice1waveDS(self):
        return self.price1waveDS
    
    def getprice2waveDS(self):
        return self.price2waveDS
    
    def getbuyprice1(self):
        return self.bid1DS
    def getsellprice1(self):
        return self.ask1DS
    
    def getbuyprice1_another(self):
        return self.bid1DS_another
    def getsellprice1_another(self):
        return self.ask1DS_another
    
    def getwavetickets(self):
        return self.wavetickets
    def getfirstSMA(self):
        return self.__firstSMA
    def getsecondSMA(self):
        return self.__secondSMA
    def getthirdSMA(self):
        return self.__thirdSMA
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

    def getpricechaDS(self):
        return self.pricechaDS

    def getRSI(self):
        return self.__rsi
    
    def getmoneyearn(self):
        return self.moneyearn
    def getmoneyearntimes(self):
        return self.moneyearntimes
    def getmoneyloss(self):
        return self.moneyloss
    
    

#     def onEnterCanceled(self, position):
#         if self.__longPos == position:
#             self.__longPos = None
#         elif self.__shortPos == position:
#             self.__shortPos = None
#         else:
#             assert(False)

    
# 
#     def onExitCanceled(self, position):
#         # If the exit was canceled, re-submit it.
#         position.exitMarket()
 
    def enterLongSignal(self, bar):#当短周期上穿 长周期，就入场做多，seg也要同方向
        return self.__shortSMA[-1] > self.__longSMA[-1] and self.__shortSMA[-1] - self.__longSMA[-1] < 15 
 
    def exitLongSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 1 and bar.getBid1() != 0
 
    def enterShortSignal(self, bar):#当短周期下穿 长周期，就入场做空，seg也要同方向
        return self.__shortSMA[-1] < self.__longSMA[-1] and self.__longSMA[-1] - self.__shortSMA[-1] < 15 
 
    def exitShortSignal(self,bar):#seg转向就平仓
        return self.allSegPankous[-1].dir != 2 and bar.getAsk1() != 0

def printLog(log):
    logging.getLogger('trade').info(log)

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
    

  
class Real_MarketData:
    def __init__(self):
        self.open_close_mark = 0
        self.price = 0.0
        self.direction = ""
        self.number = 0
        self.clientcode = ""
        self.number_remain = 0
        self.price_condition = ""
        self.valid_period_type = ""
        self.status = ""
        self.report_no = ""
        self.report_status = ""
        self.tradeday = ""
        self.entrust_time = ""
        self.no = ""
        self.report_reference = ""
        self.investor_code = ""
        self.volume_type = ""
        self.instrumentID = ""
#     mylogger.printlog(log)

def process_data(config,filepath,date,instrumentId):
    print 'start '
    str = ''
    lines = []
#     with open(filepath+'trace_'+date+'.log','rt') as handle:
    with codecs.open(filepath+'trace_'+date+'.log','r','gb2312') as handle: 
        for  line in  handle.readlines(): 
#             print  line+'\n'
            if line.find('OnRtnOrder') > 0:
                order = Real_MarketData()
                str = line.encode('utf-8')
                index = str.find('<')
                index2 = str.find('>')
                arrs = str[index+1:index2].split(',')
                for arr in arrs:
#                     print 'arr'+arr
                    if arr.split(':')[0] == '组合开平标志':
                        order.open_close_mark = int(arr.split(':')[1])
                    elif arr.split(':')[0] == '价格':
                        order.price = int(round((float)(arr.split(':')[1])/config.PriceTick))
                    elif arr.split(':')[0] == '买卖方向':
                        order.direction = arr.split(':')[1]
                    elif arr.split(':')[0] == '数量':
                        order.number = arr.split(':')[1]
                    elif arr.split(':')[0] == '客户代码':
#                         print '客户代码'+arr.split(':')[1]
                        order.clientcode = arr.split(':')[1]
                    elif arr.split(':')[0] == '剩余数量':
#                         print '剩余数量'+arr.split(':')[1]
                        order.number_remain = arr.split(':')[1]
                    elif arr.split(':')[0] == '报单价格条件':
                        order.price_condition = arr.split(':')[1]
                    elif arr.split(':')[0] == '有效期类型':
                        order.valid_period_type = arr.split(':')[1]
                    elif arr.split(':')[0] == '状态信息':
                        order.status = arr.split(':')[1]
                    elif arr.split(':')[0] == '报单编号':
                        order.report_no = arr.split(':')[1]
                    elif arr.split(':')[0] == '报单提交状态':
                        order.report_status = arr.split(':')[1]
                    elif arr.split(':')[0] == '交易日':
                        order.tradeday = arr.split(':')[1]
                    elif arr.split(':')[0] == '委托时间':
                        order.entrust_time = arr[13:]
                    elif arr.split(':')[0] == '序号':
                        order.no = arr.split(':')[1]
                    elif arr.split(':')[0] == '报单引用':
                        order.report_reference = arr.split(':')[1]
                    elif arr.split(':')[0] == '投资者代码':
                        order.investor_code = arr.split(':')[1]
                    elif arr.split(':')[0] == '成交量类型':
                        order.volume_type = arr.split(':')[1]
                    elif arr.split(':')[0] == '合约代码':
                        order.instrumentID = arr.split(':')[1]
                if order.instrumentID == instrumentId:
                    lines.append(order)
    return lines    


def main():
    
    
    
    logging.basicConfig(level=logging.DEBUG,
                format='%(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=time.strftime('%Y%m%d%H%M%S')+'duichong.log',
                filemode='w')

    datestr = '20131218'
    instruments = ['p1405','y1405']
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instruments[0], datestr+instruments[0]+".csv")
    feed.addBarsFromCSV(instruments[1], datestr+instruments[1]+".csv")
    
    
    
#     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
     
#     logfile = appconsant.logfile
    # Evaluate the strategy with the feed's bars.
    #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    myStrategy = MyStrategyRSI(feed,instruments[0],instruments[1], 660,200,100)
     
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
    
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("Bid1", myStrategy.getbuyprice1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("Ask1", myStrategy.getsellprice1())
    
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("Bid1_another", myStrategy.getbuyprice1_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("Ask1_another", myStrategy.getsellprice1_another())
    
    plt.getOrCreateSubplot("wave").addDataSeries("wave1", myStrategy.getprice1waveDS())
    plt.getOrCreateSubplot("wave").addDataSeries("wave2", myStrategy.getprice2waveDS())
    
    
    plt.getOrCreateSubplot("macd").addDataSeries("macd", myStrategy.getmacd())
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangeupper", myStrategy.getxrangeupper())
#     plt.getInstrumentSubplot(instrumentID).addDataSeries("xrangelower", myStrategy.getxrangelower())
# #     plt.getOrCreateSubplot("wave").addDataSeries("waveds", myStrategy.getWave())
#     plt.getOrCreateSubplot("chamacd").addDataSeries("chamacd", myStrategy.getchamacd())
#     plt.getOrCreateSubplot("cha").addDataSeries("cha", myStrategy.getpricecha())
#     plt.getOrCreateSubplot("chawave").addDataSeries("chawave", myStrategy.getpricechawaveDS())
#     plt.getOrCreateSubplot("wave").addDataSeries("wave1", myStrategy.getprice1waveDS())
#     plt.getOrCreateSubplot("wave").addDataSeries("wave2", myStrategy.getprice2waveDS())
    
#     plt.getOrCreateSubplot("EMA").addDataSeries("SEMA", myStrategy.getshortEMA())
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
     
    

    
    
    printLog(myStrategy.getmarketinfo())
    
    printLog(myStrategy.getmoneyearn())
    printLog(myStrategy.getmoneyloss())
    
    
#     plt.plotdiffbarbytwo(myStrategy.getmoneyearntimes(), myStrategy.moneyearn)
#     plt.plotdiff(waveseries)
    plt.plot()




# g = 
# print 

if __name__=="__main__": main()
