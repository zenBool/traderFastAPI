import calendar
import sys
import time
from datetime import datetime

from pydantic.typing import Literal
import pandas as pd

from binanceTrade.autotrader.clients import Client, ClientWS
from binanceTrade.autotrader.func import df_normalize
from binanceTrade.autotrader import enums
from binanceTrade.autotrader.logger import logger


class BinanceDataLoader:
    def __init__(self, symbol: str, interval: str):
        # вынести в config
        # Самая рання дата с которой работает приложение
        self.oldest_time = calendar.timegm((2020, 1, 1, 0, 0, 0)) * 1000

        self.symbol = symbol
        self.interval = interval
        self.client = Client(test_mode=False)
        self.client_ws = ClientWS(test_mode=False)

    def stream_data(self):
        # self.client_ws.start()
        logger.info("open ws connection")

        try:
            self.client_ws.kline(symbol=self.symbol, id=2, interval=self.interval, callback_=self._handler)
            logger.info(f"{self.symbol} {self.interval} kline stream subscribe")

            while True:
                pass

        except KeyboardInterrupt:
            ...
        finally:
            logger.info(f"closing ws connection")
            self.client_ws.stop()

    def load_historical_data(
            self,
            symbol: str = "BTCUSDT",
            interval: Literal[enums.INTERVALS] = '1m',
            limit: int = 10,
            start: int = None,
            end: int = None
    ) -> pd.DataFrame:
        """ Загрузка исторических данных с сервера Binance

            :param str symbol: Binance trading symbol e.g. "BTCUSDT"
            :param interval: name time interval
            :type interval: str in enums.INTERVALS
            :param int limit: any int __ge__ 0
            :return: pandas.DataFrame with historical data by symbol_period
        """
        klines = []
        start_time = None
        interval_time = enums.INTERVALS_TIME.get(interval)
        _limit = limit

        if limit > 1000:
            start_time = self._time_now() - limit * interval_time
            if start_time < self.oldest_time:
                start_time = self.oldest_time
                limit = int((self._time_now() - start_time) / interval_time)

            _limit = 1000

        # Load data in chunks of 1000 bars
        while limit > 0:
            bars = self.client.klines(
                symbol=symbol, interval=interval, startTime=start_time, limit=_limit
            )
            klines += bars

            # Set start_time to the next timestamp after the last bar in the previous chunk
            start_time = int(bars[-1][0] + interval_time)
            limit -= 1000

        # Convert data to pandas DataFrame
        df = pd.DataFrame(klines, columns=enums.COLUMNS)
        df = df_normalize(df)
        # df["time_open"] = pd.to_datetime(df["time_open"], unit="ms")
        # df.set_index("time_open", inplace=True)

        return df

    def _handler(self, message):
        global df_wss
        data = message.get('k')
        if data is None:
            return

        symbol = data['s']
        global_df = df_wss[symbol]

        _df = self._adapter(data)

        if global_df is not None:
            _dfi = data['t']
            _gli = global_df.index.to_list()
            if _dfi not in _gli:
                global_df = pd.concat([global_df, _df], join='outer')
            else:
                global_df.update(_df, overwrite=True)
        else:
            raise Exception('<global_df> doesnt be None', global_df)

        logger.info(global_df.tail(2))
        logger.info(global_df['close'].to_list()[-1])

    def _time_now(self):
        return int(time.time()) * 1000

    def _adapter(self, data: dict = None):
        # Data example
        sf = {'t': 1659798240000, 'T': 1659781079999, 's': 'BTCUSDT', 'i': '1m', 'f': 146705,
              'L': 146757, 'o': '6.17000000', 'c': '23197.50000000', 'h': '23199.14000000',
              'l': '23196.17000000', 'v': '2.45011400', 'n': 53, 'x': False, 'q': '56836.65111634',
              'V': '1.10623200', 'Q': '25661.94302789', 'B': '0'}

        if data is None:
            return

        dataframe_format = {
            'time_open': data.get('t'),
            'open': data.get('o'),
            'high': data.get('h'),
            'low': data.get('l'),
            'close': data.get('c'),
            'volume': data.get('v'),
            'time_close': data.get('T'),
            'q_asset_vol': data.get('q'),
            'num_trades': data.get('n'),
            'tb_base_av': data.get('V'),
            'tb_quote_av': data.get('Q'),
            'ignore': data.get('B')
        }

        df = pd.DataFrame(dataframe_format, index=[0])
        df = df_normalize(df)
        df.set_index('time_open', inplace=True)

        return df


oldest_time = calendar.timegm((2020, 1, 1, 0, 0, 0)) * 1000


def time_now_ms(self):
    return int(time.time()) * 1000


def load_historical_data(
        symbol: str = "BTCUSDT",
        interval: Literal[enums.INTERVALS] = '1m',
        limit: int = 10,
        start: int = None,
        end: int = None
) -> pd.DataFrame:
    """ Загрузка исторических данных с сервера Binance

        :param str symbol: Binance trading symbol e.g. "BTCUSDT"
        :param interval: name time interval
        :type interval: str in enums.INTERVALS
        :param int limit: any int __ge__ 0
        :return: pandas.DataFrame with historical data by symbol_period
    """

    client = Client(test_mode=False)
    klines = []
    start_time = None
    interval_time = enums.INTERVALS_TIME.get(interval)
    _limit = limit

    if limit > 1000:
        start_time = time_now_ms() - limit * interval_time
        if start_time < oldest_time:
            start_time = oldest_time
            limit = int((time_now_ms() - start_time) / interval_time)

        _limit = 1000

    # Load data in chunks of 1000 bars
    while limit > 0:
        bars = client.klines(
            symbol=symbol, interval=interval, startTime=start_time, limit=_limit
        )
        klines += bars

        # Set start_time to the next timestamp after the last bar in the previous chunk
        start_time = int(bars[-1][0] + interval_time)
        limit -= 1000

    # Convert data to pandas DataFrame
    df = pd.DataFrame(klines, columns=enums.COLUMNS)
    df = df_normalize(df)
    # df["time_open"] = pd.to_datetime(df["time_open"], unit="ms")
    # df.set_index("time_open", inplace=True)

    return df


if __name__ == '__main__':
    # loader = BinanceDataLoader()
    # df = loader.load_historical_data()
    # print(df.dtypes)
    # # print(df.head())
    #
    # print(datetime.utcfromtimestamp(time.time_ns() / 1000000000))
    # print(datetime.utcfromtimestamp(int(time.time_ns() / 1000000000)))

    client = Client(test_mode=False)
    print(client.KLINE_INTERVAL_1HOUR)
    # for param in client.__dir__():
    #     print(param)