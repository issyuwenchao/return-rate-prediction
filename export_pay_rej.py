
# export the pay (id=50) and reject (id=51) lines in database
def pay_rej(db_path, pay_rej_path, with_cancel):
    f = open(db_path, 'r')
    fout = open(pay_rej_path, 'w+')
    
    order_status_idx = 2
    
    reject = '51'
    pay = '50'
    wait_confirm = '0'
    invalid = '11'
    wait_pay = '13'
    cancel = '14'
    
    count = 0
    
    for line in f:
        line_array = line.split(',')
        order_status = line_array[order_status_idx]
        if with_cancel == 'yes':
            if order_status in [reject, wait_confirm, invalid, wait_pay, cancel]:
                #line_array[order_status_idx] = reject;
                #line = ','.join(line_array)
                fout.write(line)
                count += 1
            elif order_status == pay:
                fout.write(line)
                count += 1
        elif order_status == pay or order_status == reject:
                fout.write(line)
                count += 1
    print '%d lines of pay and reject logs' % (count)

    f.close()
    fout.close()

if __name__ == '__main__':
    
    db_path = 'data/research_refuse.gorders'
    pay_rej_path = 'parsing/db_pay_rej.txt'
    pay_rej(db_path, pay_rej_path, 'yes')
