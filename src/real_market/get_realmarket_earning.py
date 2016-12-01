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
        
        
# def analyze():
#     datafilepath = 'D:\pyTest_yh\data\\'#数据文件位置'
#     marketfilepath = 'D:\pyTest_yh\marketdata\\'#数据文件位置'
#     date = '20131218'
#     instrumentID = 'p1405'
#     
#     #数据转化
#     for f in os.listdir(datafilepath):  
#         file = os.path.join(datafilepath, f)  
#         filename = file.split("\\")[-1].split(".")[0]
#         
#         if os.path.isfile(file) and filename == date:   
#             print '原始文件:'+file
# #             data_lines = data.getDayData(instrumentID,file) #获取数据
#             data_config = conf.getInstrumentInfo(instrumentID) 
# #             csvfile = filename + instrumentID +'.csv'
# #             data_lines=StoreCsv4Nticket.guiyi(instrumentID,data_lines,data_config,csvfile,malength=90)
#             
# #             for line in data_lines:
# #                 print line.info
#             
#             market_lines = process_data(data_config,marketfilepath,date,instrumentID)
#             
# #             market_lines = market_lines.sort(lambda x: x.entrust_time)
#             market_lines = sorted(market_lines, key=lambda x : x.entrust_time)
#             f = open("market_earning.txt", 'w+')  
#             
#             orderid = ''
#             money = 0.0
#             long_num = 0
#             short_num = 0
#             for line in market_lines:
#                 if line.status == '未成交':
#                     orderid = line.report_reference
#                     order_remain_num = line.number
#                     print>>f, '下单 orderid:'+str(orderid)+' 总数量：'+str(line.number)+'price: '+str(line.price)+' offset:'+str(line.open_close_mark)+' dir'+str(line.direction)
#                     for line_2 in market_lines:
#                         if line_2.report_reference == orderid:
#                             if line_2.status == '部分成交' or line_2.status == '全部成交':
#                                 chengjiao_num = order_remain_num - line_2.number_remain
#                                 if line.open_close_mark == 0:
#                                     chengjiao_cost = -chengjiao_num * line_2.price
#                                     if line_2.direction == '买':
#                                         long_num += chengjiao_num
#                                     elif line_2.direction == '卖':
#                                         short_num += chengjiao_num
#                                 elif line.open_close_mark == 1:
#                                     chengjiao_cost = chengjiao_num * line_2.price
#                                     if line_2.direction == '买':
#                                         short_num -= chengjiao_num
#                                     elif line_2.direction == '卖':
#                                         long_num -= chengjiao_num
#                                 money = money+chengjiao_cost
#                                 print>>f, 'orderid:'+str(orderid)+' 总数量：'+str(line.number)+' 本次成交数量:'+ str(chengjiao_num)+' 单价'+str(line_2.price)+' 花费:'+str(chengjiao_cost)
#                                 order_remain_num = line_2.number_remain
#                             
#                             elif line_2.status =='已撤单':
#                                 print>>f, 'orderid:'+str(orderid)+ ' 已撤单'
#                                 break
#             print>>f,'最后盈利:'+str(money)+'剩余持仓  买多:'+str(long_num)+'买空:'+str(short_num)
#             
#             
#             
#     print 'end'
            
