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
from pyalgotrade.technical import ma, macd,rsi
# from pyalgotrade.technical import rsi
# from pyalgotrade.technical import cross
# from pyalgotrade.dataseries import DataSeries
# import tradeanalyze.data_struct
from tradeanalyze.data_struct import *
import time
from pyalgotrade.technical import cross
import codecs
from pyalgotrade.technical.rsi import RSI
logfile = ''

class MyStrategyRSI(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument1,instrument2, longSMA, shortSMA, rsiPeriod,lines,market_lines_another):
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
        self.marketlines = lines
        
        data_config = conf.getInstrumentInfo(instrument1) 
        
        self.bid1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.ask1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy2DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy3DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy4DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy5DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell2DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell3DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell4DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell5DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping2DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping3DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping4DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping5DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping2DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping3DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping4DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping5DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel1DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel2DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel3DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel4DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel5DS =  dataseries.SequenceDataSeries(100000)#use to draw map
        
#         self.data_lines_another = data_lines_another
        self.marketlines_another = market_lines_another
        self.__priceDS_another = dataseries.SequenceDataSeries(100000)#use to draw map
        self.bid1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.ask1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy2DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy3DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy4DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buy5DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell2DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell3DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell4DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sell5DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping2DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping3DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping4DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.buyping5DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping2DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping3DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping4DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.sellping5DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel1DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel2DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel3DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel4DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.cancel5DS_another =  dataseries.SequenceDataSeries(100000)#use to draw map
        
        
        
        self.repeat_space = 0.03
        
        
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
        
        self.__nwaveticket=500
        
        self.lastbar1 = None
        self.lastbar2 = None
        self.pricechaDS =  dataseries.SequenceDataSeries(100000)
        self.pricebiteDS = dataseries.SequenceDataSeries(100000)
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
        
        self.rsiDs = rsi.RSI(self.ask1DS, 200)
        
    def getrsiDs(self):
        return self.rsiDs     
    

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
            printLog(self.__instrument1+barLog)
            
            
                    
            
        
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
            printLog(self.__instrument2+barLog)
            
            
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
            self.pricebiteDS.appendWithDateTime(bardateTime, self.lastbar1.getPrice()/self.lastbar2.getPrice())
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
            i1 = priceds.index(tp.upper)
            i2 = priceds.index(tp.lower)
            if i1 > i2:
                tp.price_wave =  tp.upper - tp.lower
            else:
                tp.price_wave =  -(tp.upper - tp.lower)
    #         print ' '+str(tp.price_wave)
            self.pricechawaveDS.appendWithDateTime(bar.getDateTime(),tp.price_wave)
#             print >> self.logfile,'wavetick:tick_idx_start:'+str(tp.tick_idx_start)+' tick_idx_end:'+str(tp.tick_idx_end)+' price_start:'+str(tp.price_start)+' price_end:'+str(tp.price_end)+' upper:'+str(tp.upper)+' lower:'+str(tp.lower)+' price_wave'+str(tp.price_wave)
        
        i_buy = 0
        i_sell = 0
        i_buyping = 0
        i_sellping = 0
        i_cancel = 0
        if len(self.marketlines) == 0:
            self.buy1DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy2DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy3DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy4DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy5DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping1DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping2DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping3DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping4DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping5DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell1DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell2DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell3DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell4DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell5DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping1DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping2DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping3DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping4DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping5DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel1DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel2DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel3DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel4DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel5DS.appendWithDateTime(bar.getDateTime(), None)
            
            
            return
#         print barTime[11:19]+'  '+self.marketlines[0].entrust_time+' '+str(len(barTime[11:19]))+' '+str(len(self.marketlines[0].entrust_time))
#         if barTime[11:19] == '09:01:50':
#             i = 1
#         print bar.getDateTime()
        if  str(barTime)[11:19] == self.marketlines[0].entrust_time:
            while True:
                if len(self.marketlines) == 0:
                    break
                if  str(barTime)[11:19] == self.marketlines[0].entrust_time:
                    line = self.marketlines[0]
