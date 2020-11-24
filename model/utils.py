
import os
import time

base_path = 'data'
base_log_path = 'log'
error_list = list()
error_codes = list()

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_code_str(code):
    code = str(code)
    code_prefix = code[:3]

    sh = ['600', '601', '603', '605', '688']
    sz = ['000', '002', '300']

    code_str = ''
    if code_prefix in sh:
        code_str = "sh{}".format(code)
    elif code_prefix in sz:
        code_str = "sz{}".format(code)
    
    return code_str

def count_num(number, total_price, price, multiple):

    print(number, total_price, price, multiple)
    res = (float(number) * float(multiple) / 2) / float(total_price) * float(price)
    return round(res, 3)

def check_file(file_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('代码,股票,2020年,2021年,2022年,增速1,增速2,增速3,总市值,股价,低,中,高,PE,空间,预期差,相关行业 \n')

def save_data(data):
    save_name = '{}.csv'.format(time.strftime('%Y-%m-%d'))
    save_path = os.path.join(base_path, save_name)
    check_file(file_path=save_path)
    with open(save_path, 'a+') as f:
        f.write(data)
        f.write('\n')

def check_log_file(file_path):
    if not os.path.exists(base_log_path):
        os.makedirs(base_log_path)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass

def add_log(log_text, code, multiple=25):
    error_list.append(log_text)
    error_codes.append('{},{}'.format(code, multiple))
    write_log(data=log_text)

def write_log(data):
    save_name = '{}.log'.format(time.strftime('%Y-%m-%d'))
    save_path = os.path.join(base_log_path, save_name)
    check_log_file(file_path=save_path)
    with open(save_path, 'a+') as f:
        f.write(data)
        f.write('\n')




class NotCodeException(Exception):
    def __str__(self):
        return '{} [当前股票代码并未维护]'.format(time.strftime('%Y-%m-%d %H:%M:%S'))