def analyze2():
    #修改算法，
    #在部分成交或全部成交的时候去计算它之前开仓的map，然后算出它的盈利点    
    datafilepath = 'D:\pyTest_yh\data\\'#数据文件位置'
    marketfilepath = 'D:\pyTest_yh\marketdata\\'#数据文件位置'
    date = '20131218'
    instrumentID = 'y1405'
    
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
            f = open(date+instrumentID+"market_earning.txt", 'w+')  
            
            
            buy_dic = {}#用于保存开仓是买的价格和数量
            sell_dic = {}#用于保存开仓是卖的价格和数量
            orderid = ''
            money = 0.0
            long_num = 0
            short_num = 0
            win_point_total = 0
            for line in market_lines:
                while str(data_lines[0].UpdateTime)[0:8] <= line.entrust_time:
                    print>>f,data_lines[0].info
                    data_lines.remove(data_lines[0])
                if line.status == '未成交':
                    orderid = line.report_reference
                    order_remain_num = line.number
                    print>>f, '下单 orderid:'+str(orderid)+' 总数量：'+str(line.number)+' price: '+str(line.price)+' offset:'+str(line.open_close_mark)+' dir'+str(line.direction)
                    for line_2 in market_lines:
                        if line_2.report_reference == orderid:
                            if line_2.status == '部分成交' or line_2.status == '全部成交':
                                win_point = 0
                                chengjiao_num = order_remain_num - line_2.number_remain
                                if line.open_close_mark == 0:
                                    chengjiao_cost = -chengjiao_num * line_2.price
                                    if line_2.direction == '买':
                                        if buy_dic.has_key(line_2.price):
                                            buy_dic[line_2.price] = buy_dic[line_2.price] + chengjiao_num
                                        else:
                                            buy_dic[line_2.price] = chengjiao_num
                                        long_num += chengjiao_num
                                    elif line_2.direction == '卖':
                                        if sell_dic.has_key(line_2.price):
                                            sell_dic[line_2.price] = sell_dic[line_2.price] + chengjiao_num
                                        else:
                                            sell_dic[line_2.price] = chengjiao_num
                                        short_num += chengjiao_num
                                elif line.open_close_mark == 1:
                                    chengjiao_cost = chengjiao_num * line_2.price
                                    
                                    if line_2.direction == '买':
                                        #去前面的字典去取
                                        num = chengjiao_num
                                        for k, value in sell_dic.items():
                                            if num >= value:
                                                del(sell_dic[k])
                                                num = num - value
                                                win_point += (k - line_2.price)* value
                                                print>>f,'买平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((k - line_2.price)* value)
                                            elif num == value:
                                                del(sell_dic[k])
                                                num = num - value
                                                win_point += (k - line_2.price)* value
                                                print>>f,'买平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((k - line_2.price)* value)
                                                break
                                            else:
                                                sell_dic[k] = value - num
                                                win_point += (k - line_2.price)* num
                                                print>>f,'买平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((k - line_2.price)* num)
                                                num = 0
                                                break
                                                
                                        short_num -= chengjiao_num
                                    elif line_2.direction == '卖':
                                        num = chengjiao_num
                                        for k, value in buy_dic.items():
                                            if num >= value:
                                                del(buy_dic[k])
                                                num = num - value
                                                win_point += (line_2.price - k)* value
                                                print>>f,'卖平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((line_2.price - k)* value)
                                            elif num == value:
                                                del(buy_dic[k])
                                                num = num - value
                                                win_point += (line_2.price - k)* value
                                                print>>f,'卖平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((line_2.price - k)* value)
                                                break
                                            else:
                                                buy_dic[k] = value - num
                                                win_point += (line_2.price - k)* num
                                                print>>f,'卖平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((line_2.price - k)* num)
                                                
                                                num = 0
                                                break
                                        long_num -= chengjiao_num
                                money = money+chengjiao_cost
                                win_point_total += win_point
                                if line.open_close_mark == 1:
                                    print>>f, 'orderid:'+str(orderid)+' 总数量：'+str(line.number)+' 本次成交数量:'+ str(chengjiao_num)+' 单价'+str(line_2.price)+' 盈利点:'+str(win_point)
                                else:
                                    print>>f, 'orderid:'+str(orderid)+' 总数量：'+str(line.number)+' 本次成交数量:'+ str(chengjiao_num)+' 单价'+str(line_2.price)
                                order_remain_num = line_2.number_remain
                            
                            elif line_2.status =='已撤单':
                                print>>f, 'orderid:'+str(orderid)+ ' 已撤单'
                                break
            print>>f,str(sell_dic.items())+' '+str(buy_dic.items())
            
            print>>f,'最后盈利点:'+str(win_point_total)+'剩余持仓  买多:'+str(long_num)+'买空:'+str(short_num)
            
            
            
    print 'end'
    
    
    
def analyze3():
    #修改算法，
    #在部分成交或全部成交的时候去计算它之前开仓的map，然后算出它的盈利点    
    datafilepath = 'D:\pyTest_yh\data\\'#数据文件位置'
    marketfilepath = 'D:\pyTest_yh\marketdata\\'#数据文件位置'
    date = '20131218'
    instrumentID = 'y1405'
    
    instrumentID2 = 'p1405'
    
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
            
            market_lines = sorted(market_lines, key=lambda x : x.entrust_time)
            
            data_lines2 = data.getDayData(instrumentID,file) #获取数据
            data_config2 = conf.getInstrumentInfo(instrumentID) 
            csvfile2 = filename + instrumentID +'.csv'
            data_lines2=StoreCsv4Nticket.guiyi(instrumentID2,data_lines2,data_config2,csvfile2,malength=90)
            
#             for line in data_lines:
#                 print line.info
            
            market_lines2 = process_data(data_config2,marketfilepath,date,instrumentID2)
            market_lines2 = sorted(market_lines2, key=lambda x : x.entrust_time)