#                     print self.marketlines[0].status +' '+ self.marketlines[0].direction +' '+str(self.marketlines[0].open_close_mark)
                    if self.marketlines[0].status == '已撤单':
                        if i_cancel == 0:
                            self.cancel1DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price)
                        elif i_cancel == 1:
#                             print bar.getDateTime()
#                             newtime =  bar.getDateTime()+ timedelta(microseconds=500000)
#                             print newtime
                            self.cancel2DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price -self.repeat_space)
                        elif i_cancel == 2:
                            self.cancel3DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*2)
                        elif i_cancel == 3:
                            self.cancel4DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*3)
                        elif i_cancel == 4:
                            self.cancel5DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*4)
                        i_cancel += 1
                    elif self.marketlines[0].open_close_mark == 0:
                        if self.marketlines[0].direction == '买' and self.marketlines[0].status == '未成交':
                            if i_buy == 0:
                                self.buy1DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price)
                            elif i_buy == 1:
                                self.buy2DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*1)
                            elif i_buy == 2:
                                self.buy3DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*2)
                            elif i_buy == 3:
                                self.buy4DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*3)
                            elif i_buy == 4:
                                self.buy5DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*4)
                            i_buy += 1
                        elif self.marketlines[0].direction == '卖' and self.marketlines[0].status == '未成交':
                            if i_sell == 0:
                                self.sell1DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price)
                            elif i_sell == 1:
                                self.sell2DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*1)
                            elif i_sell == 2:
                                self.sell3DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*2)
                            elif i_sell == 3:
                                self.sell4DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*3)
                            elif i_sell == 4:
                                self.sell5DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*4)
                            i_sell += 1
                    elif self.marketlines[0].open_close_mark == 1:
                        if self.marketlines[0].direction == '买' and self.marketlines[0].status == '未成交':
                            if i_buyping == 0:
                                self.buyping1DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price)
                            elif i_buyping == 1:
                                self.buyping2DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*1)
                            elif i_buyping == 2:
                                self.buyping3DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*2)
                            elif i_buyping == 3:
                                self.buyping4DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*3)
                            elif i_buyping == 4:
                                self.buyping5DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*4)
                            i_buyping += 1
                        elif self.marketlines[0].direction == '卖' and self.marketlines[0].status == '未成交':
                            if i_sellping == 0:
                                self.sellping1DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price)
                            elif i_sellping == 1:
                                self.sellping2DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*1)
                            elif i_sellping == 2:
                                self.sellping3DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*2)
                            elif i_sellping == 3:
                                self.sellping4DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*3)
                            elif i_sellping == 4:
                                self.sellping5DS.appendWithDateTime(bar.getDateTime(), self.marketlines[0].price-self.repeat_space*4)
                            i_sellping += 1
                    self.marketlines.remove(line)
                else:
                    if  len(self.buy1DS) == 0 or self.buy1DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buy1DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy2DS) == 0 or self.buy2DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buy2DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy3DS) == 0 or self.buy3DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buy3DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy4DS) == 0 or self.buy4DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buy4DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy5DS) == 0 or self.buy5DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buy5DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping1DS) == 0 or self.buyping1DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping1DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping2DS) == 0 or self.buyping2DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping2DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping3DS) == 0 or self.buyping3DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping3DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping4DS) == 0 or self.buyping4DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping4DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping5DS) == 0 or self.buyping5DS.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping5DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell1DS) == 0 or self.sell1DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sell1DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell2DS) == 0 or self.sell2DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sell2DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell3DS) == 0 or self.sell3DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sell3DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell4DS) == 0 or self.sell4DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sell4DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell5DS) == 0 or self.sell5DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sell5DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping1DS) == 0 or self.sellping1DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping1DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping2DS) == 0 or self.sellping2DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping2DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping3DS) == 0 or self.sellping3DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping3DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping4DS) == 0 or self.sellping4DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping4DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping5DS) == 0 or self.sellping5DS.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping5DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel1DS) == 0 or self.cancel1DS.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel1DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel2DS) == 0 or self.cancel2DS.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel2DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel3DS) == 0 or self.cancel3DS.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel3DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel4DS) == 0 or self.cancel4DS.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel4DS.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel5DS) == 0 or self.cancel5DS.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel5DS.appendWithDateTime(bar.getDateTime(), None)
                        
                    
                    break
        else:
            self.buy1DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy2DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy3DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy4DS.appendWithDateTime(bar.getDateTime(), None)
            self.buy5DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping1DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping2DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping3DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping4DS.appendWithDateTime(bar.getDateTime(), None)
            self.buyping5DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell1DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell2DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell3DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell4DS.appendWithDateTime(bar.getDateTime(), None)
            self.sell5DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping1DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping2DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping3DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping4DS.appendWithDateTime(bar.getDateTime(), None)
            self.sellping5DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel1DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel2DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel3DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel4DS.appendWithDateTime(bar.getDateTime(), None)
            self.cancel5DS.appendWithDateTime(bar.getDateTime(), None)
            
            
            
        i_buy = 0
        i_sell = 0
        i_buyping = 0
        i_sellping = 0
        i_cancel = 0
        if len(self.marketlines_another) == 0:
            self.buy1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel5DS_another.appendWithDateTime(bar.getDateTime(), None)
            
            
            return
