import numpy as np
import pylab as pl

from sklearn.linear_model import LogisticRegression
from sklearn import datasets, preprocessing
from sklearn.preprocessing import StandardScaler
from collections import namedtuple
from sklearn.ensemble import GradientBoostingClassifier

from operator import itemgetter

def rate_predict(train, train_label, test, test_label):
    
    train_sample = len(train)
    
    data = train;
    data.extend(test);
    
    #print len(train[0]), len(test),test
    min_max = preprocessing.MinMaxScaler()
    
    data_scaled = min_max.fit_transform(data)
    #data_scaled = preprocessing.scale(data)
    
    train = data_scaled[:train_sample]
    test = data_scaled[train_sample:]
    
    #print test and train numbers
    print '[Predict] training samples: %d, testing samples: %d' % (len(train), len(test))


    # Set regularization parameter
    # for i, C in enumerate(10. ** np.arange(1, 4)):
    for i, C in enumerate(10. ** np.arange(2, 3)):
        # turn down tolerance for short training time
        clf_l1_LR = LogisticRegression(C=C, penalty='l1', tol=0.01, class_weight={0:1, 1:5})#class_weight='auto')
        clf_l2_LR = LogisticRegression(C=C, penalty='l2', tol=0.01, class_weight='auto')
        clf_l1_LR.fit(train, train_label)
        clf_l2_LR.fit(train, train_label)
        
        coef_l1_LR = clf_l1_LR.coef_.ravel()
        coef_l2_LR = clf_l2_LR.coef_.ravel()
        
        # coef_l1_LR contains zeros due to the
        # L1 sparsity inducing norm
        
        sparsity_l1_LR = np.mean(coef_l1_LR == 0) * 100
        sparsity_l2_LR = np.mean(coef_l2_LR == 0) * 100
        
        #print("C=%d" % C)
        #print("Sparsity with L1 penalty: %.2f%%" % sparsity_l1_LR)
        #print("score with L1 penalty: %.4f" % clf_l1_LR.score(test, test_label))
        #print("Sparsity with L2 penalty: %.2f%%" % sparsity_l2_LR)
        print('[Predict] Score with L2 penalty: %.4f' % clf_l2_LR.score(test, test_label))

        result = clf_l2_LR.predict(test)
        predict_result = clf_l2_LR.predict_proba(test)
        
        rej_precision_recall(test_label, predict_result)
        
        pay_to_pay = 0;
        pay_to_rej = 0;
        rej_to_rej = 0;
        rej_to_pay = 0;

        for i in range(len(result)):
            if test_label[i] == 0 and result[i] == 0:
                pay_to_pay += 1;
            if test_label[i] == 0 and result[i] == 1:
                pay_to_rej += 1;
            if test_label[i] == 1 and result[i] == 0:
                rej_to_pay += 1;
            if test_label[i] == 1 and result[i] == 1:
                rej_to_rej += 1;

        #Row = namedtuple('Row',['status','pay','rej'])
        #data1 = Row('pay', pay_to_pay, pay_to_rej)
        #data2 = Row('rej', rej_to_pay, rej_to_rej)

        #pprinttable([data1, data2])

        print '-' * 19
        print '|     | pay | rej |'
        print '------+-----+------'
        #print '| pay | %d | %d |' % (pay_to_pay, pay_to_rej)
        print '| pay | {:<4}| {:<4}|'.format(pay_to_pay, pay_to_rej)
        print '------+-----+------'
        #print '| rej | %d   | %d  |' % (rej_to_pay, rej_to_rej)
        print '| rej | {:<4}| {:<4}|'.format(rej_to_pay, rej_to_rej)
        print '-' * 19
       
    return predict_result



def rej_precision_recall(true_label, predict_result):
    
    predict_result[:,0] = true_label
    rank_array = predict_result.tolist()
    rank_array = sorted(rank_array, key=itemgetter(1), reverse=True)
    precision = []
    recall = []
    print np.array(rank_array)[:,0]
    
    total = len(rank_array)
    total_rej_in_array = 0
    for i in range(total):
        if rank_array[i][0] == 1:
            total_rej_in_array = total_rej_in_array + 1;

    if total_rej_in_array <> 0:
        total_rej = 0
        for i in range(total):
            if rank_array[i][1] >= 0:
                if rank_array[i][0] == 1:
                    total_rej = total_rej + 1;
                    precision.append(total_rej/(i+1.0))
                    recall.append(total_rej/float(total_rej_in_array))
                else:
                    precision.append(total_rej/(i+1.0))
                    recall.append(total_rej/float(total_rej_in_array))
        print '[Predict] Precision list:'
        print ' '.join('%.2f' % i for i in precision )
        print '[Predict] Recall list:'
        print ' '.join('%.2f' % i for i in recall )

def pprinttable(rows):
    if len(rows) > 1:
        headers = rows[0]._fields
        lens = []
        for i in range(len(rows[0])):
            lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
        formats = []
        hformats = []
        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            hformats.append("%%-%ds" % lens[i])
        pattern = " | ".join(formats)
        hpattern = " | ".join(hformats)
        separator = "-+-".join(['-' * n for n in lens])
        print hpattern % tuple(headers)
        print separator
        for line in rows:
            print pattern % tuple(line)
    elif len(rows) == 1:
        row = rows[0]
        hwidth = len(max(row._fields,key=lambda x: len(x)))
        for i in range(len(row)):
            print "%*s = %s" % (hwidth,row._fields[i],row[i])

if __name__ == '__main__':
    train = 0
    train_label = 0
    test = 0
    test_label = 0
    rate_predict(train, train_label, test, test_label)

