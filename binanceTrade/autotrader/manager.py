import sys
import time
from typing import List, Any

from loguru import logger
from pydantic import BaseModel

from binance_autotrader import Client, ClientWS, enums
from binance_autotrader.data_store import data_store

from binance_autotrader.func import get_klines_tablename

from dotenv import load_dotenv

from autotrader_front.db import get_engine


def counter():
    count = 0

    def _next():
        nonlocal count
        count += 1
        return count
    return _next


class StreamManager(BaseModel):
    symbols: List[str] = []
    intervals: List[str] = []
    _streams: dict = {}

    nextID: Any = None
    client: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nextID = counter()
        self.client = ClientWS(test_mode=False)
        self.client.start()

    def handler(self, message):
        # <message> format data in combined stream
        #
        # {
        #  "stream": "<streamName>",
        #  "data": {
        #       "e": "kline",     // Event type
        #       "E": 123456789,   // Event time
        #       "s": "BNBBTC",    // Symbol
        #       "k": { <kline_data> }
        #  }
        # }

        kline_name = self._streamName_to_SymbolKlineName(message['stream'])

        symbol_kline = data_store.storage.get(kline_name)
        symbol_kline.update(message['data'].get('k'))

    def _streamName_to_SymbolKlineName(self, streamName: str):
        symbol = streamName.split('@')[0]
        interval = streamName.split('_')[1]
        return f'{symbol.upper()}_{interval}'

    def start(self, stream):
        if isinstance(stream, list):
            stream = ["{}@kline_{}".format(x.split('_')[0].lower(), x.split('_')[1]) for x in stream]
        else:
            stream = ["{}@kline_{}".format(stream.split('_')[0].lower(), stream.split('_')[1])]

        self.client.instant_subscribe(
            stream=stream,
            callback=self.handler,
        )

    def stop(self):
        self.client.stop()


class Manager(BaseModel):
    # Get all configs
    symbols: list = ['BTCUSDT', 'BNBUSDT', 'MAGICUSDT', 'ADAUSDT', 'ETHUSDT', 'XRPUSDT', 'DOTUSDT', 'XMRUSDT', 'DASHUSDT', 'LTCUSDT'] #
    intervals: list = ['3m', '15m', '1h']
    ema_periods: list = [5, 13, 34]
    data_store: Any = None
    stream_manager: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data_store = data_store
        self.stream_manager = StreamManager()

    def start(self):
        for symbol in self.symbols:
            for interval in self.intervals:
                kline_name = self.data_store.add(symbol, enums.Interval(name=interval), self.ema_periods)
                self.stream_manager.start(kline_name)
                logger.info(f"{kline_name} kline stream subscribe")
                logger.info(f"{len(self.data_store.storage.keys())} streams working")

    def stop(self):
        self.stream_manager.stop()
        time.sleep(5)
        logger.info("closing ws connection.\nExit.")
        sys.exit()


if __name__ == '__main__':
    load_dotenv('/home/jb/PyProjects/binanceTradeFAPI/binanceTrade/.env')
    manager = Manager()
    try:
        manager.start()
        logger.info("Load and start stream for all symbols")

        # raise BaseException
    except KeyboardInterrupt:
        manager.stop()
        pass
    finally:
        pass
    for _ in range(10):
        logger.info('{}in loop{}'.format('>'*30, '<'*30))
        df = manager.data_store.storage['ADAUSDT_3m'].dfKline
        ema0 = round(df['ema_5'].iloc[-1], 2)
        ema1 = round(df['ema_5'].iloc[-2], 2)
        logger.info("ADAUSDT_3m ema_5={} <> {}".format(ema0, ema1))
        time.sleep(3)

    manager.stop()