#         print barTime[11:19]+'  '+self.marketlines[0].entrust_time+' '+str(len(barTime[11:19]))+' '+str(len(self.marketlines[0].entrust_time))
#         if barTime[11:19] == '09:01:50':
#             i = 1
#         print bar.getDateTime()
        if  str(barTime)[11:19] == self.marketlines_another[0].entrust_time:
            while True:
                if len(self.marketlines_another) == 0:
                    break
                if  str(barTime)[11:19] == self.marketlines_another[0].entrust_time:
                    line = self.marketlines_another[0]
#                     print self.marketlines_another[0].status +' '+ self.marketlines_another[0].direction +' '+str(self.marketlines_another[0].open_close_mark)
                    if self.marketlines_another[0].status == '已撤单':
                        if i_cancel == 0:
                            self.cancel1DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price)
                        elif i_cancel == 1:
#                             print bar.getDateTime()
#                             newtime =  bar.getDateTime()+ timedelta(microseconds=500000)
#                             print newtime
                            self.cancel2DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price -self.repeat_space)
                        elif i_cancel == 2:
                            self.cancel3DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*2)
                        elif i_cancel == 3:
                            self.cancel4DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*3)
                        elif i_cancel == 4:
                            self.cancel5DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*4)
                        i_cancel += 1
                    elif self.marketlines_another[0].open_close_mark == 0:
                        if self.marketlines_another[0].direction == '买' and self.marketlines_another[0].status == '未成交':
                            if i_buy == 0:
                                self.buy1DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price)
                            elif i_buy == 1:
                                self.buy2DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*1)
                            elif i_buy == 2:
                                self.buy3DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*2)
                            elif i_buy == 3:
                                self.buy4DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*3)
                            elif i_buy == 4:
                                self.buy5DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*4)
                            i_buy += 1
                        elif self.marketlines_another[0].direction == '卖' and self.marketlines_another[0].status == '未成交':
                            if i_sell == 0:
                                self.sell1DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price)
                            elif i_sell == 1:
                                self.sell2DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*1)
                            elif i_sell == 2:
                                self.sell3DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*2)
                            elif i_sell == 3:
                                self.sell4DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*3)
                            elif i_sell == 4:
                                self.sell5DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*4)
                            i_sell += 1
                    elif self.marketlines_another[0].open_close_mark == 1:
                        if self.marketlines_another[0].direction == '买' and self.marketlines_another[0].status == '未成交':
                            if i_buyping == 0:
                                self.buyping1DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price)
                            elif i_buyping == 1:
                                self.buyping2DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*1)
                            elif i_buyping == 2:
                                self.buyping3DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*2)
                            elif i_buyping == 3:
                                self.buyping4DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*3)
                            elif i_buyping == 4:
                                self.buyping5DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*4)
                            i_buyping += 1
                        elif self.marketlines_another[0].direction == '卖' and self.marketlines_another[0].status == '未成交':
                            if i_sellping == 0:
                                self.sellping1DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price)
                            elif i_sellping == 1:
                                self.sellping2DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*1)
                            elif i_sellping == 2:
                                self.sellping3DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*2)
                            elif i_sellping == 3:
                                self.sellping4DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*3)
                            elif i_sellping == 4:
                                self.sellping5DS_another.appendWithDateTime(bar.getDateTime(), self.marketlines_another[0].price-self.repeat_space*4)
                            i_sellping += 1
                    self.marketlines_another.remove(line)
                else:
                    if  len(self.buy1DS_another) == 0 or self.buy1DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buy1DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy2DS_another) == 0 or self.buy2DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buy2DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy3DS_another) == 0 or self.buy3DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buy3DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy4DS_another) == 0 or self.buy4DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buy4DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buy5DS_another) == 0 or self.buy5DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buy5DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping1DS_another) == 0 or self.buyping1DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping1DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping2DS_another) == 0 or self.buyping2DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping2DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping3DS_another) == 0 or self.buyping3DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping3DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping4DS_another) == 0 or self.buyping4DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping4DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.buyping5DS_another) == 0 or self.buyping5DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.buyping5DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell1DS_another) == 0 or self.sell1DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sell1DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell2DS_another) == 0 or self.sell2DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sell2DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell3DS_another) == 0 or self.sell3DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sell3DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell4DS_another) == 0 or self.sell4DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sell4DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sell5DS_another) == 0 or self.sell5DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sell5DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping1DS_another) == 0 or self.sellping1DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping1DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping2DS_another) == 0 or self.sellping2DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping2DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping3DS_another) == 0 or self.sellping3DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping3DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping4DS_another) == 0 or self.sellping4DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping4DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.sellping5DS_another) == 0 or self.sellping5DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.sellping5DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel1DS_another) == 0 or self.cancel1DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel1DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel2DS_another) == 0 or self.cancel2DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel2DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel3DS_another) == 0 or self.cancel3DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel3DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel4DS_another) == 0 or self.cancel4DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel4DS_another.appendWithDateTime(bar.getDateTime(), None)
                    if len(self.cancel5DS_another) == 0 or self.cancel5DS_another.getDateTimes()[-1] != bar.getDateTime():
                        self.cancel5DS_another.appendWithDateTime(bar.getDateTime(), None)
                        
                    
                    break
        else:
            self.buy1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buy5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.buyping5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sell5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.sellping5DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel2DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel3DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel4DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.cancel5DS_another.appendWithDateTime(bar.getDateTime(), None)

            

    
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
    
    def getpricebitecha(self):
        return self.pricebiteDS
    
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
    
    
    def getbuy1(self):
        return self.buy1DS
    def getbuy2(self):
        return self.buy2DS
    def getbuy3(self):
        return self.buy3DS
    def getbuy4(self):
        return self.buy4DS
    def getbuy5(self):
        return self.buy5DS
    def getsell1(self):
        return self.sell1DS
    def getsell2(self):
        return self.sell2DS
    def getsell3(self):
        return self.sell3DS
    def getsell4(self):
        return self.sell4DS
    def getsell5(self):
        return self.sell5DS
    def getbuyping1(self):
        return self.buyping1DS
    def getbuyping2(self):
        return self.buyping2DS
    def getbuyping3(self):
        return self.buyping3DS
    def getbuyping4(self):
        return self.buyping4DS
    def getbuyping5(self):
        return self.buyping5DS
    def getsellping1(self):
        return self.sellping1DS
    def getsellping2(self):
        return self.sellping2DS
    def getsellping3(self):
        return self.sellping3DS
    def getsellping4(self):
        return self.sellping4DS
    def getsellping5(self):
        return self.sellping5DS
    def getcancel1(self):
        return self.cancel1DS
    def getcancel2(self):
        return self.cancel2DS
    def getcancel3(self):
        return self.cancel3DS
    def getcancel4(self):
        return self.cancel4DS
    def getcancel5(self):
        return self.cancel5DS
    def getPrice(self):
        return self.__priceDS
    def getbuyprice1(self):
        return self.bid1DS
    def getsellprice1(self):
        return self.ask1DS
    
    def getbuy1_another(self):
        return self.buy1DS_another
    def getbuy2_another(self):
        return self.buy2DS_another
    def getbuy3_another(self):
        return self.buy3DS_another
    def getbuy4_another(self):
        return self.buy4DS_another
    def getbuy5_another(self):
        return self.buy5DS_another
    def getsell1_another(self):
        return self.sell1DS_another
    def getsell2_another(self):
        return self.sell2DS_another
    def getsell3_another(self):
        return self.sell3DS_another
    def getsell4_another(self):
        return self.sell4DS_another
    def getsell5_another(self):
        return self.sell5DS_another
    def getbuyping1_another(self):
        return self.buyping1DS_another
    def getbuyping2_another(self):
        return self.buyping2DS_another
    def getbuyping3_another(self):
        return self.buyping3DS_another
    def getbuyping4_another(self):
        return self.buyping4DS_another
    def getbuyping5_another(self):
        return self.buyping5DS_another
    def getsellping1_another(self):
        return self.sellping1DS_another
    def getsellping2_another(self):
        return self.sellping2DS_another
    def getsellping3_another(self):
        return self.sellping3DS_another
    def getsellping4_another(self):
        return self.sellping4DS_another
    def getsellping5_another(self):
        return self.sellping5DS_another
    def getcancel1_another(self):
        return self.cancel1DS_another
    def getcancel2_another(self):
        return self.cancel2DS_another
    def getcancel3_another(self):
        return self.cancel3DS_another
    def getcancel4_another(self):
        return self.cancel4DS_another
    def getcancel5_another(self):
        return self.cancel5DS_another
    def getPrice_another(self):
        return self.__priceDS_another
    def getbuyprice1_another(self):
        return self.bid1DS_another
    def getsellprice1_another(self):
        return self.ask1DS_another
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


    datafilepath = 'D:\pyTest_yh\data\\'
    marketfilepath = 'D:\pyTest_yh\marketdata\\'#数据文件位置'
    datestr = '20131218'
    instruments = ['y1405','p1405']
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instruments[0], datestr+instruments[0]+".csv")
    feed.addBarsFromCSV(instruments[1], datestr+instruments[1]+".csv")
    
    #数据转化
    for f in os.listdir(datafilepath):  
        file = os.path.join(datafilepath, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and filename == datestr:   
            print '原始文件:'+file
#             data_lines = data.getDayData(instrumentID,file) #获取数据
            data_config = conf.getInstrumentInfo(instruments[0]) 
#             csvfile = filename + instrumentID +'.csv'
#             data_lines=StoreCsv4Nticket.guiyigai(instrumentID,data_lines,data_config,csvfile,malength=90)
            
#             for line in data_lines:
#                 print line.info
#             data_lines_another = data.getDayData(instrumentID2,file) #获取数据
                
            
            data_config_another = conf.getInstrumentInfo(instruments[1]) 
#             csvfile = filename + instrumentID2 +'.csv'
#             data_lines_another=StoreCsv4Nticket.guiyigai_other(instrumentID2,data_lines_another,data_config_another,csvfile,malength=90)
            
            
            market_lines = process_data(data_config,marketfilepath,datestr,instruments[0])
            
            market_lines_another = process_data(data_config_another,marketfilepath,datestr,instruments[1])
            for market_line in market_lines:
                market_line.price = market_line.price - appconsant.realmarket_diff
#             market_lines = market_lines.sort(lambda x: x.entrust_time)
            market_lines = sorted(market_lines, key=lambda x : x.entrust_time)
            
            
            market_lines_another = sorted(market_lines_another, key=lambda x : x.entrust_time)
            
            i = 0
#             while True:
#                 data_lines
            
#             print str(len(data_lines))+'  '+str(len(data_lines_another))+' '+str(len(market_lines))+' '+str(len(market_lines_another))
#     instrumentID = appconsant.instrumentID
    
    
#     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
     
#     logfile = appconsant.logfile
    # Evaluate the strategy with the feed's bars.
    #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    myStrategy = MyStrategyRSI(feed,instruments[0],instruments[1], 660,200,100,market_lines,market_lines_another)
     
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
#     plt.getOrCreateSubplot("bitecha").addDataSeries("bitecha", myStrategy.getpricebitecha())
#     
#     plt.getOrCreateSubplot("chawave").addDataSeries("chawave", myStrategy.getpricechawaveDS())
    plt.getOrCreateSubplot("wave").addDataSeries("wave1", myStrategy.getprice1waveDS())
    plt.getOrCreateSubplot("wave").addDataSeries("wave2", myStrategy.getprice2waveDS())
#     plt.getOrCreateSubplot("rsi").addDataSeries("rsi", myStrategy.getrsiDs())
    
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buy1", myStrategy.getbuy1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buy2", myStrategy.getbuy2())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buy3", myStrategy.getbuy3())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buy4", myStrategy.getbuy4())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buy5", myStrategy.getbuy5())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sell1", myStrategy.getsell1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sell2", myStrategy.getsell2())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sell3", myStrategy.getsell3())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sell4", myStrategy.getsell4())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sell5", myStrategy.getsell5())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buyping1", myStrategy.getbuyping1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buyping2", myStrategy.getbuyping2())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buyping3", myStrategy.getbuyping3())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buyping4", myStrategy.getbuyping4())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("buyping5", myStrategy.getbuyping5())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sellping1", myStrategy.getsellping1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sellping2", myStrategy.getsellping2())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sellping3", myStrategy.getsellping3())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sellping4", myStrategy.getsellping4())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("sellping5", myStrategy.getsellping5())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("cancel1", myStrategy.getcancel1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("cancel2", myStrategy.getcancel2())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("cancel3", myStrategy.getcancel3())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("cancel4", myStrategy.getcancel4())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("cancel5", myStrategy.getcancel5())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("Bid1", myStrategy.getbuyprice1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("Ask1", myStrategy.getsellprice1())
    
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buy1_another", myStrategy.getbuy1_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buy2_another", myStrategy.getbuy2_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buy3_another", myStrategy.getbuy3_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buy4_another", myStrategy.getbuy4_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buy5_another", myStrategy.getbuy5_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sell1_another", myStrategy.getsell1_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sell2_another", myStrategy.getsell2_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sell3_another", myStrategy.getsell3_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sell4_another", myStrategy.getsell4_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sell5_another", myStrategy.getsell5_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buyping1_another", myStrategy.getbuyping1_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buyping2_another", myStrategy.getbuyping2_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buyping3_another", myStrategy.getbuyping3_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buyping4_another", myStrategy.getbuyping4_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("buyping5_another", myStrategy.getbuyping5_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sellping1_another", myStrategy.getsellping1_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sellping2_another", myStrategy.getsellping2_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sellping3_another", myStrategy.getsellping3_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sellping4_another", myStrategy.getsellping4_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("sellping5_another", myStrategy.getsellping5_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("cancel1_another", myStrategy.getcancel1_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("cancel2_another", myStrategy.getcancel2_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("cancel3_another", myStrategy.getcancel3_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("cancel4_another", myStrategy.getcancel4_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("cancel5_another", myStrategy.getcancel5_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("Bid1_another", myStrategy.getbuyprice1_another())
    plt.getInstrumentSubplot(instruments[1]).addDataSeries("Ask1_another", myStrategy.getsellprice1_another())
    
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
