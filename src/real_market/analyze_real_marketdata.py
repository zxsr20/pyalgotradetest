#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys,os,time,datetime,struct,zipfile,gzip
import itertools
from pyalgotrade.optimizer import local
import codecs
from tradeanalyze import appconsant, StoreCsv4Nticket,data,conf

# 组合开平标志:0    open_close_mark
# 价格:6036.0    price
# 买卖方向:买   direction
# 数量:100   number
# 客户代码:01649432    clientcode
# 剩余数量:100    number_remain
# 报单价格条件:限价 price_condition
# 有效期类型:当日有效  valid_period_type
# 状态信息:未成交|还在队列中 status
# 报单编号:    10009892  report_no
# 报单提交状态:已经接受  report_status
# 状态信息:未成交
# 交易日:20131218  tradeday
# 委托时间:09:00:01  entrust_time
# 序号:529 no
# 报单引用:        4456  report_reference
# 投资者代码:81240258   investor_code
# 成交量类型:任何数量  volume_type
# 
# <触发条件:立即,报单提示序号:1,操作用户代码:,今成交数量:0,用户端产品信息:,组合开平标志:0,交易所交易员代码:00492002,用户代码:,价格:6036.0,用户强评标志:0,相关报单:,买卖方向:买,安装编号:2,会员代码:0049,数量:100,合约在交易所的代码:p1405,客户代码:01649432,剩余数量:100,报单价格条件:限价,会话编号:0,有效期类型:当日有效,报单状态:未成交还在队列中,报单编号:    10009888,报单提交状态:已经接受,自动挂起标志:0,止损价:0.0,合约代码:p1405,交易所代码:DCE,最小成交量:0,状态信息:未成交,结算编号:1,强平原因: ,报单类型:正常,最后修改时间:,交易日:20131218,激活时间:,经纪公司代码:8000,委托时间:09:00:01,前置编号:0,挂起时间:,结算会员编号:,组合投机套保标志:1,撤销时间:,GTD日期:,本地报单编号:           4,业务单元:,报单日期:20131218,序号:527,报单引用:        4454,经纪公司报单编号:25147,投资者代码:81240258,成交量类型:任何数量,请求编号:0,报单来源:来自参与者,最后修改交易所交易员代码:>

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
        
        
def analyze():
    datafilepath = 'D:\pyTest_yh\data\\'#数据文件位置'
    marketfilepath = 'D:\pyTest_yh\marketdata\\'#数据文件位置'
    date = '20131218'
    instrumentID = 'p1405'
    
    #数据转化
    for f in os.listdir(datafilepath):  
        file = os.path.join(datafilepath, f)  
        filename = file.split("\\")[-1].split(".")[0]
        
        if os.path.isfile(file) and filename == date:   
            print '原始文件:'+file
            data_lines = data.getDayData(instrumentID,file) #获取数据
            data_config = conf.getInstrumentInfo(instrumentID) 
            csvfile = filename + instrumentID +'.csv'
            data_lines=StoreCsv4Nticket.guiyi(instrumentID,data_lines,data_config,csvfile,malength=90)
            
#             for line in data_lines:
#                 print line.info
            
            market_lines = process_data(data_config,marketfilepath,date,instrumentID)
            
#             market_lines = market_lines.sort(lambda x: x.entrust_time)
            market_lines = sorted(market_lines, key=lambda x : x.entrust_time)
            f = open("market.txt", 'w+')  
            i = 0
            j = 0
            while True:
                if i < len(data_lines):
                    data_line = data_lines[i]
#                     print i
                else:
                    break
                if j < len(market_lines): 
                    line = market_lines[j]
                else:
                    line = None
#                 print str(data_line.UpdateTime)[0:8] + ' '+line.entrust_time
                if  line != None and str(data_line.UpdateTime)[0:8] == line.entrust_time:
                    print>>f,data_line.info
                    if str(data_lines[i+1].UpdateTime)[0:8] == line.entrust_time:
                        i += 1
                        data_line = data_lines[i] 
                        print>>f,data_line.info
                        
                    while True:
                        if j < len(market_lines):
                            line = market_lines[j]
                            if  str(data_line.UpdateTime)[0:8] == line.entrust_time:
