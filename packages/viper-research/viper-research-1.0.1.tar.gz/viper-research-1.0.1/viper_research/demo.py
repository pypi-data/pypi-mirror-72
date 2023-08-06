from viper_research import *

# 系统支持如下格式的时间类型 '%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y%m%d'


# 设置许可证编号
# 用户可以在shell和windows系统中设置 viper_license_id 环境变量，可以避免每次都要设置许可证编号
ViperResearch.set_license_id("45713455-*******")

"""
获取K线行情
:param start_time:开始时间
:param finish_time:结束时间
:param contract_code:合约代码
:param exchange:交易所
:param quote_cycle:周期
:return:dataframe
"""
data = ViperResearch.get_bar_quote(start_time="2018-01-01", finish_time="2020-06-22", contract_code="601318",
                                   exchange=Exchange.SSE, quote_cycle=QuoteCycle.FIVE_MINUTE)

"""
获取tick行情
:param start_time:开始时间
:param finish_time:结束时间
:param contract_code:合约代码
:param exchange:交易所
:return:dataframe
"""

data = ViperResearch.get_tick_quote(start_time="2020-06-22", finish_time="2020-06-22", contract_code="601318",
                                    exchange=Exchange.SSE)

"""
获取连续合约
:param exchange:交易所
:return: dataframe
"""
data = ViperResearch.get_continuous_contract(Exchange.SHFE)

"""
获取连续合约对应的真实合约
:param exchange:交易所
:param contract_code:连续合约代码
:param start_time:开始时间
:return:dataframe
"""

data = ViperResearch.get_continuous_item(exchange=Exchange.SSE, contract_code="CU", start_time="2018-01-01")

"""
获取期货品种
:param exchange:交易所
:return:dataframe
"""
data = ViperResearch.get_future_category(Exchange.SSE)

"""
获取期货合约
:param exchange:交易所
:param category_code: 品种代码
:param start_date: 开始日期
:return:dataframe
"""
data = ViperResearch.get_future_contract(exchange=Exchange.SHFE, category_code="CU", start_date="2018-01-01")

"""
获取指数合约
:return:dataframe
"""
data = ViperResearch.get_index_contract()

"""
获取指数合约成分信息
:param contract_code:合约代码
:param start_date:开始日期
:return:dataframe
"""
data = ViperResearch.get_index_item(contract_code="000905", start_date="2018-01-01")

"""
获取股票合约
:param exchange:交易所
:param list_status:上市状态
:param start_date:开始时间
:return:dataframe
"""
data = ViperResearch.get_stock_contract(exchange=Exchange.SSE, list_status=ListStatus.LISTED, start_date="2010-01-01")

"""
获取交易日历
:param exchange:交易所
:param start_date:开始时间
:return:dataframe
"""
data = ViperResearch.get_trading_day(exchange=Exchange.SSE, start_date="2000-01-01")
