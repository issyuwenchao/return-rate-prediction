from operator import itemgetter
import numpy as np
import os
from datetime import datetime
from log_feature import get_log_list

def match_day(db_day, file_date):
    
    # determine the existence of file_date
    db_day_feature = []
    log_feature_file = 'log_feature/' + file_date + '.txt'
    if os.path.isfile(log_feature_file) and len(db_day):
        print 'processing day: %s' % file_date
        
        # unique ida
        db_day = sorted(db_day, key=itemgetter(1))
        new_db_day = []
        ida = db_day[0][1]
        new_db_day.append(db_day[0])
        
        for i in range(1, len(db_day)):
            if db_day[i][1] == db_day[i-1][1]:
                print 'dupicated ida in db in a single day: ida %s day %s.' % (db_day[i][1], db_day[i][2])
                continue
            else:
                new_db_day.append(db_day[i])
    
        # begin match algorithm
        log_day = get_log_list(log_feature_file)

        log_ida = np.array(log_day)[:,0]
        db_ida = np.array(new_db_day)[:,1]
        
        common_ida = list(set(log_ida) & set(db_ida))
        print '-' * 40
        print 'Statistics: in day %s, log num %d, db num %d, match num %d.' \
              % (file_date, len(log_ida), len(db_ida), len(common_ida))
        
        if common_ida:
            
            # get common ida index
            log_idx_dict = dict((m,n) for n,m in enumerate(log_ida))
            log_idx = [log_idx_dict[x] for x in common_ida]
            
            db_idx_dict = dict((m,n) for n,m in enumerate(db_ida))
            db_idx = [db_idx_dict[x] for x in common_ida]
            
            # extend feature with same ida
            for k in range(len(common_ida)):
                if log_ida[log_idx[k]] == db_ida[db_idx[k]]:
                    db_match_record = new_db_day[db_idx[k]]
                    log_match_record = log_day[log_idx[k]]
                    match_record = db_match_record
                    
                    # string to float
                    match_record.extend([float(i) for i in log_match_record[1:]])
                    
                    db_day_feature.append(match_record)
                else:
                    print 'error in file match_db_log.py module match_day'
            
            return db_day_feature
        else:
            return []

    else:
        return []

def log_date(db_date):
    date = datetime.strptime(str(db_date), '%Y-%m-%d %H:%M:%S')
    year_mon_day = date.strftime('%Y%m%d')
    return year_mon_day

def match_feature(feature_list, log_feature_path):

    feature_list_sort = sorted(feature_list, key=itemgetter(2, 1))
    
    final_feature = []
    db_day = []
    date = log_date(feature_list_sort[0][2])
    
    for i in range(len(feature_list_sort)):
        if log_date(feature_list_sort[i][2]) == date:
            db_day.append(feature_list_sort[i])
        else:
            db_day_feature = match_day(db_day, date)
            if db_day_feature:
                final_feature.extend(db_day_feature)
            date = log_date(feature_list_sort[i][2])
            db_day = []
            db_day.append(feature_list_sort[i])
            
    # last db day
    db_day_feature = match_day(db_day, date)
    if db_day_feature:
        final_feature.extend(db_day_feature)

    #np.savetxt('parsing/demo.txt', np.array(final_feature), delimiter = ',', fmt = '%s')
    return final_feature
