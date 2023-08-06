import os

import pandas as pd
import requests

from viper_research.entity import Exchange, QuoteCycle, ContractType, CategoryType, IndexSource, ChangeType, MeasureUnit
from viper_research.entity import ListStatus, StockType
from viper_research.util import try_parsing_date


class ViperResearch(object):
    """
    数据服务
    """
    RESTFUL_URL = "http://www.yuliangtec.cn:8018"
    license_id = os.getenv('viper_license_id', "")

    @staticmethod
    def set_restful_url(url):
        ViperResearch.RESTFUL_URL = url

    @staticmethod
    def set_license_id(license_id):
        """
        许可证编号
        :param license_id:许可证编号
        :return:None
        """
        ViperResearch.license_id = license_id

    @staticmethod
    def get_bar_quote(start_time: str, finish_time: str, contract_code: str, exchange: Exchange,
                      quote_cycle: QuoteCycle):
        """
        获取K线行情
        :param start_time:开始时间
        :param finish_time:结束时间
        :param contract_code:合约代码
        :param exchange:交易所
        :param quote_cycle:周期
        :return:dataframe
        """
        params = dict()
        params['startTime'] = try_parsing_date(start_time).isoformat()
        params['finishTime'] = try_parsing_date(finish_time).isoformat()
        params['quoteCycleType'] = quote_cycle.value
        params['contractCode'] = contract_code
        params['licenseId'] = ViperResearch.license_id
        params['exchange'] = exchange.value

        data = requests.get(url=ViperResearch.RESTFUL_URL + "/get/bar/quote", params=params)
        lines = data.text.split("\n")

        fields = lines[0].split(",")
        row_list = list()
        for line in lines[1:]:
            row_data = line.split(",")
            if len(row_data) == 7:
                row_list.append(row_data)

        pd_data = pd.DataFrame(row_list, columns=fields)
        if len(fields) < 7:
            return pd_data

        pd_data['high'] = pd.to_numeric(pd_data['high'], errors='coerce')
        pd_data['open'] = pd.to_numeric(pd_data['open'], errors='coerce')
        pd_data['low'] = pd.to_numeric(pd_data['low'], errors='coerce')
        pd_data['close'] = pd.to_numeric(pd_data['close'], errors='coerce')
        pd_data['volume'] = pd.to_numeric(pd_data['volume'], errors='coerce')

        del pd_data['order_book_id']
        pd_data.insert(loc=0, column='exchange', value=exchange)
        pd_data.insert(loc=0, column='contract_code', value=contract_code)

        return pd_data

    @staticmethod
    def get_tick_quote(start_time: str, finish_time: str, contract_code: str, exchange: Exchange):
        """
        获取tick行情
        :param start_time:开始时间
        :param finish_time:结束时间
        :param contract_code:合约代码
        :param exchange:交易所
        :return:dataframe
        """
        params = dict()
        params['startTime'] = try_parsing_date(start_time).isoformat()
        params['finishTime'] = try_parsing_date(finish_time).isoformat()
        params['quoteCycleType'] = QuoteCycle.TICK.value
        params['licenseId'] = ViperResearch.license_id
        params['contractCode'] = contract_code
        params['exchange'] = exchange.value

        data = requests.get(url=ViperResearch.RESTFUL_URL + "/get/tick/quote", params=params)
        lines = data.text.split("\n")

        fields = lines[0].split(",")
        columns = len(fields)
        row_list = list()
        for line in lines[1:]:
            row_data = line.split(",")
            if len(row_data) == columns:
                row_list.append(row_data)

        pd_data = pd.DataFrame(row_list, columns=fields)
        if columns <= 30:
            return pd_data

        pd_data['open'] = pd_data['open'].astype(float)
        pd_data['last'] = pd_data['last'].astype(float)
        pd_data['high'] = pd_data['high'].astype(float)
        pd_data['low'] = pd_data['low'].astype(float)

        pd_data['prev_close'] = pd_data['prev_close'].astype(float)
        pd_data['volume'] = pd_data['volume'].astype(float)

        pd_data['total_turnover'] = pd_data['total_turnover'].astype(float)
        pd_data['limit_up'] = pd_data['limit_up'].astype(float)
        pd_data['limit_down'] = pd_data['limit_down'].astype(float)

        pd_data['a1'] = pd_data['a1'].astype(float)
        pd_data['a2'] = pd_data['a2'].astype(float)
        pd_data['a3'] = pd_data['a3'].astype(float)
        pd_data['a4'] = pd_data['a4'].astype(float)
        pd_data['a5'] = pd_data['a5'].astype(float)

        pd_data['b1'] = pd_data['b1'].astype(float)
        pd_data['b2'] = pd_data['b2'].astype(float)
        pd_data['b3'] = pd_data['b3'].astype(float)
        pd_data['b4'] = pd_data['b4'].astype(float)
        pd_data['b5'] = pd_data['b5'].astype(float)

        pd_data['a1_v'] = pd_data['a1_v'].astype(float)
        pd_data['a2_v'] = pd_data['a2_v'].astype(float)
        pd_data['a3_v'] = pd_data['a3_v'].astype(float)
        pd_data['a4_v'] = pd_data['a4_v'].astype(float)
        pd_data['a5_v'] = pd_data['a5_v'].astype(float)

        pd_data['b1_v'] = pd_data['b1_v'].astype(float)
        pd_data['b2_v'] = pd_data['b2_v'].astype(float)
        pd_data['b3_v'] = pd_data['b3_v'].astype(float)
        pd_data['b4_v'] = pd_data['b4_v'].astype(float)
        pd_data['b4_v'] = pd_data['b4_v'].astype(float)
        pd_data['b5_v'] = pd_data['b5_v'].astype(float)

        pd_data['change_rate'] = pd_data['change_rate'].astype(float)

        if columns == 35:
            pd_data['prev_settlement'] = pd_data['prev_settlement'].astype(float)
            pd_data['open_interest'] = pd_data['open_interest'].astype(float)

        del pd_data['order_book_id']
        pd_data.insert(loc=0, column='exchange', value=exchange)
        pd_data.insert(loc=0, column='contract_code', value=contract_code)

        return pd_data

    @staticmethod
    def get_continuous_contract(exchange: Exchange):
        """
        获取连续合约
        :param exchange:交易所
        :return: dataframe
        """
        param = dict()
        param['exchange'] = exchange.value
        r = requests.get(url=ViperResearch.RESTFUL_URL + "/get/continuous/contract", params=param)

        data = r.json()
        pd_data = pd.DataFrame(data)

        pd_data['exchange'] = exchange
        pd_data['contractType'] = ContractType.CONTINUOUS

        return pd_data

    @staticmethod
    def get_continuous_item(exchange: Exchange, contract_code: str, start_time: str):
        """
        获取连续合约对应的真实合约
        :param exchange:交易所
        :param contract_code:连续合约代码
        :param start_time:开始时间
        :return:dataframe
        """
        param = dict()
        param['exchange'] = exchange.value
        param['contractCode'] = contract_code
        param['startDateTime'] = try_parsing_date(start_time).date().isoformat()

        r = requests.get(url=ViperResearch.RESTFUL_URL + "/get/continuous/item", params=param)
        data = r.json()
        pd_data = pd.DataFrame(data)
        pd_data['exchange'] = exchange

        pd_data.rename(columns={'continuousContractCode': 'continuous_code'}, inplace=True)
        del pd_data['continuousContractExchange']

        return pd_data

    @staticmethod
    def get_future_category(exchange: Exchange):
        """
        获取期货品种
        :param exchange:交易所
        :return:dataframe
        """
        param = dict()
        param['exchange'] = exchange.value

        r = requests.get(ViperResearch.RESTFUL_URL + "/get/future/category", params=param)
        data = r.json()
        pd_data = pd.DataFrame(data)
        pd_data['categoryType'] = pd_data['categoryType'].apply(lambda x: CategoryType(x))
        pd_data['unit'] = pd_data['unit'].apply(lambda x: MeasureUnit(x))
        pd_data['exchange'] = exchange

        return pd_data

    @staticmethod
    def get_future_contract(exchange: Exchange, category_code: str, start_date: str):
        """
        获取期货合约
        :param exchange:交易所
        :param category_code: 品种代码
        :param start_date: 开始日期
        :return:dataframe
        """
        param = dict()
        param['exchange'] = exchange.value
        param['categoryCode'] = category_code
        param['startDate'] = try_parsing_date(start_date).date().isoformat()

        r = requests.get(ViperResearch.RESTFUL_URL + "/get/future/contract", params=param)
        data = r.json()
        pd_data = pd.DataFrame(data)
        pd_data['contractType'] = ContractType.FUTURE
        pd_data['exchange'] = exchange
        del pd_data['categoryExchange']

        return pd_data

    @staticmethod
    def get_future_settlement(exchange: Exchange, start_date, end_date):
        param = dict()
        param['exchange'] = exchange.value
        param['startDate'] = try_parsing_date(start_date).date().isoformat()
        param['enDate'] = try_parsing_date(end_date).date().isoformat()

        r = requests.get(ViperResearch.RESTFUL_URL + "/get/future/settlement", params=param)
        data = r.json()
        pd_data = pd.DataFrame(data)

        return pd_data

    @staticmethod
    def get_index_contract():
        """
        获取指数合约
        :return:dataframe
        """
        r = requests.get(url=ViperResearch.RESTFUL_URL + "/get/index/contract")
        data = r.json()
        pd_data = pd.DataFrame(data)
        pd_data['contractType'] = ContractType.INDEX
        pd_data['exchange'] = pd_data['exchange'].apply(lambda x: Exchange(x))
        pd_data['indexSource'] = pd_data['indexSource'].apply(lambda x: IndexSource(x))

        return pd_data

    @staticmethod
    def get_index_item(contract_code, start_date):
        """
        获取指数合约成分信息
        :param contract_code:合约代码
        :param start_date:开始日期
        :return:dataframe
        """
        param = dict()
        param['startDate'] = try_parsing_date(start_date).date().isoformat()
        param['contractCode'] = contract_code

        r = requests.get(ViperResearch.RESTFUL_URL + "/get/index/item", params=param)
        data = r.json()
        pd_data = pd.DataFrame(data)
        pd_data['exchange'] = pd_data['exchange'].apply(lambda x: Exchange(x))
        pd_data['indexContractExchange'] = pd_data['indexContractExchange'].apply(lambda x: Exchange(x))
        pd_data['changeType'] = pd_data['changeType'].apply(lambda x: ChangeType(x))

        return pd_data

    @staticmethod
    def get_stock_contract(exchange: Exchange, list_status: ListStatus, start_date):
        """
        获取股票合约
        :param exchange:交易所
        :param list_status:上市状态
        :param start_date:开始时间
        :return:dataframe
        """
        param = dict()
        param['exchange'] = exchange.value
        param['listStatus'] = list_status.value
        param['startDate'] = try_parsing_date(start_date).date().isoformat()

        r = requests.get(ViperResearch.RESTFUL_URL + "/get/stock/contract", params=param)
        data = r.json()
        pd_data = pd.DataFrame(data)
        pd_data['contractType'] = ContractType.STOCK
        pd_data['exchange'] = exchange
        pd_data['listStatus'] = list_status
        pd_data['stockType'] = pd_data['stockType'].apply(lambda x: StockType(x))

        return pd_data

    @staticmethod
    def get_trading_day(exchange: Exchange, start_date):
        """
        获取交易日历
        :param exchange:交易所
        :param start_date:开始时间
        :return:dataframe
        """
        param = dict()
        param['startDate'] = try_parsing_date(start_date).date().isoformat()
        param['exchange'] = exchange.value

        r = requests.get(ViperResearch.RESTFUL_URL + "/get/trading/day", params=param)

        data = r.json()
        pd_data = pd.DataFrame(data)
        pd_data['exchange'] = exchange

        return pd_data
