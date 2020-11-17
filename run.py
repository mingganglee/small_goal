import os
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui

from model.exec_handle import *
from model.utils import error_codes, error_list


def main():
	input_code = input('请输入: 代码,倍数|代码,倍数|... : ')
	url_base = "http://stockpage.10jqka.com.cn/{}/worth/#forecastdetail"
	code_list = input_code.split('|')
	options = webdriver.ChromeOptions()
	# 使用headless无界面浏览器模式
	# options.add_argument('--headless') # 增加无界面选项
	options.add_argument('--disable-gpu') # 如果不加这个选项，有时定位会出现问题
	# 启动浏览器，获取网页源代码
	browser = webdriver.Chrome('./chromedriver', options=options)
	try:
		for item in code_list:
			code =  item.split(',')[0]
			run(item, browser, url_base.format(code))
	except Exception as e:
		print('run', e)
	finally:
		browser.quit()

	if error_list:
		print('----------ERROR----------')
		for text in error_list:
			print(text)
		print('----------ERROR----------')
		print('\n错误代码: ')
		print('|'.join(error_codes))

	print('----- 完成 !')

if __name__ == '__main__':
	main()
