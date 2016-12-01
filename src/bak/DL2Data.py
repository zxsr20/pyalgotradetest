#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys,os,time,datetime,struct,zipfile,gzip
'''
///MDBestAndDeep：最优与五档深度行情
typedef struct MDBestAndDeep{
    INT1        Type;
    UINT4        Length;                            //报文长度
    UINT4        Version;                        //版本从1开始
    UINT4        Time;                            //预留字段
    INT1        Exchange[3];                    //交易所
    INT1        Contract[80];                    //合约代码
    BOOL        SuspensionSign;                    //停牌标志
    REAL4        LastClearPrice;                    //昨结算价
    REAL4        ClearPrice;                        //今结算价
    REAL4        AvgPrice;                        //成交均价
    REAL4        LastClose;                        //昨收盘
    REAL4        Close;                            //今收盘
    REAL4        OpenPrice;                        //今开盘
    UINT4        LastOpenInterest;                //昨持仓量
    UINT4        OpenInterest;                    //持仓量
    REAL4        LastPrice;                        //最新价
    UINT4        MatchTotQty;                    //成交数量
    REAL8        Turnover;                        //成交金额
    REAL4        RiseLimit;                        //最高报价
    REAL4        FallLimit;                        //最低报价
    REAL4        HighPrice;                        //最高价
    REAL4        LowPrice;                        //最低价
    REAL4        PreDelta;                        //昨虚实度
    REAL4        CurrDelta;                        //今虚实度
    REAL4        BuyPriceOne;                    //买入价格1
    UINT4        BuyQtyOne;                        //买入数量1
    UINT4        BuyImplyQtyOne;                    //买1推导量
    REAL4        BuyPriceTwo;         
    UINT4        BuyQtyTwo;
    UINT4        BuyImplyQtyTwo;
    REAL4        BuyPriceThree;
    UINT4        BuyQtyThree;
    UINT4        BuyImplyQtyThree;
    REAL4        BuyPriceFour;
    UINT4        BuyQtyFour;
    UINT4        BuyImplyQtyFour;
    REAL4        BuyPriceFive;
    UINT4        BuyQtyFive;
    UINT4        BuyImplyQtyFive;
    REAL4        SellPriceOne;                    //卖出价格1
    UINT4        SellQtyOne;                        //买出数量1
    UINT4        SellImplyQtyOne;                //卖1推导量
    REAL4        SellPriceTwo;        
    UINT4        SellQtyTwo;
    UINT4        SellImplyQtyTwo;
    REAL4        SellPriceThree;
    UINT4        SellQtyThree;
    UINT4        SellImplyQtyThree;
    REAL4        SellPriceFour;
    UINT4        SellQtyFour;
    UINT4        SellImplyQtyFour;
    REAL4        SellPriceFive;
    UINT4        SellQtyFive;
    UINT4        SellImplyQtyFive;
    INT1        GenTime[13];                    //行情产生时间
    UINT4        LastMatchQty;                    //最新成交量
    INT4        InterestChg;                    //持仓量变化
    REAL4        LifeLow;                        //历史最低价
    REAL4        LifeHigh;                        //历史最高价
    REAL8        Delta;                            //delta
    REAL8        Gamma;                            //gama
    REAL8        Rho;                            //rho
    REAL8        Theta;                            //theta
    REAL8        Vega;                            //vega
    INT1        TradeDate[9];                    //行情日期
    INT1        LocalDate[9];                    //本地日期
}THYQuote;

////////////////////////////////////////////////
///MDTenEntrust：最优价位上十笔委托
////////////////////////////////////////////////
typedef struct MDTenEntrust{
    INT1        Type;                            //行情域标识
    UINT4        Len;
    INT1        Contract[80];                    //合约代码
    REAL8        BestBuyOrderPrice;                //价格
    UINT4        BestBuyOrderQtyOne;                //委托量1
    UINT4        BestBuyOrderQtyTwo;                //委托量2
    UINT4        BestBuyOrderQtyThree;            //委托量3
    UINT4        BestBuyOrderQtyFour;            //委托量4
    UINT4        BestBuyOrderQtyFive;            //委托量5
    UINT4        BestBuyOrderQtySix;                //委托量6
    UINT4        BestBuyOrderQtySeven;            //委托量7
    UINT4        BestBuyOrderQtyEight;            //委托量8
    UINT4        BestBuyOrderQtyNine;            //委托量9
    UINT4        BestBuyOrderQtyTen;                //委托量10
    REAL8        BestSellOrderPrice;                //价格
    UINT4        BestSellOrderQtyOne;            //委托量1
    UINT4        BestSellOrderQtyTwo;            //委托量2
    UINT4        BestSellOrderQtyThree;            //委托量3
    UINT4        BestSellOrderQtyFour;            //委托量4
    UINT4        BestSellOrderQtyFive;            //委托量5
    UINT4        BestSellOrderQtySix;            //委托量6
    UINT4        BestSellOrderQtySeven;            //委托量7
    UINT4        BestSellOrderQtyEight;            //委托量8
    UINT4        BestSellOrderQtyNine;            //委托量9
    UINT4        BestSellOrderQtyTen;            //委托量10
    INT1        GenTime[13];                    //生成时间
}TENENTRUST;

////////////////////////////////////////////////
///MDOrderStatistic：加权平均以及委托总量行情
////////////////////////////////////////////////
typedef struct MDOrderStatistic{
    INT1        Type;                            //行情域标识
    UINT4        Len;
    INT1        ContractID[80];                    //合约号
    UINT4        TotalBuyOrderNum;                //买委托总量
    UINT4        TotalSellOrderNum;                //卖委托总量
    REAL8        WeightedAverageBuyOrderPrice;    //加权平均委买价格
    REAL8        WeightedAverageSellOrderPrice;    //加权平均委卖价格
}ORDERSTATISTIC;

////////////////////////////////////////////////
///MDRealTimePrice：实时结算价
////////////////////////////////////////////////
typedef struct MDRealTimePrice{
    INT1        Type;                            //行情域标识
    UINT4        Len;
    INT1        ContractID[80];                    //合约号
    REAL8        RealTimePrice;                    //实时结算价
}REALTIMEPRICE;

////////////////////////////////////////////////
///MDMarchPriceQty：分价位成交
////////////////////////////////////////////////
typedef struct MDMarchPriceQty{
    INT1        Type;                            //行情域标识
    UINT4        Len;
    INT1        ContractID[80];                    //合约号
    REAL8        PriceOne;                        //价格
    UINT4        PriceOneBOQty;                    //买开数量
    UINT4        PriceOneBEQty;                    //买平数量
    UINT4        PriceOneSOQty;                    //卖开数量
    UINT4        PriceOneSEQty;                    //卖平数量
    REAL8        PriceTwo;                        //价格
    UINT4        PriceTwoBOQty;                    //买开数量
    UINT4        PriceTwoBEQty;                    //买平数量
    UINT4        PriceTwoSOQty;                    //卖开数量
    UINT4        PriceTwoSEQty;                    //卖平数量
    REAL8        PriceThree;                        //价格
    UINT4        PriceThreeBOQty;                //买开数量
    UINT4        PriceThreeBEQty;                //买平数量
    UINT4        PriceThreeSOQty;                //卖开数量
    UINT4        PriceThreeSEQty;                //卖平数量
    REAL8        PriceFour;                        //价格
    UINT4        PriceFourBOQty;                    //买开数量
    UINT4        PriceFourBEQty;                    //买平数量
    UINT4        PriceFourSOQty;                    //卖开数量
    UINT4        PriceFourSEQty;                    //卖平数量
    REAL8        PriceFive;                        //价格
    UINT4        PriceFiveBOQty;                    //买开数量
    UINT4        PriceFiveBEQty;                    //买平数量
    UINT4        PriceFiveSOQty;                    //卖开数量
    UINT4        PriceFiveSEQty;                    //卖平数量
}MARCHPRICEQTY;


'''
class CMDBestAndDeep():
    def __init__(self):
        pass
