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
        self.nonewtop1 = 0
        self.topprice1 = 0.0
        
        self.nonewtop2 = 0
        self.topprice2 = 0.0
        
        self.huice_during1 = 0.0
        self.huice_during2 = 0.0
        self.outhuice_during1 = 0
        self.outhuice_during2 = 0

        self.lastmymoney = 0.0
        self.losstime = 0
        self.wintime = 0
        self.winmoney = 0.0
        self.lossmoney = 0.0
        
        
        #指标相关
#         self.__longEMA = ma.EMA(self.__priceDS, longSMA)
#         self.__shortEMA = ma.EMA(self.__priceDS, shortSMA)
        
        

        #交易元素
        self.__longPos1 = None
        self.__shortPos1 = None
        self.__longPos2 = None
        self.__shortPos2 = None
        
        #策略相关元素
        
        self.__nwaveticket=10
        
        self.lastbar1 = None
        self.lastbar2 = None
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
        
        self.n = 10#有n个点没有创新高
        self.a = 3 #亏损了a个点平仓
        self.b = 3 #盈利了b个点，并且过程回撤小于c，目前回撤大于c，平仓
        self.c = 2 
        self.d = 3 #盈利了b个点，并且过程回撤大于c，目前回撤大于d，平仓
        self.f = 4 #在10个ticket中上涨了f个点，然后上涨速率小于p，并且价差的macd小于y，大于x，入场
        self.p = 2
        self.x = 0.00022 #价差的macd小于x，开始向外对冲
        self.y = 0.25 #价差dmacd大于y，开始向内对冲
        self.shortema = 50
        self.longema = 110
        self.signema = 30
        self.pricechamacdDs = macd.MACD(self.pricechaDS,self.shortema,self.longema,self.signema)
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
            
            if len(self.__priceDS1) > 10:
                priceds = self.__priceDS1[-9:]
                upper = max(priceds)
                lower = min(priceds)
                self.speed1 = (upper - lower)
                if self.speed1 > self.p:
                    self.outspeed1 = 1
                
            tp = CTicketWave()
            tp.idx = len(self.__priceDS1)+1
            tick_idx_start = len(self.__priceDS1) - self.__nwaveticket
            if tick_idx_start < 0:
                tick_idx_start = 0
            tp.tick_idx_start = tick_idx_start
            tp.tick_idx_end = len(self.__priceDS1)-1
#             tp.price_start = self.__priceDS[tick_idx_start]
#             tp.price_end = self.__priceDS[-1]
            priceds = self.__priceDS1[tick_idx_start:len(self.__priceDS1)]
            tp.upper = max(priceds)
            tp.lower = min(priceds)
            tp.price_wave = tp.upper - tp.lower
    #         print ' '+str(tp.price_wave)
            self.price1waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
