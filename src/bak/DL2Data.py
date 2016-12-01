#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys,os,time,datetime,struct,zipfile,gzip
'''
///MDBestAndDeep���������嵵�������
typedef struct MDBestAndDeep{
    INT1        Type;
    UINT4        Length;                            //���ĳ���
    UINT4        Version;                        //�汾��1��ʼ
    UINT4        Time;                            //Ԥ���ֶ�
    INT1        Exchange[3];                    //������
    INT1        Contract[80];                    //��Լ����
    BOOL        SuspensionSign;                    //ͣ�Ʊ�־
    REAL4        LastClearPrice;                    //������
    REAL4        ClearPrice;                        //������
    REAL4        AvgPrice;                        //�ɽ�����
    REAL4        LastClose;                        //������
    REAL4        Close;                            //������
    REAL4        OpenPrice;                        //����
    UINT4        LastOpenInterest;                //��ֲ���
    UINT4        OpenInterest;                    //�ֲ���
    REAL4        LastPrice;                        //���¼�
    UINT4        MatchTotQty;                    //�ɽ�����
    REAL8        Turnover;                        //�ɽ����
    REAL4        RiseLimit;                        //��߱���
    REAL4        FallLimit;                        //��ͱ���
    REAL4        HighPrice;                        //��߼�
    REAL4        LowPrice;                        //��ͼ�
    REAL4        PreDelta;                        //����ʵ��
    REAL4        CurrDelta;                        //����ʵ��
    REAL4        BuyPriceOne;                    //����۸�1
    UINT4        BuyQtyOne;                        //��������1
    UINT4        BuyImplyQtyOne;                    //��1�Ƶ���
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
    REAL4        SellPriceOne;                    //�����۸�1
    UINT4        SellQtyOne;                        //�������1
    UINT4        SellImplyQtyOne;                //��1�Ƶ���
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
    INT1        GenTime[13];                    //�������ʱ��
    UINT4        LastMatchQty;                    //���³ɽ���
    INT4        InterestChg;                    //�ֲ����仯
    REAL4        LifeLow;                        //��ʷ��ͼ�
    REAL4        LifeHigh;                        //��ʷ��߼�
    REAL8        Delta;                            //delta
    REAL8        Gamma;                            //gama
    REAL8        Rho;                            //rho
    REAL8        Theta;                            //theta
    REAL8        Vega;                            //vega
    INT1        TradeDate[9];                    //��������
    INT1        LocalDate[9];                    //��������
}THYQuote;

////////////////////////////////////////////////
///MDTenEntrust�����ż�λ��ʮ��ί��
////////////////////////////////////////////////
typedef struct MDTenEntrust{
    INT1        Type;                            //�������ʶ
    UINT4        Len;
    INT1        Contract[80];                    //��Լ����
    REAL8        BestBuyOrderPrice;                //�۸�
    UINT4        BestBuyOrderQtyOne;                //ί����1
    UINT4        BestBuyOrderQtyTwo;                //ί����2
    UINT4        BestBuyOrderQtyThree;            //ί����3
    UINT4        BestBuyOrderQtyFour;            //ί����4
    UINT4        BestBuyOrderQtyFive;            //ί����5
    UINT4        BestBuyOrderQtySix;                //ί����6
    UINT4        BestBuyOrderQtySeven;            //ί����7
    UINT4        BestBuyOrderQtyEight;            //ί����8
    UINT4        BestBuyOrderQtyNine;            //ί����9
    UINT4        BestBuyOrderQtyTen;                //ί����10
    REAL8        BestSellOrderPrice;                //�۸�
    UINT4        BestSellOrderQtyOne;            //ί����1
    UINT4        BestSellOrderQtyTwo;            //ί����2
    UINT4        BestSellOrderQtyThree;            //ί����3
    UINT4        BestSellOrderQtyFour;            //ί����4
    UINT4        BestSellOrderQtyFive;            //ί����5
    UINT4        BestSellOrderQtySix;            //ί����6
    UINT4        BestSellOrderQtySeven;            //ί����7
    UINT4        BestSellOrderQtyEight;            //ί����8
    UINT4        BestSellOrderQtyNine;            //ί����9
    UINT4        BestSellOrderQtyTen;            //ί����10
    INT1        GenTime[13];                    //����ʱ��
}TENENTRUST;

////////////////////////////////////////////////
///MDOrderStatistic����Ȩƽ���Լ�ί����������
////////////////////////////////////////////////
typedef struct MDOrderStatistic{
    INT1        Type;                            //�������ʶ
    UINT4        Len;
    INT1        ContractID[80];                    //��Լ��
    UINT4        TotalBuyOrderNum;                //��ί������
    UINT4        TotalSellOrderNum;                //��ί������
    REAL8        WeightedAverageBuyOrderPrice;    //��Ȩƽ��ί��۸�
    REAL8        WeightedAverageSellOrderPrice;    //��Ȩƽ��ί���۸�
}ORDERSTATISTIC;

////////////////////////////////////////////////
///MDRealTimePrice��ʵʱ�����
////////////////////////////////////////////////
typedef struct MDRealTimePrice{
    INT1        Type;                            //�������ʶ
    UINT4        Len;
    INT1        ContractID[80];                    //��Լ��
    REAL8        RealTimePrice;                    //ʵʱ�����
}REALTIMEPRICE;

////////////////////////////////////////////////
///MDMarchPriceQty���ּ�λ�ɽ�
////////////////////////////////////////////////
typedef struct MDMarchPriceQty{
    INT1        Type;                            //�������ʶ
    UINT4        Len;
    INT1        ContractID[80];                    //��Լ��
    REAL8        PriceOne;                        //�۸�
    UINT4        PriceOneBOQty;                    //������
    UINT4        PriceOneBEQty;                    //��ƽ����
    UINT4        PriceOneSOQty;                    //��������
    UINT4        PriceOneSEQty;                    //��ƽ����
    REAL8        PriceTwo;                        //�۸�
    UINT4        PriceTwoBOQty;                    //������
    UINT4        PriceTwoBEQty;                    //��ƽ����
    UINT4        PriceTwoSOQty;                    //��������
    UINT4        PriceTwoSEQty;                    //��ƽ����
    REAL8        PriceThree;                        //�۸�
    UINT4        PriceThreeBOQty;                //������
    UINT4        PriceThreeBEQty;                //��ƽ����
    UINT4        PriceThreeSOQty;                //��������
    UINT4        PriceThreeSEQty;                //��ƽ����
    REAL8        PriceFour;                        //�۸�
    UINT4        PriceFourBOQty;                    //������
    UINT4        PriceFourBEQty;                    //��ƽ����
    UINT4        PriceFourSOQty;                    //��������
    UINT4        PriceFourSEQty;                    //��ƽ����
    REAL8        PriceFive;                        //�۸�
    UINT4        PriceFiveBOQty;                    //������
    UINT4        PriceFiveBEQty;                    //��ƽ����
    UINT4        PriceFiveSOQty;                    //��������
    UINT4        PriceFiveSEQty;                    //��ƽ����
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
    #�����б�����
    str_path = r"F:\bigdata\\"
    list_MDBestAndDeep = getMDBestAndDeep(str_date,str_instrumentID,str_path)
    Data=[]
    for i in list_MDBestAndDeep:
        Data.append([i.GenTime[0:8],i.LastPrice])
    return Data

if __name__=="__main__": main()

