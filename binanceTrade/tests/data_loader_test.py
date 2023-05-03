import sys
import time
import calendar

from loguru import logger
import pandas as pd
from pydantic.typing import Literal

from binance_autotrader import Client, ClientWS, enums
from binance_autotrader.func import df_normalize

logger.add(sys.stderr, format="{time} {level} {message}", filter="tests", level="DEBUG")

df_global = {}


class BinanceDataLoader:
    """Загрузка исторических данных с сервера Binance, поддержание актуальности real time.
        Для Получения данных без потока их обновления :param real_time: установить в False

    """
    def __init__(
            self,
            symbol: str = "BTCUSDT",
            interval: str = '1m',
            limit: int = 1000,
            start_time: int = None,
            real_time: bool = True
    ):
        """

        :param str symbol: Binance trading symbol, e.g. "BTCUSDT"
        :param interval: name time interval
        :type interval: str in enums.INTERVALS
        :param int limit: any int __ge__ 0
        :param bool real_time: set to False if not need data stream
        """
        # вынести в config
        # Самая рання дата с которой работает приложение
        self.oldest_time = calendar.timegm((2020, 1, 1, 0, 0, 0)) * 1000

        self.symbol = symbol
        self.interval: Literal[enums.INTERVALS] = interval
        self.client = Client(test_mode=False)
        self.client_ws = ClientWS(test_mode=False)
        self.limit = limit
        self.start_time = start_time
        self._rt = real_time
        self._manager()

    def stream_data(self):
        self.client_ws.start()
        logger.info("open ws connection")

        try:
            self.client_ws.kline(symbol=self.symbol, id=2, interval=self.interval, callback=self._handler)
            logger.info(f"{self.symbol} {self.interval} kline stream subscribe")

            while True:
                pass

        except KeyboardInterrupt:
            ...
        finally:
            logger.info(f"closing ws connection")
            self.client_ws.stop()

    def load_historical_data(self) -> pd.DataFrame:
        """ Загрузка исторических данных с сервера Binance

        :return: pandas.DataFrame with historical data by symbol_period
        :rtype: pandas.DataFrame

        """
        klines = []
        start_time = None
        interval_time = enums.INTERVALS_TIME.get(self.interval)
        _limit = tmp_limit = self.limit

        # в случае, если хотим загрузить более 1000 свечей
        if tmp_limit > 1000:
            # вычисляем начальное время
            start_time = self._time_now() - tmp_limit * interval_time
            # ограничиваем начальное время
            if start_time < self.oldest_time:
                start_time = self.oldest_time
                tmp_limit = int((self._time_now() - start_time) / interval_time)

            _limit = 1000

        # используется для загрузки данных с определенного времени (до 1000 баров)
        if self.start_time:
            start_time = self.start_time

        # Load data in chunks of 1000 bars
        while tmp_limit > 0:
            bars = self.client.klines(
                symbol=self.symbol, interval=self.interval, startTime=start_time, limit=_limit
            )
            klines += bars

            # Set start_time to the next timestamp after the last bar in the previous chunk
            start_time = int(bars[-1][0] + interval_time)
            tmp_limit -= 1000

        # Convert data to pandas DataFrame
        df = pd.DataFrame(klines, columns=enums.COLUMNS)
        df = df_normalize(df)
        # df["time_open"] = pd.to_datetime(df["time_open"], unit="ms")
        # df.set_index("time_open", inplace=True)

        return df

    def _manager(self):
        global df_global
        df_global[self.symbol] = self.load_historical_data()
        self.df = self.load_historical_data()
        if self._rt:
            self.stream_data()

    def _handler(self, message):
        global df_global
        if message is None:
            return

        # выбор данных свечи из входных данных
        data = message.get('k')
        if data is None:
            return

        symbol = data['s']
        _tmp_df_global = df_global[symbol]

        # преобразование входных данных в DataFrame
        _df = self._adapter(data)

        if _tmp_df_global is not None:
            # 't' - время открытия свечи, в DataFrame это 'time_open'
            _dfi = data['t']
            # получение списка всех индексов в DataFrame, т.е. всех имеющихся 'time_open'
            _gli = _tmp_df_global.index.to_list()
            if _dfi not in _gli:
                # новая свеча, присоединяем ее
                logger.info('+++ add')
                _tmp_df_global = pd.concat([_tmp_df_global, _df], join='outer')
                df_global[self.symbol] = _tmp_df_global
            else:
                # обновление уже имеющейся свечи
                logger.info('*** update')
                _tmp_df_global.update(_df, overwrite=True)
                df_global[self.symbol] = _tmp_df_global
        else:
            raise Exception('<_tmp_df_global> doesnt be None', _tmp_df_global)

        # logger.info(f"_tmp_df_global \n{_tmp_df_global.tail(3)}")
        # logger.info('='*30)
        # logger.info(f"df_global {df_global.get(self.symbol).tail(3)}")
        # logger.info(f"df_global {df_global.get(self.symbol)['close'].to_list()[-1]}")

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

    def _ma_calculate(self):
        pass

    def _time_now(self):
        return int(time.time()) * 1000


