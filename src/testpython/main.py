#!/usr/bin/python
#-*- coding=utf-8 -*-
"This is the main demo file"

import sys,os
import conf,data,process

def main():
    #get data from .zip
    instrumentID = "IF1406"
    date = "20131218"
    data_path = "D:\pyTest_yh\data"  # yh： 没有用了
    data_lines = data.getDayData(date, instrumentID,data_path) #获取数据
    data_config = conf.getInstrumentInfo(instrumentID) 
    #获取合约乘数self.VolumeMultiple 和最小变动价位self.PriceTick
    alldata=process.process(data_lines,data_config)
    
    


if __name__=="__main__":
    main()
