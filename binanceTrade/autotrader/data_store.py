import time

import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.typing import Literal
from loguru import logger

from binance_autotrader import enums
from binance_autotrader.data_loader import load_historical_data


class SymbolKline(BaseModel):
    symbol: str
    interval: enums.Interval
    dfKline: pd.DataFrame = None
    last_update: int = None
    name: str = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.name = f'{self.symbol}_{self.interval.name}'

        if self.dfKline is None:
            """Load data from server/DB
            """
            self.dfKline = load_historical_data(symbol=self.symbol, interval=self.interval.name, limit=1000)
            self._check_data_integrity()

        self.last_update = int(time.time() * 1000)

    def _check_data_integrity(self):
        """Checking data continuity by 'time_open'

        :return:
        :rtype:
        """
        list_time_open = tuple(self.dfKline['time_open'].to_list())
        for i in range(1, len(list_time_open)):
            if list_time_open[i] != list_time_open[i-1] + self.interval.ms:
                raise ValueError("The integrity of the data is violated")


class SymbolKlineWithEMA(SymbolKline):
    short: int
    middle: int
    long: int = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._ema_calculate()

    def _get_ema(self, index: int, period: int):
        """Get values MAs for 'index'. Last line have 'index' = 0

        :param index: 0 - value now, 1 - value previous bar ...
        :type index: int
        :param period: self.short or self.middle or self.long
        :type period: int
        :return: value MA with :period: and (len(df.index)-index)
        :rtype: float
        """
        col = f'ema_{period}'
        return self.dfKline[col].iloc[-index - 1]

    def shortEMA(self, index: int):
        return self._get_ema(index, self.short)

    def middleEMA(self, index: int):
        return self._get_ema(index, self.middle)

    def longEMA(self, index: int):
        return self._get_ema(index, self.long)

    def update(self, data: dict):
        """Recieving data from WSS and update :self.dfKline:

        :param data:
        :type data:
        """

        new_row = {
            'time_open': data.get('T'),
            'open': float(data.get('o')),
            'high': float(data.get('h')),
            'low': float(data.get('l')),
            'close': float(data.get('c')),
            'volume': float(data.get('v')),
            'time_close': data.get('T'),
            'q_asset_vol': float(data.get('q')),
            'num_trades': data.get('n'),
            'tb_base_av': float(data.get('V')),
            'tb_quote_av': float(data.get('Q')),
            'ignore': data.get('B')
        }

        def _ema(period, close, previous):
            k = 2 / (period + 1)
            ema = close * k + previous * (1 - k)
            return ema

        _close = new_row.get('close')
        df = self.dfKline
        # New EMA values add to data from stream
        for period in (self.short, self.middle, self.long):
            # Previous EMA value take
            previous = df.loc[df['time_open'] == data.get('t') - self.interval.ms, f'ema_{period}'].values[0]
            new_row[f'ema_{period}'] = \
                _ema(
                    period,
                    _close,
                    previous
                )

        if new_row['time_open'] not in self.dfKline['time_open'].values:
            # Add row
            self.dfKline = pd.concat([self.dfKline, pd.DataFrame(new_row, index=[0])], join='outer', ignore_index=True)
        else:
            # Update row
            self.dfKline.update(pd.DataFrame(new_row, index=[df.loc[df['time_open'] == new_row['time_open']].index[0]]),
                      overwrite=True)
        # logger.debug(self.name)
        # logger.debug(self.dfKline.tail(1))


    def _ema_calculate(self):
        """DataFrame must have int index for iteration

        :return:
        :rtype:
        """

        for period in (self.short, self.middle, self.long):
            if period is None:
                continue
            k = 2 / (period + 1)
            self.dfKline[f'ema_{period}'] = None
            self.dfKline[f'ema_{period}'] = self.dfKline[f'ema_{period}'].astype('float')

            previous_ema = self.dfKline.iloc[0]['close']
            for i, row in self.dfKline.iterrows():
                close = row['close']
                new_ema = close * k + previous_ema * (1 - k)
                self.dfKline.loc[i, f'ema_{period}'] = new_ema
                previous_ema = new_ema

        # self.df_list.append(df)
        # return df


class DataStore(BaseModel):
    # <storage> format:
    # { "<symbol_kline.name>" : SymbolKline, } <symbol_kline.name> have format "BTCUSDT_15m"
    storage: dict = {}
    _list_id: list[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def add(self, symbol, interval, ma):
        symbol_kline = SymbolKlineWithEMA(
            symbol=symbol,
            interval=interval,
            short=ma[0],
            middle=ma[1],
            long=ma[2]
        )
        self.storage[symbol_kline.name] = symbol_kline
        return symbol_kline.name


data_store = DataStore()


if __name__ == '__main__':
    symbol = SymbolKlineWithEMA(symbol='BTCUSDT', interval=enums.Interval(name='15m'), short=5, middle=13)
    symbol2 = SymbolKlineWithEMA(symbol='BNBUSDT', interval=enums.Interval(name='15m'), short=5, middle=13)
    store = DataStore()
    store.add(symbol)
    store.add(symbol2)

    df = store.storage.get(symbol.name)
    print(df.shortMA(1))

    print(store.storage.get(symbol.name).dfKline.tail(2))


