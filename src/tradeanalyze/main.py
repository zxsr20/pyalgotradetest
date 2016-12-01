#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os,zipfile,gzip
import conf,data,re
import itertools
from pyalgotrade.optimizer import local
from pyalgotrade.barfeed import yahoofeed
import mydataplot4WaveSeg
from tradeanalyze import appconsant, StoreCsv4Nticket, mydataplot4RangeSpan
import logging
"""
用于从单个日期文件中读取一个品种的数据进行处理
"""
def main():
    #get data from .zip
    
    rootdir = 'D:\pyTest_yh\data\\'
     
    instrumentID = appconsant.instrumentID
#     instrumentID = "rb1510"
    date = "20150731"
    
    #数据转化
    
    #数据处理
#     feed.addBarsFromCSV("orcl", "20150518.csv")
#     local.run(mydatasplot.MyStrategyRSI, feed, parameters_generator())
    
    
# def parameters_generator(instrumentID):
#     instrument = [instrumentID]
#     entrySMA = range(400, 700,30)
#     exitSMA = range(100, 300,30)
#     rsiPeriod = range(80,100,5)
#     overBoughtThreshold = range(40, 70,3)
#     overSoldThreshold = range(40, 70,3)
#     return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


def test_waveseg():
    instrumentID = appconsant.instrumentID
#     instrumentID = "rb1510"
    date = "20150731"
    feed = yahoofeed.Feed()
    
    feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
    local.run(mydataplot4WaveSeg.MyStrategyRSI, feed, waveseg_parameters_generator(instrumentID))



def test_rangespan():
    
    print sys.path[0]
    if os.path.exists(sys.path[0]+'\log.txt'):
        os.remove(sys.path[0]+'\log.txt')
    if os.path.exists(sys.path[0]+'\other.txt'):
        os.remove(sys.path[0]+'\other.txt')
    if os.path.exists(sys.path[0]+'\result.txt'):
        os.remove(sys.path[0]+'\result.txt')
    
    instrumentID = appconsant.instrumentID
#     instrumentID = "rb1510"
    date = "20150731"
    feed = yahoofeed.Feed()
    
    feed.addBarsFromCSV(instrumentID, date+instrumentID+".csv")
    local.run(mydataplot4RangeSpan.MyStrategyRSI, feed, rangespan_parameters_generator(instrumentID))

def rangespan_parameters_generator(instrumentID):
    instrument = [instrumentID]
    entrySMA = [660]
    exitSMA = [200]
    rsiPeriod = [100]
    overBoughtThreshold = [57]
    overSoldThreshold = [45]
    rangespan_nwaveticket= [57]
    rangespan_ma= [30]
    rangespan_range= [0.7,0.8,0.9,0.93,0.95]#floatrange(0.6,0.9,4)
    rangespan_span= range(10,60,5)    
    rangespan_stoploss= [20]   
    rangespan_y= [10] 
    rangespan_n= range(10,30,10)   
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,rangespan_nwaveticket,rangespan_ma,rangespan_range,rangespan_span,rangespan_stoploss,rangespan_y,rangespan_n)



def parameters_generator(instrumentID):
    instrument = [instrumentID]
    entrySMA = [660]
    exitSMA = [200]
    rsiPeriod = [100]
    overBoughtThreshold = [57]
    overSoldThreshold = [45]
    nwaveticket = range(1,80,20)   
    wave_y = floatrange(0.1,20,5)
    wave_a = floatrange(0.1,20,5)#range(60,100)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,nwaveticket,wave_y,wave_a)


def waveseg_parameters_generator(instrumentID):
    instrument = [instrumentID]
    entrySMA = [660]
    exitSMA = [200]
    rsiPeriod = [100]
    overBoughtThreshold = [57]
    overSoldThreshold = [45]
    nwaveticket = range(1,80,20)   
    wave_y = floatrange(0.6,2.0,3)
    wave_a = floatrange(0.1,0.6,3)#range(60,100)
    rongren = floatrange(0.1,5,3)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold,nwaveticket,wave_y,wave_a,rongren)


def floatrange(start,stop,steps):
    ''' Computes a range of floating value.
        
        Input:
            start (float)  : Start value.
            end   (float)  : End value
            steps (integer): Number of values
        
        Output:
            A list of floats
        
        <a href="https://www.baidu.com/s?wd=Example&tn=44039180_cpr&fenlei=mv6quAkxTZn0IZRqIHckPjm4nH00T1YdP1bzPjKhnWf3mH7Bn16L0ZwV5Hcvrjm3rH6sPfKWUMw85HfYnjn4nH6sgvPsT6K1TL0qnfK1TL0z5HD0IgF_5y9YIZ0lQzqlpA-bmyt8mh7GuZR8mvqVQL7dugPYpyq8Q1DvrH0YPWTLnj61PH6YnjD4nj6" target="_blank" class="baidu-highlight">Example</a>:
            >>> print floatrange(0.25, 1.3, 5)
            [0.25, 0.51249999999999996, 0.77500000000000002, 1.0375000000000001, 1.3]
    '''
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]


