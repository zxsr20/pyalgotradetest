#!/usr/bin/python
#-*- coding=utf-8 -*-
'''
Created on 2015-6-13

@author: ct
'''

import tradeanalyze



csvfilename = ''


RangeSpan = 'mydataplot4RangeSpan'#rangespan方法
drawbigupdown = 'mydataplot4drawbigupdown'#几种画大段的方法
macd = 'mydataplot4macd'#macd的一个策略
speedspread = 'mydataplot4speedspread'#在多少个ticket中上涨或下跌占比大于y
tongjiseg = 'mydataplot4tongjiseg'#统计各个容忍度的seg长度
WaveNticket = 'mydataplot4WaveNticket'#统计多个ticket合起来计算wave
WaveSeg = 'mydataplot4WaveSeg'#wave和seg的结合策略
OneSeg = 'mydatasplotOneSeg'#单seg的策略
WaveSMA = 'mydatatplot4WaveSMA'#wave和sma的结合
LeaveByWaveZ = 'mydataplot4LeaveByWaveZ'#wave策略，离场根据wavez方法
#mydataplot4Nticket参数，进行seg的比较



#策略参数配置
rootdir = 'D:\pyTest_yh\data\\'#数据文件位置
instrumentID = "rb1701"#"IF1509"#"diffm1509m1601"#"rb1510"#"SP m1509&m1601"#合约名称
date = '20160929'#zip文件名

realmarket_diff = 460


#twoseg策略
rongren1 = 5
rongren2 = 15
nticket = 1
nwaveticket = 6

#waveseg参数
waveseg_nwaveticket = 60
waveseg_y = 100
waveseg_x = 50
waveseg_rongren = 30

#leavebywavez参数
leavebywavez_nwaveticket = 60
leavebywavez_y = 60
leavebywavez_x = 50
leavebywavez_stoploss = 20

#wavesma参数
wavesma_nwaveticket = 60
wavesma_longsma = 50
wavesma_shortsma = 20
wavesma_y = 60
wavesma_x = 50


#rangespan参数
rangespan_nwaveticket = 30
# rangespan_ma = 100
# rangespan_range = 0.8 #所占面积比
# rangespan_span = 15 #》为趋势《为盘整

# rangespan_ma = 50
# rangespan_range = 0.9 #所占面积比
# rangespan_span = 40 #》为趋势《为盘整

rangespan_ma = 30
rangespan_range = 0.8 #所占面积比
rangespan_span = 3 #》为趋势《为盘整
 
rangespan_stoploss = 1 #止损跳数
rangespan_y = 0.5 #趋势下，如果价格大于范围+-y，入场
rangespan_n = 20 #n个周期没有创新高

# rangespan_ma = 200
# rangespan_range = 0.7 #所占面积比
# rangespan_span = 5 #》为趋势《为盘整
# 
# rangespan_stoploss = 10 #止损跳数
# rangespan_y = 5 #趋势下，如果价格大于范围+-y，入场
# rangespan_n = 50 #n个周期没有创新高


#wavediff
wavediff_instrumentID1 = 60
wavediff_instrumentID2 = 60
wavediff_nwaveticket1 = 60
wavediff_nwaveticket2 = 60
wavediff_wavetickets1 = []
wavediff_wavetickets2 = []


    


def main():
#     pass
    _cls_name = 'mydataplot4RangeSpan'#调用的策略名
    _packet_name = 'tradeanalyze.'+_cls_name  
    _module_home = __import__(_packet_name,globals(),locals(),[_cls_name])  
   
#     methodList = [method for method in dir(_module_home) if callable(getattr(_module_home,method))]
#     print methodList
    _module_home.main()
    
    
if __name__=="__main__": main()