class CMDTenEntrust():
    def __init__(self):
        pass
class CMDOrderStatistic():
    def __init__(self):
        pass
class CMDRealTimePrice():
    def __init__(self):
        pass
class CMDMarchPriceQty():
    def __init__(self):
        pass


def getMDBestAndDeep(Data,InstrumentID,path ="./"):
    fz = zipfile.ZipFile(path+"/"+Data+".zip","r")
    namelist = fz.namelist()
    if InstrumentID not in namelist :
        return []
    lines = fz.read(InstrumentID) ;# print "len(lines):" + str(len(lines))
    (head_size,data_size,data_idx) = struct.unpack('iii',lines[0:12])
    #print head_size,data_size,data_idx
    data_start = lines[head_size+8:]
    data_list = []
    data_one_length = 386
    data_one_length_pack4 = data_one_length  + data_one_length % 4
    for i in range(0,data_idx):
        date_one = data_start[i*data_one_length_pack4:(i+1)*data_one_length_pack4]
        one_MDBestAndDeep = CMDBestAndDeep()
        om = one_MDBestAndDeep
        om.Type,om.Length,om.Version,om.Time,om.Exchange,om.Contract,om.SuspensionSign,om.LastClearPrice,om.ClearPrice,om.AvgPrice,om.LastClose,om.Close,om.OpenPrice,om.LastOpenInterest,om.OpenInterest,om.LastPrice,om.MatchTotQty,om.Turnover,om.RiseLimit,om.FallLimit,om.HighPrice,om.LowPrice,om.PreDelta,om.CurrDelta,om.BuyPriceOne,om.BuyQtyOne,om.BuyImplyQtyOne,om.BuyPriceTwo,om.BuyQtyTwo,om.BuyImplyQtyTwo,om.BuyPriceThree,om.BuyQtyThree,om.BuyImplyQtyThree,om.BuyPriceFour,om.BuyQtyFour,om.BuyImplyQtyFour,om.BuyPriceFive,om.BuyQtyFive,om.BuyImplyQtyFive,om.SellPriceOne,om.SellQtyOne,om.SellImplyQtyOne,om.SellPriceTwo,om.SellQtyTwo,om.SellImplyQtyTwo,om.SellPriceThree,om.SellQtyThree,om.SellImplyQtyThree,om.SellPriceFour,om.SellQtyFour,om.SellImplyQtyFour,om.SellPriceFive,om.SellQtyFive,om.SellImplyQtyFive,om.GenTime,om.LastMatchQty,om.InterestChg,om.LifeLow,om.LifeHigh,om.Delta,om.Gamma,om.Rho,om.Theta,om.Vega,om.TradeDate,om.LocalDate= struct.unpack('cIII3s80siffffffIIfIdfffffffIIfIIfIIfIIfIIfIIfIIfIIfIIfII13sIiffddddd9s9s',date_one[0:data_one_length])
        #print "[",om.Type,om.Length,om.Version,om.Time,om.Exchange,om.Contract,om.LastPrice,om.MatchTotQty,om.Turnover,om.BuyPriceOne,om.BuyQtyOne,om.BuyImplyQtyOne,om.BuyPriceTwo,om.BuyQtyTwo,om.BuyImplyQtyTwo,om.BuyPriceThree,om.BuyQtyThree,om.BuyImplyQtyThree,om.BuyPriceFour,om.BuyQtyFour,om.BuyImplyQtyFour,om.BuyPriceFive,om.BuyQtyFive,om.BuyImplyQtyFive,om.SellPriceOne,om.SellQtyOne,om.SellImplyQtyOne,om.SellPriceTwo,om.SellQtyTwo,om.SellImplyQtyTwo,om.SellPriceThree,om.SellQtyThree,om.SellImplyQtyThree,om.SellPriceFour,om.SellQtyFour,om.SellImplyQtyFour,om.SellPriceFive,om.SellQtyFive,om.SellImplyQtyFive,om.GenTime,om.LastMatchQty,om.InterestChg,om.LifeLow,om.LifeHigh,om.Delta,om.Gamma,om.Rho,om.Theta,om.Vega,om.TradeDate,om.LocalDate,"]"
        data_list += [om]
    return data_list