#             market_lines = market_lines.sort(lambda x: x.entrust_time)
            
            f = open(date+"twomarket_earning.txt", 'w+')  
            
            
            buy_dic = {}#用于保存开仓是买的价格和数量
            sell_dic = {}#用于保存开仓是卖的价格和数量
            orderid = ''
            money = 0.0
            long_num = 0
            short_num = 0
            win_point_total = 0
            for line in market_lines:
                while str(data_lines[0].UpdateTime)[0:8] <= line.entrust_time:
                    print>>f,data_lines[0].info
                    data_lines.remove(data_lines[0])
                if line.status == '未成交':
                    orderid = line.report_reference
                    order_remain_num = line.number
                    print>>f, '下单 orderid:'+str(orderid)+' 总数量：'+str(line.number)+' price: '+str(line.price)+' offset:'+str(line.open_close_mark)+' dir'+str(line.direction)
                    for line_2 in market_lines:
                        if line_2.report_reference == orderid:
                            if line_2.status == '部分成交' or line_2.status == '全部成交':
                                win_point = 0
                                chengjiao_num = order_remain_num - line_2.number_remain
                                if line.open_close_mark == 0:
                                    chengjiao_cost = -chengjiao_num * line_2.price
                                    if line_2.direction == '买':
                                        if buy_dic.has_key(line_2.price):
                                            buy_dic[line_2.price] = buy_dic[line_2.price] + chengjiao_num
                                        else:
                                            buy_dic[line_2.price] = chengjiao_num
                                        long_num += chengjiao_num
                                    elif line_2.direction == '卖':
                                        if sell_dic.has_key(line_2.price):
                                            sell_dic[line_2.price] = sell_dic[line_2.price] + chengjiao_num
                                        else:
                                            sell_dic[line_2.price] = chengjiao_num
                                        short_num += chengjiao_num
                                elif line.open_close_mark == 1:
                                    chengjiao_cost = chengjiao_num * line_2.price
                                    
                                    if line_2.direction == '买':
                                        #去前面的字典去取
                                        num = chengjiao_num
                                        for k, value in sell_dic.items():
                                            if num >= value:
                                                del(sell_dic[k])
                                                num = num - value
                                                win_point += (k - line_2.price)* value
                                                print>>f,'买平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((k - line_2.price)* value)
                                            elif num == value:
                                                del(sell_dic[k])
                                                num = num - value
                                                win_point += (k - line_2.price)* value
                                                print>>f,'买平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((k - line_2.price)* value)
                                                break
                                            else:
                                                sell_dic[k] = value - num
                                                win_point += (k - line_2.price)* num
                                                print>>f,'买平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((k - line_2.price)* num)
                                                num = 0
                                                break
                                                
                                        short_num -= chengjiao_num
                                    elif line_2.direction == '卖':
                                        num = chengjiao_num
                                        for k, value in buy_dic.items():
                                            if num >= value:
                                                del(buy_dic[k])
                                                num = num - value
                                                win_point += (line_2.price - k)* value
                                                print>>f,'卖平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((line_2.price - k)* value)
                                            elif num == value:
                                                del(buy_dic[k])
                                                num = num - value
                                                win_point += (line_2.price - k)* value
                                                print>>f,'卖平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((line_2.price - k)* value)
                                                break
                                            else:
                                                buy_dic[k] = value - num
                                                win_point += (line_2.price - k)* num
                                                print>>f,'卖平分笔盈利点  开仓价：'+str(k)+' 当前价:'+str(line_2.price)+'数量：'+str(value)+'盈利点：'+str((line_2.price - k)* num)
                                                
                                                num = 0
                                                break
                                        long_num -= chengjiao_num
                                money = money+chengjiao_cost
                                win_point_total += win_point
                                if line.open_close_mark == 1:
                                    print>>f, 'orderid:'+str(orderid)+' 总数量：'+str(line.number)+' 本次成交数量:'+ str(chengjiao_num)+' 单价'+str(line_2.price)+' 盈利点:'+str(win_point)
                                else:
                                    print>>f, 'orderid:'+str(orderid)+' 总数量：'+str(line.number)+' 本次成交数量:'+ str(chengjiao_num)+' 单价'+str(line_2.price)
                                order_remain_num = line_2.number_remain
                            
                            elif line_2.status =='已撤单':
                                print>>f, 'orderid:'+str(orderid)+ ' 已撤单'
                                break
            print>>f,str(sell_dic.items())+' '+str(buy_dic.items())
            
            print>>f,'最后盈利点:'+str(win_point_total)+'剩余持仓  买多:'+str(long_num)+'买空:'+str(short_num)
            
            
            
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
                        order.open_close_mark = (int)(arr.split(':')[1])
                    elif arr.split(':')[0] == '价格':
                        order.price = int(round((float)(arr.split(':')[1])/config.PriceTick))
                    elif arr.split(':')[0] == '买卖方向':
                        order.direction = arr.split(':')[1]
                    elif arr.split(':')[0] == '数量':
                        order.number = (int)(arr.split(':')[1])
                    elif arr.split(':')[0] == '客户代码':
                        order.clientcode = arr.split(':')[1]
                    elif arr.split(':')[0] == '剩余数量':
                        order.number_remain = (int)(arr.split(':')[1])
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
    analyze2()
