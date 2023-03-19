import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.typing import Literal

from binance_autotrader import enums


class Interval(BaseModel):
    name: Literal[*enums.INTERVALS]
    ms: enums.IntervalValueEnum = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ms = getattr(enums.IntervalValueEnum, enums.IntervalNameEnum(self.name).name).value


class SymbolKline(BaseModel):
    symbol: str
    interval: Interval
    dfkline: pd.DataFrame = None
    last_update: int = None
    id: str = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = f'{self.symbol}_{self.interval.name}'
        if self.dfkline is None:



class DataStore(BaseModel):
    storage: SymbolKline | List[SymbolKline]
    _list_id: list[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._list_id.append(self.storage.id)

    def add(self, symbol_kline: SymbolKline):
        if isinstance(self.storage, list):

            self.storage.append(symbol_kline)


if __name__ == '__main__':
    symbol = SymbolKline(symbol='BTCUSDT', interval=Interval(name='1m'))
    print(symbol.interval.name)