def getMDTenEntrust(Data,InstrumentID,path ="./"):
    fz = zipfile.ZipFile(path+"/"+Data+".zip","r")
    namelist = fz.namelist()
    file_data_name = InstrumentID + "_TenEntrust"
    if file_data_name not in namelist :
        return []
    lines = fz.read(file_data_name) ;# print "len(lines):" + str(len(lines))
    (head_size,data_size,data_idx) = struct.unpack('iii',lines[0:12])
    #print head_size,data_size,data_idx
    data_start = lines[head_size+8:]
    data_list = []
    data_one_length = 197
    data_one_length_pack4 = 200 #data_one_length  + data_one_length % 4 ; print "data_one_length_pack4",data_one_length_pack4
    for i in range(0,data_idx):
    #for i in range(0,3):
        date_one = data_start[i*data_one_length_pack4:(i+1)*data_one_length_pack4]
        o = CMDTenEntrust()
        o.Type,o.Len,o.Contract,o.BestBuyOrderPrice,o.BestBuyOrderQtyOne,o.BestBuyOrderQtyTwo,o.BestBuyOrderQtyThree,o.BestBuyOrderQtyFour,o.BestBuyOrderQtyFive,o.BestBuyOrderQtySix,o.BestBuyOrderQtySeven,o.BestBuyOrderQtyEight,o.BestBuyOrderQtyNine,o.BestBuyOrderQtyTen,o.BestSellOrderPrice,o.BestSellOrderQtyOne,o.BestSellOrderQtyTwo,o.BestSellOrderQtyThree,o.BestSellOrderQtyFour,o.BestSellOrderQtyFive,o.BestSellOrderQtySix,o.BestSellOrderQtySeven,o.BestSellOrderQtyEight,o.BestSellOrderQtyNine,o.BestSellOrderQtyTen,o.GenTime = struct.unpack('cI80sdIIIIIIIIIIdIIIIIIIIII13s',date_one[0:data_one_length])
        #print "[",o.Type,o.Len,o.Contract,o.BestBuyOrderPrice,o.BestBuyOrderQtyOne,o.BestBuyOrderQtyTwo,o.BestBuyOrderQtyThree,o.BestBuyOrderQtyFour,o.BestBuyOrderQtyFive,o.BestBuyOrderQtySix,o.BestBuyOrderQtySeven,o.BestBuyOrderQtyEight,o.BestBuyOrderQtyNine,o.BestBuyOrderQtyTen,o.BestSellOrderPrice,o.BestSellOrderQtyOne,o.BestSellOrderQtyTwo,o.BestSellOrderQtyThree,o.BestSellOrderQtyFour,o.BestSellOrderQtyFive,o.BestSellOrderQtySix,o.BestSellOrderQtySeven,o.BestSellOrderQtyEight,o.BestSellOrderQtyNine,o.BestSellOrderQtyTen,o.GenTime,"]"
        data_list += [o]
    return data_list

