#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys,os,time,datetime,struct,zipfile,gzip
import csv
from compiler.pycodegen import EXCEPT

class OrderField:
    def __init__(self):
        #交易日
        self.TradingDay = "";#char9
        #结算组代码
        self.SettlementGroupID = "";#char9
        #结算编号
        self.SettlementID = 0;#int
        #报单编号
        self.OrderSysID = "";#char13
        #会员代码
        self.ParticipantID = "";#char11
        #客户代码
        self.ClientID = "";#char11
        #交易用户代码
        self.UserID = "";#char16
        #合约代码
        self.InstrumentID = "";#char31
        #报单价格条件
        self.OrderPriceType = "";#char
        #买卖方向
        self.Direction = "";#char
        #组合开平标志
        self.CombOffsetFlag = "";#char5
        #组合投机套保标志
        self.CombHedgeFlag = "";#char5
        #价格
        self.LimitPrice = 0.0;#double
        #数量
        self.VolumeTotalOriginal = 0;#int
        #有效期类型
        self.TimeCondition = "";#char
        #GTD日期
        self.GTDDate = "";#char9
        #成交量类型
        self.VolumeCondition = "";#char
        #最小成交量
        self.MinVolume = 0;#int
        #触发条件
        self.ContingentCondition = "";#char
        #止损价
        self.StopPrice = 0.0;#double
        #平原因
        self.ForceCloseReason = "";#char
        #本地报单编号
        self.OrderLocalID = "";#char13
        #自动挂起标志
        self.IsAutoSuspend = 0;#int
        #报单来源
        self.OrderSource = "";#char
        #报单状态
        self.OrderStatus = "";#char
        #报单类型
        self.OrderType = "";#char
        #今成交数量
        self.VolumeTraded = 0;#int
        #剩余数量
        self.VolumeTotal = 0;#int
        #报单日期
        self.InsertDate = "";#char9
        #插入时间
        self.InsertTime = "";#char9
        #激活时间9s9si13s11s11s16s31s1s5s5sdi1s9s1si1sd1s13si1s1s1sii9s9s9s9s9s9s16sii11s21s
        self.ActiveTime = "";#char9
        #挂起时间
        self.SuspendTime = "";#char9
        #最后修改时间
        self.UpdateTime = "";#char9
        #撤销时间
        self.CancelTime = "";#char9
        #最后修改交易用户代码
        self.ActiveUserID = "";#char16
        #优先权
        self.Priority = 0;#int
        #按时间排队的序号
        self.TimeSortID = 0;#int
        #结算会员编号
        self.ClearingPartID = "";#char11
        #业务单元
        self.BusinessUnit = "";#char21
        
        self.timestamp = 0;#long
