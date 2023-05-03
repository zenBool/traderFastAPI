from datetime import *
from enum import Enum
from typing import Literal, List, Any

from pydantic import BaseModel


INTERVALS: List[str] = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]
INTERVALS_LITERAL = Literal["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]


class IntervalNameEnum(str, Enum):
    SEC1 = "1s"
    MIN1 = "1m"
    MIN3 = "3m"
    MIN5 = "5m"
    MIN15 = "15m"
    MIN30 = "30m"
    HOUR1 = "1h"
    HOUR2 = "2h"
    HOUR4 = "4h"
    HOUR6 = "6h"
    HOUR8 = "8h"
    HOUR12 = "12h"
    DAY1 = "1d"
    DAY3 = "3d"
    WEEK1 = "1w"


class IntervalValueEnum(int, Enum):
    SEC1 = 1000
    MIN1 = 1000 * 60
    MIN3 = 1000 * 60 * 3
    MIN5 = 1000 * 60 * 5
    MIN15 = 1000 * 60 * 15
    MIN30 = 1000 * 60 * 30
    HOUR1 = 1000 * 60 * 60
    HOUR2 = 1000 * 60 * 60 * 2
    HOUR4 = 1000 * 60 * 60 * 4
    HOUR6 = 1000 * 60 * 60 * 6
    HOUR8 = 1000 * 60 * 60 * 8
    HOUR12 = 1000 * 60 * 60 * 12
    DAY1 = 1000 * 60 * 60 * 24
    DAY3 = 1000 * 60 * 60 * 24 * 3
    WEEK1 = 1000 * 60 * 60 * 24 * 7


class Interval(BaseModel):
    name: Literal[INTERVALS_LITERAL]
    ms: IntervalValueEnum = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.ms = getattr(IntervalValueEnum, IntervalNameEnum(self.name).name).value


TRADING_TYPE = Literal["spot", "um", "cm"]
MONTHS = list(range(1, 13))
INTERVALS_TIME = {
    "1m": 1000 * 60,
    "3m": 1000 * 60 * 3,
    "5m": 1000 * 60 * 5,
    "15m": 1000 * 60 * 15,
    "30m": 1000 * 60 * 30,
    "1h": 1000 * 60 * 60,
    "2h": 1000 * 60 * 60 * 2,
    "4h": 1000 * 60 * 60 * 4,
    "6h": 1000 * 60 * 60 * 6,
    "8h": 1000 * 60 * 60 * 8,
    "12h": 1000 * 60 * 60 * 12,
    "1d": 1000 * 60 * 60 * 24,
    "3d": 1000 * 60 * 60 * 24 * 3,
    "1w": 1000 * 60 * 60 * 24 * 7,
}
COLUMNS = ['time_open', 'open', 'high', 'low', 'close', 'volume', 'time_close', 'q_asset_vol',
           'num_trades', 'tb_base_av', 'tb_quote_av', 'ignore']
COLUMNS_EMA = ['ma_5', 'ma_8', 'ma_13', 'ma_21', 'ma_34', 'ma_55', 'ma_89',
               'ma_144', 'ma_5_delta', 'ma_8_delta', 'ma_13_delta', 'ma_21_delta',
               'ma_34_delta', 'ma_55_delta', 'ma_89_delta', 'ma_144_delta', 'time_open']
SYMBOLS = (
    '1INCHUSDT', 'AAVEUSDT', 'ADAUSDT', 'ALGOUSDT', 'AMPUSDT', 'APEUSDT', 'ARUSDT', 'ATOMUSDT', 'AVAXUSDT', 'AXSUSDT',
    'BCHUSDT', 'BNBUSDT', 'BNTUSDT', 'BTCUSDT', 'CAKEUSDT', 'CELOUSDT', 'CHZUSDT', 'COMPUSDT', 'CRVUSDT',
    'DASHUSDT', 'DOGEUSDT', 'DOTUSDT', 'EGLDUSDT', 'ENJUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'FILUSDT', 'FLOWUSDT',
    'FTMUSDT', 'GALAUSDT', 'GNOUSDT', 'GRTUSDT', 'HBARUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT',
    'IOTAUSDT', 'IOTXUSDT', 'KDAUSDT', 'KLAYUSDT', 'KSMUSDT', 'LINKUSDT', 'LPTUSDT', 'LRCUSDT', 'LTCUSDT', 'MANAUSDT',
    'MATICUSDT', 'MINAUSDT', 'MKRUSDT', 'NEARUSDT', 'NEOUSDT', 'OMGUSDT', 'ONEUSDT', 'ONTUSDT', 'QTUMUSDT',
    'ROSEUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SCRTUSDT', 'SHIBUSDT', 'SOLUSDT', 'STXUSDT', 'SUSHIUSDT',
    'TFUELUSDT', 'THETAUSDT', 'TRXUSDT', 'UNIUSDT', 'VETUSDT', 'WAVESUSDT', 'WAXPUSDT', 'XECUSDT',
    'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'XTZUSDT', 'YFIUSDT', 'ZECUSDT',
    'ADABTC', 'ATOMBTC', 'AVAXBTC', 'BATBTC', 'DASHBTC', 'DOGEBTC', 'DOTBTC', 'ETCBTC', 'EOSBTC', 'IOTABTC',
    'LINKBTC', 'LTCBTC', 'MATICBTC', 'NEOBTC', 'OMGBTC', 'ONTBTC', 'QTUMBTC', 'SOLBTC', 'TRXBTC',
    'VETBTC', 'XLMBTC', 'XMRBTC', 'ADAETH', 'ATOMETH', 'AVAXETH', 'BATETH', 'DASHETH', 'EOSETH',
    'DOTETH', 'ETCETH', 'IOTAETH', 'LINKETH', 'LTCETH', 'MATICETH', 'NEOETH', 'OMGETH', 'ONTETH', 'QTUMETH',
    'SOLETH', 'TRXETH', 'VETETH', 'XLMETH', 'XMRETH', 'ADABNB', 'ATOMBNB', 'AVAXBNB', 'BATBNB', 'DASHBNB',
    'DOTBNB', 'EOSBNB', 'ETCBNB', 'IOTABNB', 'LINKBNB', 'LTCBNB', 'MATICBNB', 'NEOBNB', 'OMGBNB', 'ONTBNB',
    'QTUMBNB', 'SOLBNB', 'TRXBNB', 'VETBNB', 'XLMBNB', 'XMRBNB')
SYMBOLS_AMPLITUDE_USDT = (
    'ADAUSDT', 'ATOMUSDT', 'AVAXUSDT', 'DASHUSDT', 'DOGEUSDT', 'DOTUSDT', 'EOSUSDT',
    'ETCUSDT', 'IOTAUSDT', 'LINKUSDT', 'LTCUSDT', 'MATICUSDT', 'NEOUSDT', 'OMGUSDT', 'ONTUSDT', 'QTUMUSDT',
    'SOLUSDT', 'TRXUSDT', 'VETUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT')
SYMBOLS_AMPLITUDE_USDT_TEST = ('BTCUSDT', 'BNBUSDT', 'ETHUSDT')
SYMBOLS_AMPLITUDE_BTC = (
    'ADABTC', 'ATOMBTC', 'AVAXBTC', 'DASHBTC', 'DOGEBTC', 'DOTBTC', 'EOSBTC', 'ETCBTC',
    'IOTABTC', 'LINKBTC', 'LTCBTC', 'MATICBTC', 'NEOBTC', 'OMGBTC', 'ONTBTC', 'QTUMBTC', 'SOLBTC', 'TRXBTC',
    'VETBTC', 'XLMBTC', 'XMRBTC', 'XRPBTC')

if __name__ == '__main__':
    # new_list = []
    # new_list1 = []
    # new_list2 = []
    # new_list3 = []
    # for el in SYMBOLS_AMPLITUDE_USDT:
    #     if el not in ('BTCUSDT', 'ETHUSDT', 'BNBUSDT'):
    #         new_list1.append((el[:-4] + 'BTC'))
    #         new_list2.append((el[:-4] + 'ETH'))
    #         new_list3.append((el[:-4] + 'BNB'))
    # new_list = new_list1 + new_list2 + new_list3
    # new_list = [el for el in new_list if el not in SYMBOLS]
    # print(new_list)

    # =================================================

    # from datetime import date
    # class Weekday(Enum):
    #     MONDAY = 1
    #     TUESDAY = 2
    #     WEDNESDAY = 3
    #     THURSDAY = 4
    #     FRIDAY = 5
    #     SATURDAY = 6
    #     SUNDAY = 7
    #
    #     @classmethod
    #     def today(cls):
    #         print('today is %s' % cls(date.today().isoweekday()).name)
    #
    # for x in Weekday:
    #     print(type(x.value))

    # =================================================

    interval = Interval(name='15m')
    print(interval.name)
    print(interval.ms)

    # name = 'MIN1'
    # s = IntervalNameEnum('MIN5')
    # print(s)
