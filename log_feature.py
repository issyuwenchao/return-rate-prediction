# encoding=utf-8
import sys
from operator import itemgetter
import re
import os
import numpy as np
from datetime import datetime
from collections import defaultdict
from collections import Counter
from collections import OrderedDict

# Compute the time interval
def get_second(time_before, time_after):
    b1,b2,b3,b4 = time_before.split(':')
    a1,a2,a3,a4 = time_after.split(':')
    second = int(a4) - int(b4)
    minute = int(a3) - int(b3)
    hour = int(a2) - int(b2)
    return hour * 3600 + minute * 60 + second

# convert log file to nest lists
def get_log_list(log_path):
    log = open(log_path, 'r')
    log_list = []
    for line in log:
        log_list.append(line.strip().split(','))
    log.close()
    return log_list

# print the user click path of the same ida
def print_sequence(id_block):
    
    ida = id_block[0][0]
    result_seq = ida + ': ' + id_block[0][2]
    
    for i in range(1, len(id_block)):
        result_seq = result_seq + ' -(' + str(get_second(id_block[i-1][1], id_block[i][1]))+ 'sec)-> ' + id_block[i][2]
    print result_seq

# process the log block with same ida
def same_id_block(id_block, file_date):
    
    # eliminate invalid date
    new_id_block = []
    for i in range(len(id_block)):
        date = datetime.strptime(id_block[i][1], '%d/%b/%Y:%H:%M:%S')
        year_mon_day = date.strftime('%Y%m%d')
        if year_mon_day == file_date:
            new_id_block.append(id_block[i])

    if new_id_block:
        id_block = np.array(new_id_block)
        one_record = []
        
        # ida
        one_record.append(id_block[0][0])
        
        # date
        one_record.append(file_date)
        
        # iPhone model
        model = np.unique(id_block[:,4])
        if len(model) <> 1:
            print 'Warrning: more than 1 model occurs in a sequence.'
            print model
        one_record.append(model[0])

        # average server response time
        avg_time = np.mean([float(i) for i in id_block[:,5]])
        one_record.append('{0:.4f}'.format(avg_time))

        # from app
        app = np.unique(id_block[:,3])
        if len(app) <> 1:
            print 'Warrning: more than 1 app occurs in a sequence.'
            print app
        one_record.append(app[0])
        
        # sequence length
        one_record.append(len(id_block))

        actions = id_block[:,2]

        # is picture edit
        if 'CasePic' in actions:
            one_record.append(1)
        else:
            one_record.append(0)

        # is buy click
        if 'CaseBuy' in actions:
            one_record.append(1)
        else:
            one_record.append(0)

        # is order click
        if 'CaseOrder' in actions:
            one_record.append(1)
        else:
            one_record.append(0)

        case_num = defaultdict(int)
        for action in actions:
            case_num[action] += 1

        # Case3D number
        one_record.append(case_num['Case3D'])

        # CasePic number
        one_record.append(case_num['CasePic'])

        # CaseBuy number
        one_record.append(case_num['CaseBuy'])

        # CaseOrder number
        one_record.append(case_num['CaseOrder'])

        # CaseEnter number
        one_record.append(case_num['CaseEnter'])

        # CasePic/CaseBuy co-occurance
        if min(case_num['CasePic'], case_num['CaseBuy']) == 0:
            one_record.append(0)
        else:
            one_record.append(1)

        # CasePic/CaseOrder co-occurance
        if min(case_num['CasePic'], case_num['CaseOrder']) == 0:
            one_record.append(0)
        else:
            one_record.append(1)

        # operation average time (smaller than 10 mins)
        time_interval = []
        for i in range(1, len(id_block)):
            time_interval.append(get_second(id_block[i-1][1], id_block[i][1]))
            
            # detect invalid logs
            if get_second(id_block[i-1][1], id_block[i][1]) < 0:
                print (id_block[i-1][1], id_block[i][1])

        adjust_interval = [i for i in time_interval if 0 < i < 600]

        if adjust_interval:
            one_record.append('{0:.2f}'.format(np.mean(adjust_interval)))
        else:
            one_record.append(0)

        # 编辑的停留时间 edit time
        # 填写订单的时间 buy time
        # 相同用户出现次数 sequence number
        
        return one_record
    else:
        return []

