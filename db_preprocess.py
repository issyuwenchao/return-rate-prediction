# encoding=utf-8
import sys
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
from collections import OrderedDict
from datetime import datetime
from basics import which_model
from basics import valid_app
from basics import valid_province
from basics import valid_express

code = sys.getfilesystemencoding()

# function for demo.py
def get_one_db_order(db_path, index):
    db = open(db_path, 'r')
    db_list = []
    for line in db:
        db_list.append(line.strip().split(','))
    db.close()
    return db_list[index]

# convert db file to nest lists
def get_db_list(db_path):
    db = open(db_path, 'r')
    db_list = []
    for line in db:
        db_list.append(line.strip().split(','))
    db.close()
    return db_list

# [类标]：货到付款（id 50）／ 货到拒收（id 51）
# [ida, 创建时间, 手机壳类型, 商品数目, 商品单价, app来源, 省份, 地址长度, 快递, 是否有用户备注]
# 手机号与地区是否匹配; 下订单次数 拒收次数 付钱次数 编辑次数 Case3D数目

feature_name = ['label', 'ida', 'time', 'model', 'total', 'price', \
                'app', 'province', 'addr', 'express', 'note']

def feature_extraction(db_list):
    
    # db_list = db_list[:3]
    
    rows = len(db_list)
    feature_list = []
    dict_list = []
    
    for i in range(rows):
        one_log = db_list[i]
        dict_log = dict()
        
        # model
        model = which_model(one_log[5])
        dict_log['model'] = model
        
        #total
        dict_log['total'] = int(one_log[6])
        
        #price
        if one_log[7].isdigit():
            dict_log['price'] = int(one_log[7])
        else:
            dict_log['price'] = 0

        #app
        app = valid_app(one_log[9])
        dict_log['app'] = app

        #province
        province = valid_province(one_log[10])
        dict_log['province'] = province
        
        #addr
        dict_log['addr'] = int(one_log[11])
        
        #express
        express = valid_express(one_log[12])
        dict_log['express'] = express
        
        #note
        if one_log[14]:
            dict_log['note'] = 'yes'
        else:
            dict_log['note'] = 'no'
        
        dict_list.append(dict_log)
    
    vec = DictVectorizer()
    feature_matrix = vec.fit_transform(dict_list).toarray()
    
    #print vec.get_feature_names()
    #print len(vec.get_feature_names())
    
    for i in range(rows):
        feature_vec = []
        one_log = db_list[i]
        
        # label: order_status
        if one_log[2] == '50':
            feature_vec.append(0)
        elif one_log[2] == '51':
            feature_vec.append(1)
        else:
            feature_vec.append(2)
        
        # ida
        feature_vec.append(one_log[1])
        
        # time
        feature_vec.append(datetime.utcfromtimestamp(int(one_log[3])))

        feature_vec.extend(feature_matrix[i])
        feature_list.append(feature_vec)
    
    return feature_list

def feature_extraction_order(db_list, order):
    
    db_list.append(order)
    
    rows = len(db_list)
    feature_list = []
    dict_list = []
    
    for i in range(rows):
        one_log = db_list[i]
        dict_log = dict()
        
        # model
        model = which_model(one_log[5])
        dict_log['model'] = model
        
        #total
        dict_log['total'] = int(one_log[6])
        
        #price
        if one_log[7].isdigit():
            dict_log['price'] = int(one_log[7])
        else:
            dict_log['price'] = 0
        
        #app
        app = valid_app(one_log[9])
        dict_log['app'] = app
        
        #province
        province = valid_province(one_log[10])
        dict_log['province'] = province
        
        #addr
        dict_log['addr'] = int(one_log[11])
        
        #express
        express = valid_express(one_log[12])
        dict_log['express'] = express
        
        #note
        if one_log[14]:
            dict_log['note'] = 'yes'
        else:
            dict_log['note'] = 'no'
        
        dict_list.append(dict_log)
    
    vec = DictVectorizer()
    feature_matrix = vec.fit_transform(dict_list).toarray()
    
    #print vec.get_feature_names()
    #print len(vec.get_feature_names())
    
    for i in range(rows):
        feature_vec = []
        one_log = db_list[i]
        
        # label: order_status
        if one_log[2] == '50':
            feature_vec.append(0)
        elif one_log[2] == '51':
            feature_vec.append(1)
        else:
            feature_vec.append(2)
        
        # ida
        feature_vec.append(one_log[1])
        
        # time
        feature_vec.append(datetime.utcfromtimestamp(int(one_log[3])))
        
        feature_vec.extend(feature_matrix[i])
        feature_list.append(feature_vec)
    
    return feature_list[-1]


label = ['order id','ida','order_status','created utc','goods id',\
        'goods name','item num','item price','total price','from app','addr', \
        'addr length','express','?','user memo','auditor memo','request']

def db_result(db_path):
    f = open(db_path, 'r')

    debug = 0

    for line in f:
        debug += 1
        if debug == 10:
            break
        one_db = line.split(',')
        label = ['order id','unique ida','order status','created utc','goods id',\
                 'goods name','item num','item price','total price','from app','address', \
                 'addr length','express','unknown','user memo','auditor memo','request']
        for i in range(len(one_db)):
            if i == 3:
                print '%d\t%s:\t\t %s' % (i, label[i], datetime.utcfromtimestamp(int(one_db[i])))
            if i == 5:
                model = which_model(one_db[i])
                print '%d\t%s:\t\t %s \t %s' % (i, label[i], model, one_db[i].decode('utf-8').encode(code))
            if i == 9:
                app = valid_app(one_db[i])
                print '%d\t%s:\t\t %s \t %s' % (i, label[i], app, one_db[i].decode('utf-8').encode(code))
            if i == 10:
                province = valid_province(one_db[i])
                print '%d\t%s:\t\t %s \t %s' % (i, label[i], province, one_db[i].decode('utf-8').encode(code))
            
             
            else:
                print '%d\t%s:\t\t %s' % (i, label[i], one_db[i].decode('utf-8').encode(code))

    return debug

def city_feature(city):
    return 0

# call this function only once!!!
def get_total_city():
    return 0
def express_feature(express, total):
    return 0

# get one column in the database
def get_one_column(db_path, index):
    f = open(db_path, 'r')
    one_column = []
    for line in f:
        one_column.append(line.split(',')[index])
    f.close()
    return one_column

# call this function only once!!!
def get_column_statistic(db_path, index):
    one_column = get_one_column(db_path, index)

    unique = Counter(one_column)


    sort_unique = OrderedDict(sorted(unique.items()))
    # Debug info
    for c in sort_unique:
        #print datetime.utcfromtimestamp(int(c))
        print c.decode('utf-8').encode(code), sort_unique[c]
    #unique = set()
    #for express in express_list:
    #    unique.add(express)
    return len(unique)

def model_feature(model):
    case_type = model.split(' ')
    options = {
            '彩绘' : (1, 0, 0),
            '磨砂' : (0, 1, 0),
            '浮雕' : (0, 0, 1),
    }
    return options[case_type[len(case_type)-1]]

if __name__ == '__main__':
    
    db_path = 'parsing/db_pay_rej.txt'
    db_list = get_db_list(db_path)
    
    feature_name = ['label', 'ida', 'time', 'model', 'total', 'price', \
                    'app', 'province', 'addr', 'express', 'note']
    feature_extraction(db_list, feature_name)
    
    db_result(db_path)
    #print model_feature('彩绘')
    items = get_one_column(db_path, 2)
    #for item in items:
    #    print item.decode('utf-8').encode(code)
    print get_total_express(db_path)


