import os
import time
import selenium.webdriver.support.ui as ui


from model.utils import *
from model.exec_lib import *


def get_data(browser=None, url='', multiple=25):
    global error_list

    browser.get(url)
    ui.WebDriverWait(browser, 10)

    name = browser.find_element_by_xpath('/html/body/div[9]/div/h1/a[1]/strong').get_attribute("stockname")
    code = browser.find_element_by_xpath('/html/body/div[9]/div/h1/a[1]/strong').get_attribute("stockcode")

    if (name == None):
        nc_str = browser.find_element_by_xpath('/html/body/div[9]/div/h1/a[1]/strong')
        nc_list = nc_str.text.split('\n')
        name = nc_list[0]
        code = nc_list[1]


    browser.switch_to_frame('ifm')
    time.sleep(0.5)

    price = browser.find_element_by_xpath('//*[@id="hexm_curPrice"]')
    price = price.text

    total_price = browser.find_element_by_xpath('//*[@id="tvalue"]')
    total_price = total_price.text

    browser.switch_to_default_content()
    browser.switch_to_frame('dataifm')

    # 业绩预测年份获取
    yjyc_years = browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[2]/div[1]/div/div[3]/div[1]/div[1]')
    yjyc_years = yjyc_years.text.split('\n')
    year_2019_index = yjyc_years.index('2019')

    if year_2019_index > 0:
        year_2019_last_index = year_2019_index - len(yjyc_years) + 1
    else:
        year_2019_last_index = year_2019_index

    left_num_xpath = '//*[@id="yjycChart"]/div[last()]'
    if year_2019_last_index < 0:
        left_num_xpath = '/html/body/div[3]/div[3]/div[1]/div[2]/div[1]/div/div[3]/div[last(){}]'.format(year_2019_last_index)


    # 2019 year //*[@id="yjycChart"]/div[last()-2]
    left_num = browser.find_element_by_xpath(left_num_xpath)
    left_num = left_num.text

    # 2020 year //*[@id="forecast"]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[3]
    middel_num = browser.find_element_by_xpath('//*[@id="forecast"]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[3]')
    middel_num = middel_num.text

    # 2021 year //*[@id="forecast"]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[3]
    right_num = browser.find_element_by_xpath('//*[@id="forecast"]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[3]')
    right_num = right_num.text

    # 2022 year //*[@id="forecast"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[3]
    four_num = browser.find_element_by_xpath('//*[@id="forecast"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[3]')
    four_num = four_num.text

    if not is_float(right_num) or not is_float(middel_num) or not is_float(right_num) or not is_float(total_price) or  not is_float(price):
        log_text = '{} [string not is float.] [name: {}, url: {}]'.format(time.strftime('%Y-%m-%d %H:%M:%S'), name, url)
        error_list.append(log_text)
        error_codes.append('{},{}'.format(code, multiple))
        write_log(data=log_text)
        return

    if four_num != '':
        low_price = round(float(four_num) * float(multiple) / 2 / float(total_price) * float(price), 2)
        middel_price = round(float(middel_num) * float(multiple) / float(total_price) * float(price), 2)
        high_price = round(float(right_num) * float(multiple) / float(total_price) * float(price), 2)
    else:
        low_price = round(float(right_num) * float(multiple) / 2 / float(total_price) * float(price), 2)
        middel_price = round(float(left_num) * float(multiple) / float(total_price) * float(price), 2)
        high_price = round(float(middel_num) * float(multiple) / float(total_price) * float(price), 2)

    if four_num != '':
        expect_diff = round(float(four_num) / float(middel_num), 2)
    else:
        expect_diff = round(float(right_num) / float(left_num), 2)

    baifenbi = round(low_price * 2 / float(price) * 100 - 100, 2)

    # 增速部分计算
    if float(middel_num) and float(left_num):
        growth_tate_1 = round(float(middel_num) / float(left_num), 2)
    else:
        growth_tate_1 = 0
    if float(right_num) and float(middel_num):
        growth_tate_2 = round(float(right_num) / float(middel_num), 2)
    else:
        growth_tate_2 = 0

    if float(right_num) and float(four_num):
        growth_tate_3 = round(float(four_num) / float(right_num), 2)
    else:
        growth_tate_3 = 0


    # hqzs = get_hqzs(browser, code)
    gszl = get_gszl(browser, code)
    cwfx = get_cwfx_dfcf(browser, code)
    data_list = [
        code,
        name,
        str(middel_num),
        str(right_num),
        str(four_num),
        str(growth_tate_1),
        str(growth_tate_2),
        str(growth_tate_3),
        str(total_price),
        str(price),
        str(low_price),
        str(middel_price),
        str(high_price),
        str(multiple),
        str(baifenbi)+'%',
        str(expect_diff),
        str(cwfx['hbzj']),
        str(cwfx['yszk']),
        str(cwfx['ch']),
        str(cwfx['hjzjgc']),
        str(cwfx['sy']),
        str(cwfx['dqjk']),
        str(gszl['sshy']).strip(),
        # str(hqzs['zyyw']).strip()
    ]

    data_list_str = list(map(str, data_list))

    data = ','.join(data_list_str)


    return data

def run(item=None, browser=None, url_base=None):
    if not item or not browser or not url_base:
        print('item is None or browser is None')
        return

    code, multiple =  item.split(',')
    url = url_base.format(code)
    
    data = None
    log_text = None
    # data = get_data(browser=browser, url=url, multiple=multiple)
    try:
        data = get_data(browser=browser, url=url, multiple=multiple)
    except NotCodeException as e:
        log_text = '{} [code: {}, multiple: {}]'.format(e, code, multiple)
        print(log_text)
    except Exception as e:
        print(e)
        log_text = '{} [error] [url: {}]'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url)

    if log_text:
        add_log(log_text, code, multiple)

    if data:
        save_data(data=data)
        print(data)
