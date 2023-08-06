from enum import Enum, unique


@unique
class QuoteCycle(Enum):
    """
    K线的周期类型
    """
    DAY = 1
    ONE_MINUTE = 2
    FIVE_MINUTE = 3
    TICK = 4


@unique
class Exchange(Enum):
    """
    交易所常量
    """
    DCE = 1
    SHFE = 2
    CZCE = 3
    CFFEX = 4
    SSE = 5
    SZSE = 6
    INE = 7
    VIPER = 8


@unique
class ContractType(Enum):
    """
    合约类型
    """
    FUTURE = 1
    OPTION = 2
    STOCK = 3
    STOCKOPTION = 4
    EAC = 5
    INDEX = 6
    CONTINUOUS = 7


@unique
class CategoryType(Enum):
    """
    期货品种类型
    """
    INDUSTRIAL = 1
    AGRICULTURAL = 2
    INDEX = 3
    ENERGY_CHEMICAL = 4
    NATIONAL_DEBT = 5
    FOREX = 6
    METAL = 7
    NEW = 8
    OTHER = 11


@unique
class MeasureUnit(Enum):
    """
    度量单位
    """
    BUSHEL = 1
    BTU = 2
    MM_BTU = 3
    LBS = 4
    BARREL = 5
    GALLON = 6
    SHORT_TON = 7
    TONNE = 8
    TON = 9
    G = 10
    KG = 11
    OUNCE = 12
    POINT = 13
    YUAN = 14
    PIECE = 15
    SHARE = 16
    OTHER = 17


@unique
class IndexSource(Enum):
    """
    指数行情来源
    """
    SSE = 1
    SZSE = 2
    MSCI = 3
    CSI = 4
    SW = 5
    VIPER = 6


@unique
class ChangeType(Enum):
    """
    指数行情变动原因
    """
    ADD = 1
    REMOVE = 2
    INIT = 3


@unique
class ListStatus(Enum):
    """
    上市状态
    """
    LISTED = 1
    PAUSE = 2
    STOP = 3


@unique
class StockType(Enum):
    """
    股票合约类型
    """
    STOCK_A = 1
    STOCK_B = 2
    STOCK_SCIENCE = 3
    FUND = 4
    DEBENTURE = 5
    INDEX = 6
    STOCK_H = 7
    OTHER = 8
