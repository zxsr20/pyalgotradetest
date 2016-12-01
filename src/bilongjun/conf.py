#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"
import re

class CInstrumentInfo():
    def __init__(self,iid,pt,vm):
        self.InstrumentID = iid #代码
        self.PriceTick = pt  # 最小变动价
        self.VolumeMultiple = vm  #合约乘数

def getInstrumentInfo(strInstrumentID):
    InstrumentID=re.findall('\D*',strInstrumentID)[0]#匹配任何非数字
    #info={'IF':[0.2,300],'m':[1,10],'y':[2,10]}
    Info={'ru':[10,5],'al':[5,5],'zn':[5,5],'cu':[5,10],'wr':[10,1],'rb':[10,1],'au':[100,0.05],
          'ag':[15,1],'pb':[25,5],'fu':[50,1],'bu':[10,2],'hc':[10,2],'c':[10,1],'a':[10,1],
          'm':[10,1],'y':[10,2],'p':[10,2],'l':[5,5],'v':[5,5],'JM':[60,1],'j':[100,1],'I':[100,1],'JD':[5,1],
          'fb':[500,0.05],'bb':[500,0.05],'pp':[5,1],'CF':[5,5],'TA':[5,2],'OI':[10,2],'WH':[20,1],
          'RI':[20,1],'SR':[10,1],'FG':[20,1],'ME':[50,1],'PM':[50,1],'RM':[10,1],'RS':[10,1],
          'TC':[200,0.2],'JR':[20,1],'IF':[300,0.2],'TF':[1000000,0.002]}
    #if strInstrumentID[0:2] == "IF" :
        #ni = CInstrumentInfo(strInstrumentID, 0.2,300)
        #return ni
    # (合约名称，最小变动价位，合约乘数)
    return CInstrumentInfo(strInstrumentID,Info[InstrumentID][1],Info[InstrumentID][0])

if __name__=="__main__":
    strInstrumentID='ru1501'
    CInstrumentInfo=getInstrumentInfo(strInstrumentID)
    print CInstrumentInfo.InstrumentID,CInstrumentInfo.PriceTick,CInstrumentInfo.VolumeMultiple 
    

#不太懂   是为了找到ru对应的【10,5】吗 然后得到一个类，得到最小变动价10，合约岑书5吗
