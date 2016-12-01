# coding: utf-8
'''
Created on 2015-11-25

@author: Administrator
'''
import csv,os
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from datetime import *




def handledata():
    
    nowyear = '2016'
    rootdir = 'E:\Users\ct\workspace\pyctpmaster\src\example\info\data'
    date = '20160929'
    for f in os.listdir(rootdir):  
        foler = os.path.join(rootdir, f)  
        instrument = foler.split("\\")[-1].split(".")[0]
        for ff in os.listdir(foler): 
            ffile = os.path.join(foler, ff)  
            filename = ffile.split("\\")[-1].split(".")[0]
            
            if os.path.isfile(ffile) and filename == date:   
                
                print '原始文件:'+ffile
                
                csvfile = file(ffile,'rb') 
                reader = csv.reader(csvfile)
                
                tocsvfile = file(date+instrument+'.csv', 'wb')
                writer = csv.writer(tocsvfile)
                
            #     writer = csv.writer(file(filename, 'wb'))
                 
                writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close','bidvol','askvol'])
                #TICK_FORMAT = '{0.time},{0.msec},{0.price:.%(flen)df},{0.high:.%(flen)df},{0.low:.%(flen)df},{0.dvolume},{0.damount},{0.holding},{0.bid_price:.%(flen)df},{0.bid_volume},{0.ask_price:.%(flen)df},{0.ask_volume}\n'
                for line in reader:
                    date_oldformat = nowyear+'0'+line[0]+'.'+line[1] #1125103001  517
                    print date_oldformat
            #         date_oldformat = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
                    year = int(date_oldformat[0:4])
                    month = int(date_oldformat[4:6])
                    day = int(date_oldformat[6:8])
                    hour = int(date_oldformat[8:10])
                    minute = int(date_oldformat[10:12])
                    second = int(date_oldformat[12:14])
                    microsecond = int(date_oldformat[15:])*1000
                    ret = datetime(year, month, day,hour,minute,second,microsecond)
                    __barTime = ret.strftime('%Y%m%d %H:%M:%S.%f')
                    barTime = __barTime[0:len(__barTime)-3]
                    
                    
                    open = line[8]
                    high = line[3]
                    low = line[4]
                    close = line[10]
                    volume = line[5]
                    adjclose = line[2]
                    bidvol = line[9]
                    askvol = line[11]
                    
                    writer.writerow([barTime,open,high,low,close,volume,adjclose,bidvol,askvol])
                    
                csvfile.close() 
                tocsvfile.close()
#         array = line.split(',')
#         time = array[0]+array[1]
#         writer.writerow(['姓名', '年龄', '电话'])
#         print time
        
    
                
                
#             data_lines = data.getDayData(instrumentID,file) #获取数据
#             data_config = conf.getInstrumentInfo(instrumentID) 
#             csvfile = filename + instrumentID +'.csv'
# #             res=StoreCsv.process(data_lines,data_config,csvfile,malength=90)
#             data_lines=StoreCsv4Nticket.process(data_lines,data_config,csvfile,malength=90)
            
    
    
    
    print 'end'
    
    

if __name__=="__main__": handledata()