'''
///深度市场行情
struct CFfexFtdcDepthMarketDataField
{
    ///交易日
    TFfexFtdcDateType    TradingDay;typedef char TFfexFtdcDateType[9];
    ///结算组代码
    TFfexFtdcSettlementGroupIDType    SettlementGroupID;typedef char TFfexFtdcSettlementGroupIDType[9];
    ///结算编号
    TFfexFtdcSettlementIDType    SettlementID;typedef int TFfexFtdcSettlementIDType;
    ///最新价
    TFfexFtdcPriceType    LastPrice;typedef double TFfexFtdcPriceType;
    ///昨结算
    TFfexFtdcPriceType    PreSettlementPrice;typedef double TFfexFtdcPriceType;
    ///昨收盘
    TFfexFtdcPriceType    PreClosePrice;typedef double TFfexFtdcPriceType;
    ///昨持仓量
    TFfexFtdcLargeVolumeType    PreOpenInterest;typedef double TFfexFtdcLargeVolumeType;
    ///今开盘
    TFfexFtdcPriceType    OpenPrice;typedef double TFfexFtdcPriceType;
    ///最高价
    TFfexFtdcPriceType    HighestPrice;typedef double TFfexFtdcPriceType;
    ///最低价
    TFfexFtdcPriceType    LowestPrice;typedef double TFfexFtdcPriceType;
    ///数量
    TFfexFtdcVolumeType    Volume;typedef int TFfexFtdcVolumeType;
    ///成交金额
    TFfexFtdcMoneyType    Turnover;typedef double TFfexFtdcMoneyType;
    ///持仓量
    TFfexFtdcLargeVolumeType    OpenInterest;typedef double TFfexFtdcLargeVolumeType;
    ///今收盘
    TFfexFtdcPriceType    ClosePrice;typedef double TFfexFtdcPriceType;
    ///今结算
    TFfexFtdcPriceType    SettlementPrice;typedef double TFfexFtdcPriceType;
    ///涨停板价
    TFfexFtdcPriceType    UpperLimitPrice;typedef double TFfexFtdcPriceType;
    ///跌停板价
    TFfexFtdcPriceType    LowerLimitPrice;typedef double TFfexFtdcPriceType;
    ///昨虚实度
    TFfexFtdcRatioType    PreDelta;typedef double TFfexFtdcRatioType;
    ///今虚实度
    TFfexFtdcRatioType    CurrDelta;typedef double TFfexFtdcRatioType;
    ///最后修改时间
    TFfexFtdcTimeType    UpdateTime;typedef char TFfexFtdcTimeType[9];
    ///最后修改毫秒
    TFfexFtdcMillisecType    UpdateMillisec;typedef int TFfexFtdcMillisecType;
    ///合约代码9s9sidddddddidddddddd9si31sdidididididididididi
    TFfexFtdcInstrumentIDType    InstrumentID;typedef char TFfexFtdcInstrumentIDType[31];
    ///申买价一
    TFfexFtdcPriceType    BidPrice1;typedef double TFfexFtdcPriceType;
    ///申买量一
    TFfexFtdcVolumeType    BidVolume1;typedef int TFfexFtdcVolumeType;
    ///申卖价一
    TFfexFtdcPriceType    AskPrice1;typedef double TFfexFtdcPriceType;
    ///申卖量一
    TFfexFtdcVolumeType    AskVolume1;typedef int TFfexFtdcVolumeType;
    ///申买价二
    TFfexFtdcPriceType    BidPrice2;typedef double TFfexFtdcPriceType;
    ///申买量二
    TFfexFtdcVolumeType    BidVolume2;typedef int TFfexFtdcVolumeType;
    ///申卖价二
    TFfexFtdcPriceType    AskPrice2;typedef double TFfexFtdcPriceType;
    ///申卖量二
    TFfexFtdcVolumeType    AskVolume2;typedef int TFfexFtdcVolumeType;
    ///申买价三
    TFfexFtdcPriceType    BidPrice3;typedef double TFfexFtdcPriceType;
    ///申买量三
    TFfexFtdcVolumeType    BidVolume3;typedef int TFfexFtdcVolumeType;
    ///申卖价三
    TFfexFtdcPriceType    AskPrice3;typedef double TFfexFtdcPriceType;
    ///申卖量三
    TFfexFtdcVolumeType    AskVolume3;typedef int TFfexFtdcVolumeType;
    ///申买价四
    TFfexFtdcPriceType    BidPrice4;typedef double TFfexFtdcPriceType;
    ///申买量四
    TFfexFtdcVolumeType    BidVolume4;typedef int TFfexFtdcVolumeType;
    ///申卖价四
    TFfexFtdcPriceType    AskPrice4;typedef double TFfexFtdcPriceType;
    ///申卖量四
    TFfexFtdcVolumeType    AskVolume4;typedef int TFfexFtdcVolumeType;
    ///申买价五
    TFfexFtdcPriceType    BidPrice5;typedef double TFfexFtdcPriceType;
    ///申买量五
    TFfexFtdcVolumeType    BidVolume5;typedef int TFfexFtdcVolumeType;
    ///申卖价五
    TFfexFtdcPriceType    AskPrice5;typedef double TFfexFtdcPriceType;
    ///申卖量五
    TFfexFtdcVolumeType    AskVolume5;typedef int TFfexFtdcVolumeType;
};

};
'''   

def getDayData(InstrumentID,path): #此处yh修改
    #fz = zipfile.ZipFile("./"+path+"/"+Data+".zip","r")
    fz= zipfile.ZipFile(path,"r")
