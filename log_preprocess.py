from operator import itemgetter
import re
import sys
import os
import numpy as np

def single_day_log(path):

    f = open(path, 'r')
    
    # log example
    # 127.0.0.1 - - [0.003] [28/Mar/2014:23:22:15 +0800]  "GET /statistic/setpageview?pagename=CaseEnter
    #   &goods_id=(null)&ida=4D52060A-40AA-45BE-A9E9-77BB33CB4DD6&deviceid=replaceudid&osn=iPhone%2520OS
    #   &idv=60D8D4E3-3FF5-470E-846A-483BDB3D0AED&osv=7%2E1&as=0&tz=8&jb=0&app=9P_iPhone5Wallpapers&lang=zh-Hans
    #   &mobclix=0&idvs=&model=iphone5%252C2&macaddr=020000000000&v=1%2E6&phonetype=iphone HTTP/1.0" 200  12 "-"
    #   "9P_iPhone5Wallpapers/1.6 (iPhone; iOS 7.1; Scale/2.00)"

    pattern1 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*&app=(?P<app>.+?)&.*ida=(?P<ida>.+?)&.*model=(?P<model>.+?)%.*")
    pattern2 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*ida=(?P<ida>.+?)&.*&app=(?P<app>.+?)&.*model=(?P<model>.+?)%.*")
    pattern3 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*&app=(?P<app>.+?)&.*ida=(?P<ida>.+?)&.*")
    pattern4 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*ida=(?P<ida>.+?)&.*&app=(?P<app>.+?)&.*")

    log_for_sort = []
    valid_log = '/statistic/setpageview?pagename'
     
    for line in f:
        # Find legal log without null ida
        if valid_log in line and ('&ida=&' not in line):
            result1 = pattern1.search(line)
            result2 = pattern2.search(line)
            result3 = pattern3.search(line)
            result4 = pattern4.search(line)
            
            if result1:
                log_for_sort.append([result1.group('ida'), result1.group('time'), result1.group('pagename'), \
                                     result1.group('app'), result1.group('model'), result1.group('second')])
            elif result2:
                log_for_sort.append([result2.group('ida'), result2.group('time'), result2.group('pagename'), \
                                     result2.group('app'), result2.group('model'), result2.group('second')])
            elif result3:
                log_for_sort.append([result3.group('ida'), result3.group('time'), result3.group('pagename'), \
                                     result3.group('app'), 'iphone0', result3.group('second')])
            elif result4:
                log_for_sort.append([result4.group('ida'), result4.group('time'), result4.group('pagename'), \
                                     result4.group('app'), 'iphone0', result4.group('second')])
            else:
                print 'ignore one illegal line.'

    log_for_sort = sorted(log_for_sort, key=itemgetter(0, 1, 2))
    
    if log_for_sort:
        filename = path.split('.')
        np.savetxt('parsing/'+filename[-1]+'.txt', np.array(log_for_sort), delimiter = ',', fmt = '%s')
        print 'day: %s finished.' % (filename[-1])

def single_day_log_ida(path, ida):
    
    f = open(path, 'r')
    
    # log example
    # 127.0.0.1 - - [0.003] [28/Mar/2014:23:22:15 +0800]  "GET /statistic/setpageview?pagename=CaseEnter
    #   &goods_id=(null)&ida=4D52060A-40AA-45BE-A9E9-77BB33CB4DD6&deviceid=replaceudid&osn=iPhone%2520OS
    #   &idv=60D8D4E3-3FF5-470E-846A-483BDB3D0AED&osv=7%2E1&as=0&tz=8&jb=0&app=9P_iPhone5Wallpapers&lang=zh-Hans
    #   &mobclix=0&idvs=&model=iphone5%252C2&macaddr=020000000000&v=1%2E6&phonetype=iphone HTTP/1.0" 200  12 "-"
    #   "9P_iPhone5Wallpapers/1.6 (iPhone; iOS 7.1; Scale/2.00)"
    
    pattern1 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*&app=(?P<app>.+?)&.*ida=(?P<ida>.+?)&.*model=(?P<model>.+?)%.*")
    pattern2 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*ida=(?P<ida>.+?)&.*&app=(?P<app>.+?)&.*model=(?P<model>.+?)%.*")
    pattern3 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*&app=(?P<app>.+?)&.*ida=(?P<ida>.+?)&.*")
    pattern4 = re.compile(r".* \[(?P<second>.+?)\] \[(?P<time>.+?) .*pagename=(?P<pagename>.+?)&.*ida=(?P<ida>.+?)&.*&app=(?P<app>.+?)&.*")
    
    log_for_sort = []
    valid_log = '/statistic/setpageview?pagename'
    
    for line in f:
        # Find legal log without null ida
        if valid_log in line and ('&ida=&' not in line) and line.find(ida) != -1:
            result1 = pattern1.search(line)
            result2 = pattern2.search(line)
            result3 = pattern3.search(line)
            result4 = pattern4.search(line)
            
            if result1:
                log_for_sort.append([result1.group('ida'), result1.group('time'), result1.group('pagename'), \
                                     result1.group('app'), result1.group('model'), result1.group('second')])
            elif result2:
                log_for_sort.append([result2.group('ida'), result2.group('time'), result2.group('pagename'), \
                                     result2.group('app'), result2.group('model'), result2.group('second')])
            elif result3:
                log_for_sort.append([result3.group('ida'), result3.group('time'), result3.group('pagename'), \
                                     result3.group('app'), 'iphone0', result3.group('second')])
            elif result4:
                log_for_sort.append([result4.group('ida'), result4.group('time'), result4.group('pagename'), \
                                     result4.group('app'), 'iphone0', result4.group('second')])
            else:
                print 'ignore one illegal line.'
    
    log_for_sort = sorted(log_for_sort, key=itemgetter(0, 1, 2))
    
    if log_for_sort:
        filename = path.split('.')
        np.savetxt('/Users/wenchao/Developer/OnlinePredict/parsing/test_log.txt', np.array(log_for_sort), delimiter = ',', fmt = '%s')
        print 'day: %s finished.' % (filename[-1])


# Walk through the data dir
def walk_dir(dirname):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            print path
            single_day_log(path)
        else:
            walk_dir(path)

if __name__ == '__main__':

    data_path = 'data/nginx_logs/'
    year = '2013/'
    month = '12/'
    path = data_path + year + month +'access.log.20131231'
    
    single_day_log(path)
    cwd = os.getcwd()
    #walk_dir(cwd)
    #print get_second('28/Mar/2014:15:05:36', '28/Mar/2014:15:06:00')