def getMDOrderStatistic(Data,InstrumentID,path ="./"):
    fz = zipfile.ZipFile(path+"/"+Data+".zip","r")
    namelist = fz.namelist()
    file_data_name = InstrumentID + "_OrderStatistic"
    if file_data_name not in namelist :
        return []
    lines = fz.read(file_data_name) ;# print "len(lines):" + str(len(lines))
    (head_size,data_size,data_idx) = struct.unpack('iii',lines[0:12])
    #print head_size,data_size,data_idx
    data_start = lines[head_size+8:]
    data_list = []
    data_one_length = 112
    data_one_length_pack4 = data_one_length  #+ data_one_length % 4 ;# print "data_one_length_pack4",data_one_length_pack4
    for i in range(0,data_idx):
        date_one = data_start[i*data_one_length_pack4:(i+1)*data_one_length_pack4]
        o = CMDOrderStatistic()
        o.Type,o.Len,o.ContractID,o.TotalBuyOrderNum,o.TotalSellOrderNum,o.WeightedAverageBuyOrderPrice,o.WeightedAverageSellOrderPrice = struct.unpack('cI80sIIdd',date_one[0:data_one_length])
        #print "[",o.Type,o.Len,o.ContractID,o.TotalBuyOrderNum,o.TotalSellOrderNum,o.WeightedAverageBuyOrderPrice,o.WeightedAverageSellOrderPrice,"]"
        data_list += [o]
    return data_list

def getMDRealTimePrice(Data,InstrumentID,path ="./"):
    fz = zipfile.ZipFile(path+"/"+Data+".zip","r")
    namelist = fz.namelist()
    file_data_name = InstrumentID + "_RealTimePrice"
    if file_data_name not in namelist :
        return []
    lines = fz.read(file_data_name) ;# print "len(lines):" + str(len(lines))
    (head_size,data_size,data_idx) = struct.unpack('iii',lines[0:12])
    #print head_size,data_size,data_idx
    data_start = lines[head_size+8:]
    data_list = []
    data_one_length = 96
    data_one_length_pack4 = data_one_length  + data_one_length % 4 ;# print "data_one_length_pack4",data_one_length_pack4
    for i in range(0,data_idx):
        date_one = data_start[i*data_one_length_pack4:(i+1)*data_one_length_pack4]
        o = CMDOrderStatistic()
        o.Type,o.Len,o.ContractID,o.RealTimePrice = struct.unpack('cI80sd',date_one[0:data_one_length])
        #print "[",o.Type,o.Len,o.ContractID,o.RealTimePrice,"]"
        data_list += [o]
    return data_list


