#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sched, time, datetime
from threading import Thread, Timer
from tradeanalyze import dailytask

s = sched.scheduler(time.time, time.sleep)

def each_day_time(hour, min, sec):
    struct = time.localtime()
    # if next_day:
    #     day = struct.tm_mday + 1
    # else:
    #     day = struct.tm_mday

    return time.mktime((struct.tm_year,struct.tm_mon,struct.tm_mday,
        hour,min,sec,struct.tm_wday, struct.tm_yday,
        struct.tm_isdst))
    
def subProcessThread():
    keepWorking  = readConfigFile('begin')
    print keepWorking
    if keepWorking == "1":
        Timer(3600 * 24, subProcessThread, ()).start()#每隔一天执行一次
        print_time()

def print_time():
    print  "From print_time",\
        time.time()," :", time.ctime()
    dailytask.dodailywork()
    

def readConfigFile(name):
    filename = "configFile.txt"
    config = open(filename)
    for line in  config.readlines():
        print line
        if  name in line:
            return line.split('=')[1]
    return ''

def main():
    # customTime = each_day_time(18, 11, 0)
    # datetime = datetime.str
    struct = time.localtime()
    arrs = readConfigFile('starttime')[0:8].split(':')
    print arrs
    print arrs[0]+arrs[1]+arrs[2]
    customTime = time.mktime((struct.tm_year,struct.tm_mon,struct.tm_mday,
        (int)(arrs[0]),(int)(arrs[1]),(int)(arrs[2]),struct.tm_wday, struct.tm_yday,
        struct.tm_isdst))
    # current = '20151004 09:00:00'#str(struct.tm_year) + str(struct.tm_mon) + str(struct.tm_mday) + readConfigFile('datetime')
    # customTime = datetime.datetime.strptime(current,'%Y%m%d %H:%M:%S')
    print customTime
    s.enterabs(customTime, 1, subProcessThread, ())
    s.run()

    #2. delay
    # while(True):
    #     print "second task"
    #     Timer(0, do_somthing, ()).start()
    #     time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    main()