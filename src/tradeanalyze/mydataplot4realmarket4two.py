#!/usr/bin/python
#-*- coding=utf-8 -*-
import os
import conf,data
import logging
import codecs
from  datetime  import  * 
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

class mydataplot4realmarket4two(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, lines,data_lines_another,market_lines_another):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
#         self.__price_index = 0
        self.marketlines = lines
        
        
        self.diffpriceDS = dataseries.SequenceDataSeries(100000)#use to draw map
        
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
        
        self.data_lines_another = data_lines_another
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

        self.__longPos = None
        self.__shortPos = None
    def getdiffpriceDS(self):
        return self.diffpriceDS
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
    
    

    def onBars(self, bars):
        
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
        barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
#         printLog(barLog)
        self.bid1DS.appendWithDateTime(bar.getDateTime(), bar.getBid1())
        self.ask1DS.appendWithDateTime(bar.getDateTime(), bar.getAsk1())
        
        #给第二个bar添置 
#         print self.data_lines_another[0].date_format +'   ' + barTime
        print 'bartime '+str(barTime) 
        if self.data_lines_another[0].date_format == barTime: 
            if self.data_lines_another[0].BidPrice1 != 0:
                self.bid1DS_another.appendWithDateTime(bar.getDateTime(), self.data_lines_another[0].bid1_format)
            if self.data_lines_another[0].AskPrice1 != 0:
                self.ask1DS_another.appendWithDateTime(bar.getDateTime(), self.data_lines_another[0].ask1_format)
            self.diffpriceDS.appendWithDateTime(bar.getDateTime(), self.data_lines_another[0].avg_format - bar.getPrice())
            self.data_lines_another.remove(self.data_lines_another[0])
        elif self.data_lines_another[0].date_format < barTime:
            while self.data_lines_another[0].date_format < barTime:
                print str(self.data_lines_another[0].date_format)+' '+str(barTime) 
                print '时间不对应，开始删除'
                self.data_lines_another.remove(self.data_lines_another[0])
            if self.data_lines_another[0].date_format == barTime:
                if self.data_lines_another[0].BidPrice1 != 0:
                    self.bid1DS_another.appendWithDateTime(bar.getDateTime(), self.data_lines_another[0].bid1_format)
                if self.data_lines_another[0].AskPrice1 != 0:
                    self.ask1DS_another.appendWithDateTime(bar.getDateTime(), self.data_lines_another[0].ask1_format)
                self.diffpriceDS.appendWithDateTime(bar.getDateTime(), self.data_lines_another[0].avg_format - bar.getPrice())
                self.data_lines_another.remove(self.data_lines_another[0])
        else:
            print 'dayu-----'+str(self.data_lines_another[0].date_format)+' '+str(barTime) 
            self.bid1DS_another.appendWithDateTime(bar.getDateTime(), None)
            self.ask1DS_another.appendWithDateTime(bar.getDateTime(), None)
#        
        #看当前时间是否是order最前的一条，如果不是就过，是的话就while一下，把该时间的order根据类型存到相应的serie里面
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

def printLog(log):
    pass
#     logging.getLogger('trade').info(log)


  

