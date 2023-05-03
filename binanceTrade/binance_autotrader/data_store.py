import time

import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.typing import Literal

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


class SymbolKlineWithMA(SymbolKline):
    short: int
    middle: int
    long: int = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._ema_calculate()

    def ma(self, index: int):
        """Get values MAs for 'index'. Last line have 'index' = 0

        :param index: 0 - value now, 1 - value previous bar ...
        :type index: int
        :return: return values short, middle, long for 'index' value
        :rtype: tuple
        """
        pass
        # return (short, middle, long)

    def update(self, data: dict):
        """Recieving data from WSS and update :self.dfKline:

        :param data:
        :type data:
        :return:
        :rtype:
        """
        pass

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
    storage: SymbolKline | List[SymbolKline]
    _list_id: list[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._list_id.append(self.storage.name)

    def add(self, symbol_kline: SymbolKline):
        if isinstance(self.storage, list):

            self.storage.append(symbol_kline)


if __name__ == '__main__':
    symbol = SymbolKlineWithMA(symbol='BTCUSDT', interval=enums.Interval(name='15m'), short=5, middle=13)
    # symbol = SymbolKline(symbol='BTCUSDT', interval=enums.Interval(name='1m'))
    print(symbol.interval.ms)
    print(symbol.last_update)
    print(symbol.dfKline.tail(2))
    print(symbol.dfKline.info())