def getMDMarchPriceQty(Data,InstrumentID,path ="./"):
    fz = zipfile.ZipFile(path+"/"+Data+".zip","r")
    namelist = fz.namelist()
    file_data_name = InstrumentID + "_MarchPrice"
    if file_data_name not in namelist :
        return []
    lines = fz.read(file_data_name) ;# print "len(lines):" + str(len(lines))
    (head_size,data_size,data_idx) = struct.unpack('iii',lines[0:12])
    #print head_size,data_size,data_idx
    data_start = lines[head_size+8:]
    data_list = []
    data_one_length = 208
    data_one_length_pack4 = data_one_length  #+ data_one_length % 4 ; print "data_one_length_pack4",data_one_length_pack4
    for i in range(0,data_idx):
        date_one = data_start[i*data_one_length_pack4:(i+1)*data_one_length_pack4]
        o = CMDOrderStatistic()
        o.Type,o.Len,o.ContractID,o.PriceOne,o.PriceOneBOQty,o.PriceOneBEQty,o.PriceOneSOQty,o.PriceOneSEQty,o.PriceTwo,o.PriceTwoBOQty,o.PriceTwoBEQty,o.PriceTwoSOQty,o.PriceTwoSEQty,o.PriceThree,o.PriceThreeBOQty,o.PriceThreeBEQty,o.PriceThreeSOQty,o.PriceThreeSEQty,o.PriceFour,o.PriceFourBOQty,o.PriceFourBEQty,o.PriceFourSOQty,o.PriceFourSEQty,o.PriceFive,o.PriceFiveBOQty,o.PriceFiveBEQty,o.PriceFiveSOQty,o.PriceFiveSEQty = struct.unpack('cI80sd4Id4Id4Id4Id4I',date_one[0:data_one_length])
        #print "[",o.Type,o.Len,o.ContractID,o.PriceOne,o.PriceOneBOQty,o.PriceOneBEQty,o.PriceOneSOQty,o.PriceOneSEQty,o.PriceTwo,o.PriceTwoBOQty,o.PriceTwoBEQty,o.PriceTwoSOQty,o.PriceTwoSEQty,o.PriceThree,o.PriceThreeBOQty,o.PriceThreeBEQty,o.PriceThreeSOQty,o.PriceThreeSEQty,o.PriceFour,o.PriceFourBOQty,o.PriceFourBEQty,o.PriceFourSOQty,o.PriceFourSEQty,o.PriceFive,o.PriceFiveBOQty,o.PriceFiveBEQty,o.PriceFiveSOQty,o.PriceFiveSEQty,"]"
        data_list += [o]
    return data_list
def main():
    # test
    str_date = "20141219"
    str_instrumentID = "m1505"
    str_path = "/home/wangf/trade/data/"
    #list_MDBestAndDeep = getMDBestAndDeep(str_date,str_instrumentID,str_path)
    #for line in list_MDBestAndDeep : print line
    #list_MDTenEntrust = getMDTenEntrust(str_date,str_instrumentID,str_path)
    #list_MDOrderStatistic = getMDOrderStatistic(str_date,str_instrumentID,str_path)
    #list_MDRealTimePrice = getMDRealTimePrice(str_date,str_instrumentID,str_path)
    #list_MDMarchPriceQty = getMDMarchPriceQty(str_date,str_instrumentID,str_path)


def getPriceData(str_instrumentID = "m1505",str_date = "20141218"):
    #返回列表数据
    str_path = r"F:\bigdata\\"
    list_MDBestAndDeep = getMDBestAndDeep(str_date,str_instrumentID,str_path)
    Data=[]
    for i in list_MDBestAndDeep:
        Data.append([i.GenTime[0:8],i.LastPrice])
    return Data

if __name__=="__main__": main()