#     mylogger.printlog(log)

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
    datafilepath = 'D:\pyTest_yh\data\\'#数据文件位置'
    marketfilepath = 'D:\pyTest_yh\marketdata\\'#数据文件位置'
    date = '20131218'
    instrumentID = 'p1405'
    instrumentID2 = 'y1405'
    
    #数据转化
    for f in os.listdir(datafilepath):  
        file = os.path.join(datafilepath, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and filename == date:   
            print '原始文件:'+file
            data_lines = data.getDayData(instrumentID,file) #获取数据
            data_config = conf.getInstrumentInfo(instrumentID) 
            csvfile = filename + instrumentID +'.csv'
            data_lines=StoreCsv4Nticket.guiyigai(instrumentID,data_lines,data_config,csvfile,malength=90)
            
#             for line in data_lines:
#                 print line.info
            data_lines_another = data.getDayData(instrumentID2,file) #获取数据
                
            
            data_config_another = conf.getInstrumentInfo(instrumentID2) 
            csvfile = filename + instrumentID2 +'.csv'
            data_lines_another=StoreCsv4Nticket.guiyigai_other(instrumentID2,data_lines_another,data_config_another,csvfile,malength=90)
            
            
            market_lines = process_data(data_config,marketfilepath,date,instrumentID)
            
            market_lines_another = process_data(data_config_another,marketfilepath,date,instrumentID2)
            for market_line_another in market_lines_another:
                market_line_another.price = market_line_another.price - appconsant.realmarket_diff
#             market_lines = market_lines.sort(lambda x: x.entrust_time)
            market_lines = sorted(market_lines, key=lambda x : x.entrust_time)
            
            
            market_lines_another = sorted(market_lines_another, key=lambda x : x.entrust_time)
            
            i = 0
#             while True:
#                 data_lines
            
            print str(len(data_lines))+'  '+str(len(data_lines_another))+' '+str(len(market_lines))+' '+str(len(market_lines_another))
#     instrumentID = appconsant.instrumentID
    
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
    
#     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
     
#     logfile = appconsant.logfile
    # Evaluate the strategy with the feed's bars.
    #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    myStrategy = mydataplot4realmarket4two(feed,instrumentID, market_lines,data_lines_another,market_lines_another)
     
    # Attach a returns analyzers to the strategy. 
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy1", myStrategy.getbuy1())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy2", myStrategy.getbuy2())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy3", myStrategy.getbuy3())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy4", myStrategy.getbuy4())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy5", myStrategy.getbuy5())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell1", myStrategy.getsell1())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell2", myStrategy.getsell2())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell3", myStrategy.getsell3())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell4", myStrategy.getsell4())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell5", myStrategy.getsell5())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping1", myStrategy.getbuyping1())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping2", myStrategy.getbuyping2())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping3", myStrategy.getbuyping3())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping4", myStrategy.getbuyping4())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping5", myStrategy.getbuyping5())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping1", myStrategy.getsellping1())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping2", myStrategy.getsellping2())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping3", myStrategy.getsellping3())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping4", myStrategy.getsellping4())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping5", myStrategy.getsellping5())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel1", myStrategy.getcancel1())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel2", myStrategy.getcancel2())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel3", myStrategy.getcancel3())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel4", myStrategy.getcancel4())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel5", myStrategy.getcancel5())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("Bid1", myStrategy.getbuyprice1())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("Ask1", myStrategy.getsellprice1())
    
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy1_another", myStrategy.getbuy1_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy2_another", myStrategy.getbuy2_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy3_another", myStrategy.getbuy3_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy4_another", myStrategy.getbuy4_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buy5_another", myStrategy.getbuy5_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell1_another", myStrategy.getsell1_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell2_another", myStrategy.getsell2_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell3_another", myStrategy.getsell3_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell4_another", myStrategy.getsell4_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sell5_another", myStrategy.getsell5_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping1_another", myStrategy.getbuyping1_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping2_another", myStrategy.getbuyping2_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping3_another", myStrategy.getbuyping3_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping4_another", myStrategy.getbuyping4_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("buyping5_another", myStrategy.getbuyping5_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping1_another", myStrategy.getsellping1_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping2_another", myStrategy.getsellping2_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping3_another", myStrategy.getsellping3_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping4_another", myStrategy.getsellping4_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("sellping5_another", myStrategy.getsellping5_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel1_another", myStrategy.getcancel1_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel2_another", myStrategy.getcancel2_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel3_another", myStrategy.getcancel3_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel4_another", myStrategy.getcancel4_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("cancel5_another", myStrategy.getcancel5_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("Bid1_another", myStrategy.getbuyprice1_another())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("Ask1_another", myStrategy.getsellprice1_another())
    
#     plt.getOrCreateSubplot("diff").addDataSeries("diff", myStrategy.getdiffpriceDS())
     
    # Run the strategy. 
    myStrategy.run()
     
    
    plt.plot()




# g = 
# print 

if __name__=="__main__": main()
