#!/usr/bin/python
#-*- coding=utf-8 -*-
import conf
"This is the main demo file"

class CExData():#tick
    def __init__(self):
        self.vol = 0
        self.DiffOpenInterest = 0 #持仓量
        self.idx = 0 #下标0开始
        self.OneTurnover = 0.0 #成交额
        self.avg_pri = 0.0 #均价一笔
        #self.last_price = 0
        #self.vol = 0
        self.avg_price= 0.0



class COneTick():
    def __init__(self,malength=60):
        self.dmd = None   #data.py
        self.exData = None #计算
        self.malength=malength

    def dump(self):
        return " ".join([str(self.dmd.InstrumentID),str(self.dmd.UpdateTime),str(self.dmd.UpdateMillisec),str(self.dmd.LastPrice),str(self.exData.vol),str(self.dmd.AskPrice1),str(self.dmd.AskVolume1),str(self.dmd.BidPrice1),str(self.dmd.BidVolume1),str(self.exData.avg_pri)])
        #return "%s " %()

    def OneTickInfo(self):
        return [str(self.dmd.InstrumentID),str(self.dmd.UpdateTime),str(self.dmd.UpdateMillisec),str(self.dmd.LastPrice),str(self.exData.vol),str(self.dmd.AskPrice1),str(self.dmd.AskVolume1),str(self.dmd.BidPrice1),str(self.dmd.BidVolume1),str(self.exData.avg_pri)]

    def OneTickDic(self): #返回字典组成列表
        return {'InstrumentID':str(self.dmd.InstrumentID),'UpdateTime':str(self.dmd.UpdateTime),'UpdateMillisec':str(self.dmd.UpdateMillisec),'LastPrice':self.dmd.LastPrice,'vol':self.exData.vol,'AskPrice1':self.dmd.AskPrice1,'AskVolume1':self.dmd.AskVolume1,'BidPrice1':self.dmd.BidPrice1,'BidVolume1':self.dmd.BidVolume1,'avg_pri':self.exData.avg_pri,'avg_price':self.exData.avg_price}

    def OneTickDic_normalizations(self):
        info=conf.getInstrumentInfo(self.dmd.InstrumentID)
        InstrumentID = info[0] #代码
        PriceTick = info[1]  # 最小变动价
        VolumeMultiple = info[2] #合约乘数
        return {'InstrumentID':str(self.dmd.InstrumentID),'UpdateTime':str(self.dmd.UpdateTime),'UpdateMillisec':str(self.dmd.UpdateMillisec),'LastPrice':self.dmd.LastPrice/PriceTick,'vol':self.exData.vol,'AskPrice1':self.dmd.AskPrice1/PriceTick,'AskVolume1':self.dmd.AskVolume1,'BidPrice1':self.dmd.BidPrice1/PriceTick,'BidVolume1':self.dmd.BidVolume1,'avg_pri':self.exData.avg_pri/PriceTick,'avg_price':self.exData.avg_price/PriceTick}

#####################################################

class CSegPankou(): #盘口分析
    def __init__(self):
        self.idx = 0;
        self.tick_idx_start = 0
        self.tick_idx_end = 0
        self.dir = 0  #direction
        self.price_start = 0.0
        self.price_end = 0.0
        self.diffpri = 0.0
        self.lower = 0
        self.upper = 0
        self.tongji = 0
        
class CTicketWave(): #盘口分析
    def __init__(self):
        self.idx = 0;
        self.tick_idx_start = 0
        self.tick_idx_end = 0
        self.dir = 0  #direction
        self.price_start = 0.0
        self.price_end = 0.0
        self.lower = 0
        self.upper = 0
        self.price_wave = 0.0
        
class CHLTicket(): #极值 
    def __init__(self):
        self.idx = 0;
        self.hl = 0  #direction
        self.price = 0.0
        self.id = 0.0
        self.time = ''

#####################################################

class CAllData():
    def __init__(self):
        self.conf = None
        self.allTicks = None
        self.allSegPankous = None
        
        
#就是获得一些对象，从data.py中获得，然后也有从conf中获得信息进行拼接对象的

 