#             if bar.getPrice() > self.pricemax1:
#                 self.pricemax1 = bar.getPrice()
            __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
            barTime = __barTime[0:len(__barTime)-3]
            barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
            printLog(self.__instrument1+barLog)
            
            if (self.__longPos1 != None and self.__longPos1.entryFilled()) or (self.__shortPos1 != None and self.__shortPos1.entryFilled()):
                if self.__longPos1 != None and self.__longPos1.entryFilled():
                    if self.buyprice1 == 0:#获得购买价格
                        self.buyprice1 = self.__longPos1.getEntryOrder().getAvgFillPrice()#getLimitPrice()    #self.__priceDS1[-1]

                    if self.topprice1 == 0:
                        self.topprice1 = self.__priceDS1[-1]
                    if self.topprice1 > self.__priceDS1[-1]:#没有创新高
                        self.nonewtop1 += 1
                        if self.topprice1 - self.__priceDS1[-1] > self.huice_during1:
                            self.huice_during1 = self.topprice1 - self.__priceDS1[-1]
                    else:
                        self.topprice1 = self.__priceDS1[-1]#创新高
                        self.nonewtop1 =  0  
                        
                    if self.nonewtop1 > self.n:
                        printLog(self.__instrument1+'当前已经有'+str(self.nonewtop1)+'个ticket没有创新高，准备平仓')
                        self.__longPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做多平仓')
                        
                    elif self.buyprice1 - self.__priceDS1[-1] > self.a:
                        printLog(self.__instrument1+'当前已经亏损'+str(self.a)+'，准备平仓')
                        self.__longPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做多平仓')
                    elif self.__priceDS1[-1] - self.buyprice1 < self.b and self.huice_during1 > self.c: 
                        self.outhuice_during1 = 1 
                    elif self.__priceDS1[-1] - self.buyprice1 > self.b and self.huice_during1 > self.c and self.outhuice_during1 == 0:
                        printLog(self.__instrument1+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'outhuice_during1'+self.outhuice_during1+'，准备平仓')
                        self.__longPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做多平仓')
                    elif self.__priceDS1[-1] - self.buyprice1 > self.b and self.huice_during1 > self.d and self.outhuice_during1 == 1:
                        printLog(self.__instrument1+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'，准备平仓')
                        self.__longPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做多平仓')
                elif self.__shortPos1 != None and self.__shortPos1.entryFilled():
                    if self.buyprice1 == 0:#获得购买价格
                        self.buyprice1 = self.__shortPos1.getEntryOrder().getAvgFillPrice()#getLimitPrice()    #self.__priceDS1[-1]

                    if self.topprice1 == 0:
                        self.topprice1 = self.__priceDS1[-1]
                    if self.topprice1 < self.__priceDS1[-1]:#没有创新高
                        self.nonewtop1 += 1
                        if self.__priceDS1[-1] - self.topprice1  > self.huice_during1:
                            self.huice_during1 = self.__priceDS1[-1] - self.topprice1 
                    else:
                        self.topprice1 = self.__priceDS1[-1]#创新高
                        self.nonewtop1 =  0  
                        
                    if self.nonewtop1 > self.n:
                        printLog(self.__instrument1+'当前已经有'+str(self.nonewtop1)+'个ticket没有创新低，准备平仓')
                        self.__shortPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做空平仓')
                        
                    elif self.__priceDS1[-1] - self.buyprice1 > self.a:
                        printLog(self.__instrument1+'当前已经亏损'+str(self.a)+'，准备平仓')
                        self.__shortPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做空平仓')
                    elif self.buyprice1 - self.__priceDS1[-1] < self.b and self.huice_during1 > self.c: 
                        self.outhuice_during1 = 1 
                    elif self.buyprice1 - self.__priceDS1[-1]  > self.b and self.huice_during1 > self.c and self.outhuice_during1 == 0:
                        printLog(self.__instrument1+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'outhuice_during1'+str(self.outhuice_during1)+'，准备平仓')
                        self.__shortPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做空平仓')
                    elif self.buyprice1 - self.__priceDS1[-1]  > self.b and self.huice_during1 > self.d and self.outhuice_during1 == 1:
                        printLog(self.__instrument1+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'，准备平仓')
                        self.__shortPos1.exitMarket()
                        self.buyprice1 = 0
                        self.nonewtop1 =  0
                        self.topprice1 = 0.0
                        self.huice_during1 = 0.0
                        self.outhuice_during1 = 0
                        printLog(self.__instrument1+'做空平仓')
            else:
                if self.__longPos1 == None and self.__longPos2 == None and self.__shortPos1 == None and self.__shortPos2 == None:
