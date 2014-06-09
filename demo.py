# encoding=utf-8

import os
from predict import predict
from export_pay_rej import pay_rej
from db_preprocess import get_one_db_order

log_path = '/Users/wenchao/Developer/RatePrediction/data/nginx_logs/2014/03/access.log.20140331'
db_path = '/Users/wenchao/Developer/RatePrediction/data/research_refuse.gorders'
pay_rej_path = '/Users/wenchao/Developer/OnlinePredict/parsing/db_pay_rej.txt'
pay_rej(db_path, pay_rej_path, 'yes')
print 'Finished export the database log with label buy and reject'

order = get_one_db_order(pay_rej_path, 1)
print order

predict(log_path, order)

