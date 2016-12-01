# coding: utf-8
'''
Created on 2015-11-25

@author: Administrator
'''
import csv,os
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from datetime import *
from boto.dynamodb.condition import NULL




def handledata():
    
#     nowyear = '2016'
    rootdir = 'E:\historymarket\\'
    date = '20160720'
    instrument = ''
    for f in os.listdir(rootdir + date):  
#         foler = os.path.join(rootdir + date, f)  
#         instrument = foler.split("\\")[-1].split(".")[0]
#         for ff in os.listdir(foler): 
            ffile = os.path.join(rootdir + date, f)  
            filename = ffile.split("\\")[-1].split(".")[0]
            print 'filename'+filename
            print filename.index(date)
            print os.path.isfile(ffile)
            if os.path.isfile(ffile) and filename.index(date) > 0:   
                
                print '原始文件:'+ffile
                
                csvfile = file(ffile,'rb') 
                reader = csv.reader(csvfile)
                instrument = filename[:filename.index('_')]
                print instrument
                tocsvfile = file(date+instrument+'.csv', 'wb')
                writer = csv.writer(tocsvfile)
                
            #     writer = csv.writer(file(filename, 'wb'))
                 
                writer.writerow(['Date', 'Open', 'High','Low','Close','Volume','Adj Close','bidvol','askvol'])
                #TICK_FORMAT = '{0.time},{0.msec},{0.price:.%(flen)df},{0.high:.%(flen)df},{0.low:.%(flen)df},{0.dvolume},{0.damount},{0.holding},{0.bid_price:.%(flen)df},{0.bid_volume},{0.ask_price:.%(flen)df},{0.ask_volume}\n'
                i = 0
                tempdate = ''
                for line in reader:
                    if i == 0:
                        i += 1
                        continue
                    if line is NULL or len(line) == 0 or line == '':
                        print 'end'
                        break
                    print 'line'+line[0]
                    
                    date_oldformat = line[0]+ line[1]+'.'+ '000'#1125103001  517
                    print ''+date_oldformat+' '+tempdate
                    if date_oldformat == tempdate:
                        date_oldformat = line[0] + line[1]+'.'+ '500'
                    tempdate = date_oldformat
                    print date_oldformat
            #         date_oldformat = str(line.TradingDay)+' '+str(line.UpdateTime)[0:8]+'.'+str(line.UpdateMillisec)
                    year = int(line[0].split('-')[0])
                    month = int(line[0].split('-')[1])
                    day = int(line[0].split('-')[2])
                    hour = int(line[1].split(':')[0])
                    minute = int(line[1].split(':')[1])
                    second = int(line[1].split(':')[2])
                    print date_oldformat[date_oldformat.index('.'):]+''
                    microsecond = int(date_oldformat[date_oldformat.index('.')+1:])*1000
                    print microsecond
                    ret = datetime(year, month, day,hour,minute,second,microsecond)
                    __barTime = ret.strftime('%Y%m%d %H:%M:%S.%f')
                    barTime = __barTime[0:len(__barTime)-3]
                    
                    
                    open = line[6]
                    high = line[2]
                    low = line[2]
                    close = line[12]
                    volume = line[3]
                    adjclose = line[2]
                    bidvol = line[7]
                    askvol = line[13]
                    
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
