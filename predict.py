# encoding=utf-8
import os
import numpy as np
from db_preprocess import db_result
from db_preprocess import get_column_statistic
from db_preprocess import feature_extraction
from db_preprocess import feature_extraction_order
from db_preprocess import get_db_list
from rate_prediction import rate_predict
from log_preprocess import walk_dir
from log_preprocess import single_day_log_ida
from export_pay_rej import pay_rej
from log_feature import get_log_list
from log_feature import single_log_feature
from log_feature import log_feature_discretize
from log_feature import log_feature_walk_dir
from log_feature import test_log_feature
from match_db_log import match_feature
#from cross_validation import stat_ida_before_date

def predict(log_path, order):

    # step 1:
    db_path = '/Users/wenchao/Developer/RatePrediction/data/research_refuse.gorders'
    pay_rej_path = '/Users/wenchao/Developer/OnlinePredict/parsing/db_pay_rej.txt'
    #pay_rej(db_path, pay_rej_path, 'yes')
    print '(1/6) Finished export the database log with label buy and reject'

    # step 2:
    db_list = get_db_list(pay_rej_path)
    feature_list = feature_extraction(db_list)
    order_feature = feature_extraction_order(db_list, order)
    print '(2/6) Finished extract database feature'

    # step 3:
    #log_path = 'data/nginx_logs/'
    #walk_dir(log_path)
    single_day_log_ida(log_path, order_feature[1])
    print '(3/6) Finished parsing raw log'

    # step 4:
    parsing_result_path = '/Users/wenchao/Developer/OnlinePredict/parsing/test_log.txt'
    #log_feature_walk_dir(parsing_result_path)
    test_feature = test_log_feature(parsing_result_path, '20140331')
    print '(4/6) Finished extract log feature'

    # step 5:
    test_feature = [float(i) for i in test_feature[0][1:]]
    order_feature.extend(test_feature)
    print '(5/6) Finished match log and databese feature'

    # step 6:

    # Debug:
    final_feature = get_db_list('/Users/wenchao/Developer/RatePrediction/final_feature_with_cancel.txt')
    #print final_feature
    train = []
    train_label = []
    test = []
    test_label = []
    for i in range(len(final_feature)):
        train_label.append(int(final_feature[i][0]))
        train.append([float(m) for m in final_feature[i][3:]])
    
    test_label.append(order_feature[0])
    test.append(order_feature[3:])

    ret_rate = rate_predict(train, train_label, test, test_label)
    print ret_rate
    
    print '(6/6) Job done!'

    return ret_rate




