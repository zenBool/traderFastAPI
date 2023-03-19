import sys
from loguru import logger
import pandas as pd

from binance_autotrader import Client, ClientWS, enums

from trade.bEx.functions import get_klines_tablename

from dotenv import load_dotenv

from binance_autotrader_front.db import get_engine

load_dotenv('/home/jb/PycharmProjects/binanceTradeDj/binanceTrade/.env')

logger.add(sys.stderr, format="{time} {level} {message}", filter="tests", level="INFO")

engine = get_engine(echo=False)


def handler(message):
    global df_wss
    data = message.get('k')
    if data is None:
        return

    symbol = data['s']
    global_df = df_wss[symbol]

    _df = adapter(data)

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


def get_kline(symbol: str, interval: str, limit: int = 3):
    client = Client()
    limit = 100 if limit is None else limit

    columns = enums.COLUMNS

    df = pd.DataFrame(client.klines(symbol, interval, limit=limit), columns=columns)
    df = df.set_index('time_open')

    return df


def adapter(data: dict = None):
    # Data example
    sf = {'t': 1659798240000, 'T': 1659781079999, 's': 'BTCUSDT', 'i': '1m', 'f': 146705,
          'L': 146757, 'o': '6.17000000', 'c': '23197.50000000', 'h': '23199.14000000',
          'l': '23196.17000000', 'v': '2.45011400', 'n': 53, 'x': False, 'q': '56836.65111634',
          'V': '1.10623200', 'Q': '25661.94302789', 'B': '0'}

    if data is None:
        return

    dataframe_format = {
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

    df = pd.DataFrame(dataframe_format, index=[data.get('t')])

    return df


def load_df(symbol: str, interval: str, isMA: bool) -> pd.DataFrame:
    table = get_klines_tablename(symbol, interval, isMA)

    df = pd.read_sql_table(table, engine)
    df = pd.read_sql()

    return df


if __name__ == '__main__':
    df_wss = {}
    sBTC = 'BTCUSDT'
    sETH = 'ETHUSDT'
    sBNB = 'BNBUSDT'

    symbol = sBNB
    symbols = [sBTC, sETH, sBNB]
    interval = '1m'
    for symbol in symbols:
        df_wss[symbol] = get_kline(symbol, interval)

    client_ws = ClientWS()
    client_ws.start()
    logger.info("open ws connection")

    try:
        for symbol in symbols:
            client_ws.kline(symbol=symbol, id=2, interval=interval, callback=handler)
            logger.info(f"{symbol} kline stream subscribe")

        while True:
            pass

    except KeyboardInterrupt:
        ...
    finally:
        logger.info("closing ws connection")
        client_ws.stop()
