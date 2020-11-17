# python_selenium_tonghuashun
python + selenium 爬取同花顺数据

## 环境安装
```
pip3 install selenium
```
## chromedriver 安装
```
http://chromedriver.storage.googleapis.com/index.html
进入网站下载对应版本 chromedriver
```

## 推荐文章
```
https://www.jianshu.com/p/1531e12f8852
```

# 快速获取股票代码方法
```
// 操作流程
// 1.打开 Chrome 浏览器
// 2.打开 东方财富 登陆后跳转到自选股模块
// 3.选中需要获取的股票代码
// 4.鼠标右键在网页中点击检查按钮
// 5.点击检查界面中国呢的 Console 选项
// 6.将下面代码复制到 Console 控制台中

// ----------------------------------------
// 东方财富自选：
code_list = document.getElementsByClassName('td_f12')
codes_str = ''
for(var i=0; i<code_list.length; i++)
{
    codes_str += code_list[i].getAttribute('data-odata') + ','
}

// ----------------------------------------
// 同花顺问财：

code_list = document.getElementsByClassName('static_tbody_table')[0].rows
codes_str = ''
for(var i=0; i<code_list.length; i++)
{
    codes_str += code_list[i].cells[2].children[0].textContent + ','
}
```