#                     if len(self.pricechahisDs) > 0 and self.pricechahisDs[-1] < -self.y:
#                         printLog('当前价差的macd为'+str(self.pricechahisDs[-1]))
#                         shares = 1
#                         printLog(self.__instrument1+'做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getOpen()))
#                         self.__longPos1 = self.enterLongLimit(self.__instrument1, self.lastbar1.getOpen(), shares, True)
#                         self.buyprice1 = 0
#                         shares = 1
#                         printLog(self.__instrument2+'做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getClose()))
#                         self.__shortPos2 = self.enterShortLimit(self.__instrument2, self.lastbar2.getClose(), shares, True)
#                         self.buyprice2 = 0
#                         self.duicong = 1#向外对冲
#                     elif  len(self.pricechahisDs) > 0 and self.pricechahisDs[-1] > self.y:
#                         printLog('当前价差的macd为'+str(self.pricechahisDs[-1]))
#                         shares = 1
#                         printLog(self.__instrument2+'做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getOpen()))
#                         self.__longPos2 = self.enterLongLimit(self.__instrument2, self.lastbar2.getOpen(), shares, True)
#                         self.buyprice2 = 0
#                         shares = 1
#                         printLog(self.__instrument1+'做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getClose()))
#                         self.__shortPos1 = self.enterShortLimit(self.__instrument1, self.lastbar1.getClose(), shares, True)
#                         self.buyprice1 = 0
#                         self.duicong = 1#向外对冲
                    if self.speed1 < self.p and self.outspeed1 == 1:
                        if self.__priceDS1[-1] - self.__priceDS1[-9] > 0:
                            shares = 1
                            printLog(self.__instrument1+'速率入场，做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getClose()))
                            self.__shortPos1 = self.enterShortLimit(self.__instrument1, self.lastbar1.getClose(), shares, True)
                            self.buyprice1 = 0
                            shares = 1
                            printLog(self.__instrument2+'速率入场，做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getClose()))
                            self.__shortPos2 = self.enterShortLimit(self.__instrument2, self.lastbar2.getClose(), shares, True)
                            self.buyprice2 = 0
                            self.outspeed1 = 0
                            self.duicong = 0
                        else:
                            shares = 1
                            printLog(self.__instrument1+'速率入场，做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getClose()))
                            self.__longPos1 = self.enterLongLimit(self.__instrument1, self.lastbar1.getOpen(), shares, True)
                            self.buyprice1 = 0
                            shares = 1
                            printLog(self.__instrument2+'速率入场，做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getClose()))
                            self.__longPos2 = self.enterLongLimit(self.__instrument2, self.lastbar2.getOpen(), shares, True)
                            self.buyprice2 = 0
                            self.outspeed1 = 0
                            self.duicong = 0
                    
            
        
        if bars.getBar(self.__instrument2)!=None:#品种二，价格低的
            self.whichticket = 2
            bar = bars.getBar(self.__instrument2)
            self.lastbar2 = bar
            bardateTime = bar.getDateTime()
            
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
            printLog(self.__instrument2+barLog)
            
            
            tp = CTicketWave()
            tp.idx = len(self.__priceDS2)+1
            tick_idx_start = len(self.__priceDS2) - self.__nwaveticket
            if tick_idx_start < 0:
                tick_idx_start = 0
            tp.tick_idx_start = tick_idx_start
            tp.tick_idx_end = len(self.__priceDS2)-1
#             tp.price_start = self.__priceDS[tick_idx_start]
#             tp.price_end = self.__priceDS[-1]
            priceds = self.__priceDS2[tick_idx_start:len(self.__priceDS2)]
            tp.upper = max(priceds)
            tp.lower = min(priceds)
            tp.price_wave = tp.upper - tp.lower
    #         print ' '+str(tp.price_wave)
            self.price2waveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
            
            
            if (self.__longPos2 != None and self.__longPos2.entryFilled()) or (self.__shortPos2 != None and self.__shortPos2.entryFilled()):
                if self.__longPos2 != None and self.__longPos2.entryFilled():
                    if self.buyprice2 == 0:#获得购买价格
                        self.buyprice2 = self.__longPos2.getEntryOrder().getAvgFillPrice()#getLimitPrice()    #self.__priceDS2[-1]

                    if self.topprice2 == 0:
                        self.topprice2 = self.__priceDS2[-1]
                    if self.topprice2 > self.__priceDS2[-1]:#没有创新高
                        self.nonewtop2 += 1
                        if self.topprice2 - self.__priceDS2[-1] > self.huice_during2:
                            self.huice_during2 = self.topprice2 - self.__priceDS2[-1]
                    else:
                        self.topprice2 = self.__priceDS2[-1]#创新高
                        self.nonewtop2 =  0  
                        
                    if self.nonewtop2 > self.n:
                        printLog(self.__instrument2+'当前已经有'+str(self.nonewtop2)+'个ticket没有创新高，准备平仓')
                        self.__longPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做多平仓')
                        
                    elif self.buyprice2 - self.__priceDS2[-1] > self.a:
                        printLog(self.__instrument2+'当前已经亏损'+str(self.a)+'，准备平仓')
                        self.__longPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做多平仓')
                    elif self.__priceDS2[-1] - self.buyprice2 < self.b and self.huice_during2 > self.c: 
                        self.outhuice_during2 = 1 
                    elif self.__priceDS2[-1] - self.buyprice2 > self.b and self.huice_during2 > self.c and self.outhuice_during2 == 0:
                        printLog(self.__instrument2+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'outhuice_during2'+str(self.outhuice_during2)+'，准备平仓')
                        self.__longPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做多平仓')
                    elif self.__priceDS2[-1] - self.buyprice2 > self.b and self.huice_during2 > self.d and self.outhuice_during2 == 1:
                        printLog(self.__instrument2+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'，准备平仓')
                        self.__longPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做多平仓')
                elif self.__shortPos2 != None and self.__shortPos2.entryFilled():
                    if self.buyprice2 == 0:#获得购买价格
                        self.buyprice2 = self.__shortPos2.getEntryOrder().getAvgFillPrice()#getLimitPrice()    #self.__priceDS2[-1]

                    if self.topprice2 == 0:
                        self.topprice2 = self.__priceDS2[-1]
                    if self.topprice2 < self.__priceDS2[-1]:#没有创新高
                        self.nonewtop2 += 1
                        if self.__priceDS2[-1] - self.topprice2  > self.huice_during2:
                            self.huice_during2 = self.__priceDS2[-1] - self.topprice2 
                    else:
                        self.topprice2 = self.__priceDS2[-1]#创新高
                        self.nonewtop2 =  0  
                        
                    if self.nonewtop2 > self.n:
                        printLog(self.__instrument2+'当前已经有'+str(self.nonewtop2)+'个ticket没有创新低，准备平仓')
                        self.__shortPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做空平仓')
                        
                    elif self.__priceDS2[-1] - self.buyprice2 > self.a:
                        printLog(self.__instrument2+'当前已经亏损'+str(self.a)+'，准备平仓')
                        self.__shortPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做空平仓')
                    elif self.buyprice2 - self.__priceDS2[-1] < self.b and self.huice_during2 > self.c: 
                        self.outhuice_during2 = 1 
                    elif self.buyprice2 - self.__priceDS2[-1]  > self.b and self.huice_during2 > self.c and self.outhuice_during2 == 0:
                        printLog(self.__instrument2+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'outhuice_during2'+str(self.outhuice_during2)+'，准备平仓')
                        self.__shortPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做空平仓')
                    elif self.buyprice2 - self.__priceDS2[-1]  > self.b and self.huice_during2 > self.d and self.outhuice_during2 == 1:
                        printLog(self.__instrument2+'当前已经盈利'+str(self.b)+'回撤'+str(self.c)+'，准备平仓')
                        self.__shortPos2.exitMarket()
                        self.buyprice2 = 0
                        self.nonewtop2 =  0
                        self.topprice2 = 0.0
                        self.huice_during2 = 0.0
                        self.outhuice_during2 = 0
                        printLog(self.__instrument2+'做空平仓')
            else:
                if self.__longPos1 == None and self.__longPos2 == None and self.__shortPos1 == None and self.__shortPos2 == None:
                    if self.speed2 < self.p and self.outspeed2 == 1:
                        if self.__priceDS2[-1] - self.__priceDS2[-9] > 0:
                            shares = 1
                            printLog(self.__instrument1+'速率入场，做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getClose()))
                            self.__shortPos1 = self.enterShortLimit(self.__instrument1, self.lastbar1.getClose(), shares, True)
                            self.buyprice1 = 0
                            shares = 1
                            printLog(self.__instrument2+'速率入场，做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getClose()))
                            self.__shortPos2 = self.enterShortLimit(self.__instrument2, self.lastbar2.getClose(), shares, True)
                            self.buyprice2 = 0
                            self.outspeed2 = 0
                            self.duicong = 0
                        else:
                            shares = 1
                            printLog(self.__instrument1+'速率入场，做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getOpen()))
                            self.__longPos1 = self.enterLongLimit(self.__instrument1, self.lastbar1.getOpen(), shares, True)
                            self.buyprice1 = 0
                            shares = 1
                            printLog(self.__instrument2+'速率入场，做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getOpen()))
                            self.__longPos2 = self.enterLongLimit(self.__instrument2, self.lastbar2.getOpen(), shares, True)
                            self.buyprice2 = 0
                            self.outspeed2 = 0
                            self.duicong = 0
        
                
        if len(self.__priceDS1) == 1 and len(self.__priceDS2) == 1:
            shares = 1
            printLog(self.__instrument1+'做多之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar1.getOpen()))
            self.__longPos1 = self.enterLongLimit(self.__instrument1, self.lastbar1.getOpen(), shares, True)
            self.buyprice = 0
            shares = 1
            printLog(self.__instrument2+'做空之前我的钱'+str(self.getBroker().getCash())+'限价单价格：'+str(self.lastbar2.getClose()))
            self.__shortPos2 = self.enterShortLimit(self.__instrument2, self.lastbar2.getClose(), shares, True)
            self.buyprice2 = 0
            self.duicong = 1#向外对冲
         
        if self.lastbar2 != None and self.lastbar1 != None:
            self.pricecha = self.lastbar1.getPrice() - self.lastbar2.getPrice()
            self.pricechaDS.appendWithDateTime(bardateTime, self.pricecha)
            if self.pricecha > self.maxcha:
                self.maxcha = self.pricecha
            elif self.pricecha < self.mincha or self.mincha == 0:
                self.mincha = self.pricecha    
            if  len(self.pricechahisDs) > 0 and self.pricechahisDs[-1] > self.y:
                printLog('当前价差的macd为'+str(self.pricechahisDs[-1]))
                
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
        if self.__longPos1 == position:
            self.__longPos1 = None
        elif self.__shortPos1 == position:
            self.__shortPos1 = None
        elif self.__shortPos2 == position:
            self.__shortPos2 = None
        elif self.__longPos2 == position:
            self.__longPos2 = None
        else:
            assert(False)   
    def getmarketinfo(self):
        return '交易次数:'+str(self.wintime+self.losstime)+'盈利次数:'+str(self.wintime)+'亏损次数:'+str(self.losstime)+'盈利额:'+str(self.winmoney)+'亏损额:'+str(self.lossmoney)
    def getPrice(self):
        return self.__priceDS
    
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

    def getbuyprice1(self):
        return self.bid1DS
    def getsellprice1(self):
        return self.ask1DS
    
    def getbuy1_another(self):
        return self.buy1DS_another
    def getbuy2_another(self):
        return self.buy2DS_another

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

    datestr = '20151201'
    instruments = ['y1601','p1601']
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
