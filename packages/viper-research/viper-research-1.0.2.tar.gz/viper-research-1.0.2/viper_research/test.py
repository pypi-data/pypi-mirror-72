import time
import datetime
from viper_research import *

start_time = "20200101"
finish_time = "20200601"
stock_list = [
    '601318',
    '600519',
    '600000',
    '600004',
    '600009'
]

ViperResearch.set_restful_url("http://www.yuliangtec.cn:8018")
ViperResearch.set_license_id("")
print("---------开始测试第一部分时间-----------")
start = time.time()
for stock_code in stock_list:
    print(str.format(f"发送前{datetime.datetime.now()}"))
    data = ViperResearch.get_bar_quote(start_time, finish_time, stock_code, Exchange.SSE, QuoteCycle.FIVE_MINUTE)
    print(str.format(f"发送后{datetime.datetime.now()}"))
end = time.time()

print(str.format(f"耗时:{end - start}"))

ViperResearch.set_restful_url("http://www.shyouxia.cn:8018")
ViperResearch.set_license_id("")
print("---------开始测试第二部分时间-----------")
start = time.time()
for stock_code in stock_list:
    print(str.format(f"发送前{datetime.datetime.now()}"))
    data = ViperResearch.get_bar_quote(start_time, finish_time, stock_code, Exchange.SSE, QuoteCycle.FIVE_MINUTE)
    print(str.format(f"发送后{datetime.datetime.now()}"))
end = time.time()

print(str.format(f"耗时:{end - start}"))