#                                 print>>f,('合约代码'+str(line.instrumentID)
#                                     +'组合开平标志:'+str(line.open_close_mark)
#                                     +'价格:'+str(line.price)
#                                     +'买卖方向:'+line.direction
#                                     +'数量:'+str(line.number)
#                                     +'客户代码:'+line.clientcode
#                                     +'剩余数量:'+str(line.number_remain)
#                                     +'报单价格条件:'+line.price_condition
#                                     +'有效期类型:'+line.valid_period_type
#                                     +'状态信息:'+line.status
#                                     +'报单编号:'+line.report_no
#                                     +'报单提交状态:'+line.report_status
#                                     +'交易日:'+line.tradeday
#                                     +'委托时间:'+line.entrust_time
#                                     +'序号:'+line.no
#                                     +'报单引用:'+line.report_reference
#                                     +'投资者代码:'+line.investor_code
#                                     +'成交量类型:'+line.volume_type)
#                                     print>>f,(str(line.instrumentID)
#                                     +' '+'offset:'+str(line.open_close_mark)
#                                     +' '+'pri:'+str(line.price)
#                                     +' '+'dir:'+line.direction
#                                     +' '+'vol:'+str(line.number)
#                                     +' '+'userid:'+line.clientcode
#                                     +' '+'rmvol:'+str(line.number_remain)
#                                     +' '+'报单价格条件:'+line.price_condition
#                                     +' '+'有效期类型:'+line.valid_period_type
#                                     +' '+'orderstatus:'+line.status
#                                     +' '+'sysorder:'+line.report_no
#                                     +' '+'报单提交状态:'+line.report_status
#                                     +' '+'Tradingday:'+line.tradeday
#                                     +' '+'insertTime:'+line.entrust_time
#                                     +' '+'序号:'+line.no
#                                     +' '+'OrderRef:'+line.report_reference
#                                     +' '+' Invenstorid:'+line.investor_code
#                                     +' '+'成交量类型:'+line.volume_type)
                                    
                                    print>>f,(str(line.instrumentID)
                                    +' '+'offset:'+str(line.open_close_mark)
                                    +' '+'pri:'+str(line.price)
                                    +' '+'dir:'+line.direction
                                    +' '+'vol:'+str(line.number)
                                   
                                    +' '+'rmvol:'+str(line.number_remain)
                                    +' '+'报单价格条件:'+line.price_condition
                                    
                                    +' '+'orderstatus:'+line.status
                                    +' '+'OrderRef:'+line.report_reference
                                    +' '+'sysorder:'+line.report_no
                                    +' '+'报单提交状态:'+line.report_status
                                    
                                    +' '+'insertTime:'+line.entrust_time
                                    +' '+'序号:'+line.no
                                    
                                    )
                            else:
                                break
                        else:
                            break
                        j += 1
                    i += 1
                else:
                    print>>f,data_line.info
                    if i+1 < len(data_lines) and  str(data_lines[i+1].UpdateTime)[0:8] == str(data_lines[i].UpdateTime)[0:8]:
                        i += 1
                        data_line = data_lines[i] 
                        print>>f,data_line.info
                        i += 1
                    else:
                        i += 1
            
    print 'end'
            
            
#             
#                 
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
                    
                    if arr.split(':')[0] == '组合开平标志':
                        order.open_close_mark = arr.split(':')[1]
                    elif arr.split(':')[0] == '价格':
                        order.price = int(round((float)(arr.split(':')[1])/config.PriceTick))
                    elif arr.split(':')[0] == '买卖方向':
                        order.direction = arr.split(':')[1]
                    elif arr.split(':')[0] == '数量':
                        order.number = arr.split(':')[1]
                    elif arr.split(':')[0] == '客户代码':
                        order.clientcode = arr.split(':')[1]
                    elif arr.split(':')[0] == '剩余数量':
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
#                 arr = str
#                 if line.encode('utf-8').find('今成交数量') > 0:
 
    
    
if __name__=="__main__":
    analyze()