def maintest():
    print sys.path[0]
    
    ch = logging.StreamHandler()  
  
    # 定  义handler的输出格式formatter    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    ch.setFormatter(formatter)  
  
    logging.getLogger().addHandler(ch)  
    logging.getLogger().setLevel(logging.DEBUG)
#     log = logging.getLogger()
#     .info('111111111111111')
    #获取每个品种的主力合约
    rootdir = 'D:\pyTest_yh\data\\'
    date = "20151030"
    #先是遍历info，获得每个品种的代码，然后去读取文件中以该品种打头的文件，读取第一条和最后一条记录，计算vol，比较或者前三的保存起来。
    info={'ru':[10,5],'al':[5,5],'zn':[5,5],'cu':[5,10],'wr':[10,1],'rb':[10,1],'au':[100,0.05],
          'ag':[15,1],'pb':[25,5],'fu':[50,1],'bu':[10,2],'hc':[10,2],'c':[10,1],'a':[10,1],
          'm':[10,1],'y':[10,2],'p':[10,2],'l':[5,5],'v':[5,5],'JM':[60,1],'j':[100,1],'i':[100,1],'JD':[5,1],
          'fb':[500,0.05],'bb':[500,0.05],'pp':[5,1],'CF':[5,5],'TA':[5,2],'OI':[10,2],'WH':[20,1],
          'RI':[20,1],'SR':[10,1],'FG':[20,1],'ME':[50,1],'PM':[50,1],'RM':[10,1],'RS':[10,1],
          'TC':[200,0.2],'JR':[20,1],'IF':[300,0.2],'TF':[1000000,0.002]}
      
    for f in os.listdir(rootdir):  
        file = os.path.join(rootdir, f)  
        filename = file.split("\\")[-1].split(".")[0]
          
        if os.path.isfile(file) and filename == date:   
            logging.getLogger().info('原始文件:'+file)
            fz= zipfile.ZipFile(file,"r")
            namelist = fz.namelist() ; #print namelist
            instrument_vols = []
            for name in namelist:
                data_lines = data.getDayData(name,file) #获取数据
                instrumentVol = InstrumentVol()
                instrumentVol.instrument = name 
                instrumentVol.vol = data_lines[len(data_lines)-1].Volume - data_lines[0].Volume
                logging.getLogger().info('instrument:'+instrumentVol.instrument+'vol:'+str(instrumentVol.vol))
                instrument_vols.append(instrumentVol)
            instrument_vols = sorted(instrument_vols, key=lambda line: line.vol)
            mainInstruments = []
            for instruments in info:
                mainInstrument = MainInstrument()
                mainInstrument.pingzhong = instruments
                mainInstruments.append(mainInstrument)
                  
            for instrument_vol in instrument_vols:
                ins=re.findall('\D*',instrument_vol.instrument)[0]
                for maininstrument in mainInstruments:
                    if maininstrument.pingzhong == ins:
#                         if len(maininstrument.instruments) < 3:
                            maininstrument.instruments.append(instrument_vol.instrument)
                              
            for maininstrument in mainInstruments:
                logging.getLogger().info('品种:'+maininstrument.pingzhong+'前三个品种代码:'+str(maininstrument.instruments))
                for instrument in maininstrument.instruments:
                    data_lines = data.getDayData(instrument,file) #获取数据
                    data_config = conf.getInstrumentInfo(instrument) 
                    csvfile = date + instrument +'.csv'
                    data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
#                     data_lines=StoreCsv4Nticket.processbymeaning(data_lines,data_config,csvfile,malength=90)
#                      
#                     feed = yahoofeed.Feed()
#        
#                     feed.addBarsFromCSV(instrument, date+instrument+".csv")
#                     local.run(mydataplot4WaveSeg.MyStrategyRSI, feed, waveseg_parameters_generator(instrument))
    print 'complete'
                
                    
                    
                    
                    
class InstrumentVol():#tick
    def __init__(self):
        self.vol = 0
        self.instrument = '' #持仓量
                
class MainInstrument():#tick
    def __init__(self):
        self.pingzhong = ''
        self.instruments = [] #持仓量
        
    
        
        

if __name__=="__main__": maintest()