if __name__ == '__main__':
    # loader = BinanceDataLoader(interval='15m', limit=3, real_time=False)
    #
    # df = df_global['BTCUSDT'].to_dict()
    # # pd.DataFrame.to
    # print(df)

    # df = loader.load_historical_data()
    # print(df.dtypes)
    # print(df.head())
    #
    # print(datetime.utcfromtimestamp(time.time_ns() / 1000000000))
    # print(datetime.utcfromtimestamp(int(time.time_ns() / 1000000000)))

    # client = Client(test_mode=False)
    # print(Client.KLINE_INTERVAL_1HOUR)
    # for param in client.__dir__():
    #     print(param)

    periods = [5, 13, 34]
    df = pd.DataFrame({'open': {1679320800000: 27821.17, 1679321700000: 27936.88, 1679322600000: 27990.92},
                       'close': {1679320800000: 27936.88, 1679321700000: 27992.55, 1679322600000: 27950.27},
                       'ignore': {1679320800000: 0, 1679321700000: 0, 1679322600000: 0},
                       'ema_5': {1679320800000: 27924.17, 1679321700000: 27986.88, 1679322600000: 27991.92},
                       'ema_13': {1679320800000: 27913.17, 1679321700000: 27946.88, 1679322600000: 27980.92},
                       'ema_34': {1679320800000: 27898.17, 1679321700000: 27938.08, 1679322600000: 27971.12}})

    new_df = pd.DataFrame({'open': {1679323500000: 27821.17, 1679324400000: 27936.88, 1679325300000: 27990.92},
                           'close': {1679323500000: 27936.88, 1679324400000: 27992.55, 1679325300000: 27950.27},
                           'ignore': {1679323500000: 0, 1679324400000: 0, 1679325300000: 0}})

    # print(new_df.index[0])
    print(df.iloc[0]['close'])
    print(df.loc[df.index[0], 'close'])
    # EMA = close(t)×k + EMA(y)×(1−k)
    #
    # where:
    # close(t) = цена закрытия текущего бара
    # EMA(y) = значение EMA предыдущего бара
    # k = 2÷(N + 1)

    # N = значение периода EMA, одно из значений 'periods'

    # df = pd.concat([df, new_df])
    #
    # for period in periods:
    #     k = 2 / (period + 1)
    #     previous_ema = df[f'ema_{period}'][df.index[-1]]
    #     for i, row in new_df.iterrows():
    #         close = row['close']
    #         new_ema = close * k + previous_ema * (1 - k)
    #         new_df.loc[i, f'ema_{period}'] = new_ema
    #         previous_ema = new_ema
    #     df = pd.concat([df, new_df])
    #
    # print(df.tail())