#     namelist = fz.namelist() ; #print namelist
    
    lines = fz.read('orderdata')
    
    preOI = 0
    size = 312
    nCnt = (len(lines)-preOI) / size

#     nn = lines[0:preOI] #取出该位置的数据
#     u = struct.unpack('q',nn)
#     print str(u)+' '+str(len(lines))

    l_data = []
    
    for i in range(0,nCnt):
        dmd = OrderField()
        t_t = lines[preOI+i*size:preOI+(i+1)*size] #取出该位置的数据

        dmd.timestamp,dmd.TradingDay,dmd.SettlementGroupID,dmd.SettlementID,dmd.OrderSysID,dmd.ParticipantID,dmd.ClientID,dmd.UserID,dmd.InstrumentID,dmd.OrderPriceType,dmd.Direction,dmd.CombOffsetFlag,dmd.CombHedgeFlag,dmd.LimitPrice,dmd.VolumeTotalOriginal,dmd.TimeCondition,dmd.GTDDate,dmd.VolumeCondition,dmd.MinVolume,dmd.ContingentCondition,dmd.StopPrice,dmd.ForceCloseReason,dmd.OrderLocalID,dmd.IsAutoSuspend,dmd.OrderSource,dmd.OrderStatus,dmd.OrderType,dmd.VolumeTraded,dmd.VolumeTotal,dmd.InsertDate,dmd.InsertTime,dmd.ActiveTime,dmd.SuspendTime,dmd.UpdateTime,dmd.CancelTime,dmd.ActiveUserID,dmd.Priority,dmd.TimeSortID,dmd.ClearingPartID,dmd.BusinessUnit = struct.unpack('q9s9si13s11s11s16s31scc5s5sdic9scicdc13sicccii9s9s9s9s9s9s16sii11s21s',t_t)
        dmd.TradingDay = dmd.TradingDay[0:8]

#         print str(dmd.timestamp)+' '+dmd.TradingDay
        if dmd.InstrumentID[0:6] == InstrumentID:
            l_data += [dmd] #把该dmd数据放进数组去   
    return l_data #返回一天的数据，以dmd数组的格式



if __name__=="__main__":
    '''
    strdata = sys.argv[1] #yhModify
    strInsLeft = sys.argv[2]
    '''
#     print struct.calcsize("<9s9si13s11s11s16s31scc5s5sdic9scicdc13sicccii9s9s9s9s9s9s16sii11s21s")
#     print struct.calcsize(">9s9si13s11s11s16s31scc5s5sdic9scicdc13sicccii9s9s9s9s9s9s16sii11s21s")
#     print struct.calcsize("@9s9si13s11s11s16s31scc5s5sdic9scicdc13sicccii9s9s9s9s9s9s16sii11s21s")
#     print struct.calcsize("!9s9si13s11s11s16s31scc5s5sdic9scicdc13sicccii9s9s9s9s9s9s16sii11s21s")
#     print struct.calcsize("=9s9si13s11s11s16s31scc5s5sdic9scicdc13sicccii9s9s9s9s9s9s16sii11s21s")
    
    rootdir = 'D:\\pyTest_yh\\basicdata\\orderdata.zip'
    
    l = getDayData('IF1507',rootdir)   
    print len(l)
   
    writer = csv.writer(file('your10.csv', 'wb'))
     
    writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close'])
    
    preOI=''
    
    for i in l : 
        
        writer.writerow([str(i.TradingDay)+' '+str(i.UpdateTime)[0:8],str(i.LimitPrice),str(i.LimitPrice),str(i.LimitPrice),str(i.LimitPrice),str(i.VolumeTotalOriginal),str(i.LimitPrice)])
#         preOI=str(i.TradingDay)+' '+str(i.UpdateTime)[0:8]
#         print " ".join([str(i.InstrumentID),str(i.TradingDay),str(i.UpdateTime)[0:8],str(i.UpdateMillisec),str(i.LastPrice),str(i.Volume),str(i.AskPrice1),str(i.AskVolume1),str(i.BidPrice1),str(i.BidVolume1)])
    print 'finish'



    
