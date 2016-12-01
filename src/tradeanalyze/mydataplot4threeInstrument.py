#!/usr/bin/python
#-*- coding=utf-8 -*-
import os
import conf,data
from tradeanalyze import StoreCsv4Nticket
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

class MyStrategy4threeInstrument(strategy.BacktestingStrategy):
    def __init__(self, feed,instrument, ds2,ds3):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        # We'll use adjusted close values, if available, instead of regular close values.
        if feed.barsHaveAdjClose():
            self.setUseAdjustedValues(True)
        self.__priceDS = feed[instrument].getPriceDataSeries()
        self.data_lines_two = ds2
        self.data_lines_three = ds3
        
        self.instrumentDS_two =  dataseries.SequenceDataSeries(100000)#use to draw map
        self.instrumentDS_three =  dataseries.SequenceDataSeries(100000)#use to draw map
        

    def getPrice(self):
        return self.__priceDS
    
    def getinstrumentDS_two(self):
        return self.instrumentDS_two
    
    def getinstrumentDS_three(self):
        return self.instrumentDS_three


    def onBars(self, bars):
        
        # when dirction is change ,then save the price in segmentds
        bar = bars[self.__instrument]
        
        __barTime = bar.getDateTime().strftime('%Y-%m-%d %H:%M:%S %f')
        barTime = __barTime[0:len(__barTime)-3]
        barLog = 'bar:'+ barTime+' '+str(bar.getLastPrice())+' '+str(bar.getVolume())+' '+str(bar.getAsk1())+' '+str(bar.getAskVol())+' '+str(bar.getBid1())+' '+str(bar.getBidVol())+' '+str(bar.getPrice())
        
        #处理时间不对应的问题
        if len(self.data_lines_two) > 0:
            print self.data_lines_two[0].date_format +'   ' + barTime
            if self.data_lines_two[0].date_format == barTime:
                self.instrumentDS_two.appendWithDateTime(bar.getDateTime(), self.data_lines_two[0].avg_format)
                self.data_lines_two.remove(self.data_lines_two[0])
            elif self.data_lines_two[0].date_format < barTime:
                while  len(self.data_lines_two) > 0 and self.data_lines_two[0].date_format < barTime:
                    print '时间不对应，开始删除'
                    self.data_lines_two.remove(self.data_lines_two[0])
                if len(self.data_lines_two) > 0 and self.data_lines_two[0].date_format == barTime:
                    self.instrumentDS_two.appendWithDateTime(bar.getDateTime(), self.data_lines_two[0].avg_format)
            else:
                self.instrumentDS_two.appendWithDateTime(bar.getDateTime(), None)
            
        if len(self.data_lines_two) > 0:   
            print self.data_lines_three[0].date_format +'   ' + barTime
            if self.data_lines_three[0].date_format == barTime:
                self.instrumentDS_three.appendWithDateTime(bar.getDateTime(), self.data_lines_three[0].avg_format)
                self.data_lines_three.remove(self.data_lines_two[0])
            elif self.data_lines_three[0].date_format < barTime:
                while len(self.data_lines_three) > 0 and self.data_lines_three[0].date_format < barTime:
                    print '时间不对应，开始删除'
                    self.data_lines_three.remove(self.data_lines_three[0])
                if len(self.data_lines_three) > 0 and self.data_lines_three[0].date_format == barTime:
                    self.instrumentDS_three.appendWithDateTime(bar.getDateTime(), self.data_lines_three[0].avg_format)
            else:
                self.instrumentDS_three.appendWithDateTime(bar.getDateTime(), None)
    


def main():
    
    datafilepath = 'D:\pyTest_yh\data\\'#数据文件位置'
    date = '20150728'
    instrumentID = 'i1508'
    instrumentID2 = 'j1508'
    instrumentID3 = 'rb1607'
    #数据转化
    for f in os.listdir(datafilepath):  
        file = os.path.join(datafilepath, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and filename == date:   
            print '原始文件:'+file
            data_lines = data.getDayData(instrumentID,file) #获取数据
            data_config = conf.getInstrumentInfo(instrumentID) 
            csvfile = filename + instrumentID +'.csv'
            data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
            
            data_lines_two = data.getDayData(instrumentID2,file) #获取数据
            data_config_two = conf.getInstrumentInfo(instrumentID2) 
            csvfile = filename + instrumentID2 +'.csv'
            data_lines_two=StoreCsv4Nticket.process(data_lines_two,data_config_two,csvfile,malength=90)
            
            data_lines_three = data.getDayData(instrumentID2,file) #获取数据
            data_config_three = conf.getInstrumentInfo(instrumentID2) 
            csvfile = filename + instrumentID3 +'.csv'
            data_lines_three=StoreCsv4Nticket.process(data_lines_three,data_config_three,csvfile,malength=90)
            
            
            
#     instrumentID = appconsant.instrumentID
    
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
    
#     feed.addBarsFromCSV("rb1510", "20150708rb1510.csv")
     
#     logfile = appconsant.logfile
    # Evaluate the strategy with the feed's bars.
    #(self, feed, instrument, longSMA, shortSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    myStrategy = MyStrategy4threeInstrument(feed,instrumentID, data_lines_two,data_lines_three)
     
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
     
     
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy,plotOrder=True)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
     
    plt.getInstrumentSubplot(instrumentID).addDataSeries("two", myStrategy.getinstrumentDS_two())
    plt.getInstrumentSubplot(instrumentID).addDataSeries("three", myStrategy.getinstrumentDS_three())
     
    # Run the strategy. 
    myStrategy.run()
     
    
    plt.plot()





# g = 
# print 

if __name__=="__main__": main()
