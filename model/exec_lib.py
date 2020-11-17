import os
import time
import selenium.webdriver.support.ui as ui
from model.utils import *

def get_cwfx(browser=None, code=0):
    url = 'http://stockpage.10jqka.com.cn/{}/finance/'.format(code)
    browser.get(url)
    ui.WebDriverWait(browser, 10)
    browser.switch_to_frame('dataifm')


    hbzj = yszk = ch = hjzjgc = dqjk = sy = '*******'
    browser.find_element_by_xpath('//*[@id="title-chart"]/div[2]/ul/li[2]/a').click()
    browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/ul/li[2]/a').click()

    # 防止未加载出来元素后面后获取不到返回空值
    time.sleep(1)

    # 短期借款
    try:
        dqjk_index = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[3]/table[2]/tbody/tr/th[@data-title="短期借款"]/..').get_attribute('data-index')
        dqjk = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[4]/div/table[2]/tbody/tr[{}]/td[1]'.format(dqjk_index)).text
    except Exception as e:
        pass
    # 货币资金
    try:
        hbzj_index = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[3]/table[2]/tbody/tr/th[@data-title="货币资金"]/..').get_attribute('data-index')
        hbzj = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[4]/div/table[2]/tbody/tr[{}]/td[1]/div'.format(hbzj_index)).text
    except Exception as e:
        pass
    # 应收账款
    try:
        yszk_index = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[3]/table[2]/tbody/tr/th[@data-title="应收账款"]/..').get_attribute('data-index')
        yszk = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[4]/div/table[2]/tbody/tr[{}]/td[1]'.format(yszk_index)).text
    except Exception as e:
        pass
    # 存货
    try:
        ch_index = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[3]/table[2]/tbody/tr/th[@data-title="存货"]/..').get_attribute('data-index')
        ch = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[4]/div/table[2]/tbody/tr[{}]/td[1]'.format(ch_index)).text
    except Exception as e:
        pass
    # 合计在建工程
    try:
        hjzjgc_index = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[3]/table[2]/tbody/tr/th[@data-title="在建工程合计"]/..').get_attribute('data-index')
        hjzjgc = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[4]/div/table[2]/tbody/tr[{}]/td[1]'.format(hjzjgc_index)).text
    except Exception as e:
        pass
    # 商誉
    try:
        sy_index = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[3]/table[2]/tbody/tr/th[@data-title="商誉"]/..').get_attribute('data-index')
        sy = browser.find_element_by_xpath('//*[@id="cwzbTable"]/div[1]/div[1]/div[4]/div/table[2]/tbody/tr[{}]/td[1]'.format(sy_index)).text
    except Exception as e:
        pass

    res = {
        'hbzj': hbzj,
        'yszk': yszk,
        'ch': ch,
        'hjzjgc': hjzjgc,
        'dqjk': dqjk,
        'sy': sy,
    }
    return res

def get_cwfx_dfcf(browser=None, code=0):
    code_str = get_code_str(code)
    hbzj = yszk = ch = hjzjgc = dqjk = sy = '*******'
    if not code_str:
        # log_text = '{} [当前股票代码并未维护] [not code: {}]'.format(time.strftime('%Y-%m-%d %H:%M:%S'), code)
        raise NotCodeException(code)

    url = 'http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code={}#zcfzb-0'.format(code_str)
    browser.get(url)
    ui.WebDriverWait(browser, 10)

    
    # browser.find_element_by_xpath('//*[@id="zcfzb_ul"]/li[2]/span').click()

    # 防止未加载出来元素后面后获取不到返回空值
    time.sleep(0.5)

    # 短期借款
    dqjk = browser.find_element_by_xpath('//*[@id="report_zcfzb"]/tbody/tr[52]/td[2]/span').text

    # 货币资金
    hbzj = browser.find_element_by_xpath('//*[@id="report_zcfzb"]/tbody/tr[3]/td[2]/span').text

    # 应收账款
    yszk = browser.find_element_by_xpath('//*[@id="report_zcfzb"]/tbody/tr[11]/td[2]/span').text

    # 存货
    ch = browser.find_element_by_xpath('//*[@id="report_zcfzb"]/tbody/tr[24]/td[2]/span').text

    # 在建工程
    hjzjgc = browser.find_element_by_xpath('//*[@id="report_zcfzb"]/tbody/tr[37]/td[2]/span').text

    # 商誉
    sy = browser.find_element_by_xpath('//*[@id="report_zcfzb"]/tbody/tr[44]/td[2]/span').text

    res = {
        'dqjk': dqjk,
        'hbzj': hbzj,
        'yszk': yszk,
        'ch': ch,
        'hjzjgc': hjzjgc,
        'sy': sy,
    }
    return res


def get_gszl(browser=None, code=0):
    url = 'http://stockpage.10jqka.com.cn/{}/company/'.format(code)
    browser.get(url)
    ui.WebDriverWait(browser, 10)
    try:
        browser.switch_to_frame('dataifm')

        try:
            sshy = browser.find_element_by_xpath('//*[@id="detail"]/div[2]/table/tbody/tr[2]/td[2]/span')
        except:
            # solve xpath error.
            sshy = browser.find_element_by_xpath('//*[@id="detail"]/div[3]/table/tbody/tr[2]/td[2]/span')

        sshy = sshy.text
    except:
        sshy = ''

    res = {
        'sshy': sshy
    }
    return res

def get_hqzs(browser=None, code=0):
    url = 'http://stockpage.10jqka.com.cn/{}/#hqzs'.format(code)
    browser.get(url)
    ui.WebDriverWait(browser, 10)
    try:
        zyyw = browser.find_element_by_xpath('/html/body/div[10]/div[2]/div[3]/dl/dd[2]')
        zyyw = '、'.join(zyyw.get_attribute("title").split('，')[0:3])
    except Exception as e:
        zyyw = ''

    res = {
        'zyyw': zyyw
    }
    return res