# ida, time, pagename, app, model, respond
def single_log_feature(log_list, file_date):
    
    # all unique ida records in a single file
    records = []
    
    tmp_block = []
    ida = log_list[0][0]
    for i in range(len(log_list)):
        if log_list[i][0] == ida:
            tmp_block.append(log_list[i])
        else:
            one_record = same_id_block(tmp_block, file_date)
            if one_record:
                records.append(one_record)
            ida = log_list[i][0]
            tmp_block = []
            tmp_block.append(log_list[i])

    # last block
    one_record = same_id_block(tmp_block, file_date)
    if one_record:
        records.append(one_record)
    return records

# print the log feature
def print_log_feature(log_feature_list, lines):
    label = ['ida', 'date', 'model', 'avg_respond', 'from_app', \
             'seq_length', 'is_edit', 'is_buy', 'is_order', 'case_3d', \
             'case_pic', 'case_buy', 'case_order', 'case_enter', \
             'case_pic_buy', 'case_pic_order', 'avg_oper_time']
    for i in range(lines):
        for j in range(len(label)):
            print '{:>15} {:<12}'.format(label[j], log_feature_list[i][j])
        print '-' * 30

def get_column_statistic(records, index):
    one_column = np.array(records)[:,index]
    unique = Counter(one_column)
    sort_unique = OrderedDict(sorted(unique.items()))
    # Debug info
    for item in sort_unique:
        print item, sort_unique[item]
    return len(unique)

def model_feature(model):
    options = {
        'iphone3' : [1, 0, 0, 0, 0],
        'iphone4' : [0, 1, 0, 0, 0],
        'iphone5' : [0, 0, 1, 0, 0],
        'iphone6' : [0, 0, 0, 1, 0],
    }
    if model in options:
        return options[model]
    else:
        return [0, 0, 0, 0, 1]

def app_feature(app):
    options = {
        '1P_ThemeWallpapers'   : [1, 0, 0, 0, 0, 0],
        '9P_RetinaWallpapers'  : [0, 1, 0, 0, 0, 0],
        '9P_iOS7Wallpapershd'  : [0, 0, 1, 0, 0, 0],
        '9P_iPhone5Wallpapers' : [0, 0, 0, 1, 0, 0],
        'AR_XianYouAnswer'     : [0, 0, 0, 0, 1, 0],
    }
    if app in options:
        return options[app]
    else:
        return [0, 0, 0, 0, 0, 1]

def log_feature_discretize(records, file_date):
    
    #print_log_feature(records, 1)
    
    final_log_feature = []
    for i in range(len(records)):
        log_feature = []
        # ida
        log_feature.append(records[i][0])
        
        # model
        log_feature.extend(model_feature(records[i][2]))
        
        # respond time
        log_feature.append(records[i][3])
        
        # from app
        log_feature.extend(app_feature(records[i][4]))
        
        # the rest
        log_feature.extend(records[i][5:])
        
        final_log_feature.append(log_feature)

    if final_log_feature:
        #if not os.path.exists('log_feature/'):
        #    os.makedirs('log_feature/')
        np.savetxt('/Users/wenchao/Developer/OnlinePredict/log_feature/'+file_date+'.txt', np.array(final_log_feature), delimiter = ',', fmt = '%s')
        print '>> day: %s feature generated.' % (file_date)

    return final_log_feature

# Walk through the data dir
def log_feature_walk_dir(dirname):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            file_date = name.split('.')[0]
            if file_date.isdigit():
                log_list = get_log_list(path)
                records = single_log_feature(log_list, file_date)
                log_feature_discretize(records, file_date)
        else:
            log_feature_walk_dir(path)

def test_log_feature(parsing_result_path, file_date):
    test_log_list = get_log_list(parsing_result_path)
    one_record = []
    one_record.append(same_id_block(test_log_list, file_date))
    log_feature = log_feature_discretize(one_record, 'test_log_feature')
    return log_feature

if __name__ == '__main__':
    
    data_path = 'data/nginx_logs/'
    year = '2013/'
    month = '12/'
    path = data_path + year + month +'access.log.20131231'
    
    single_day_log(path)
    cwd = os.getcwd()
