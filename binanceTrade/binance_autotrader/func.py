import sys
from typing import Literal

import pandas as pd
import numpy as np

from . import enums


def history_dir() -> str:
    return '/home/jb/binance/data/spot/daily/klines'


def convert_time_open(df: pd.DataFrame, to: Literal['datetime', 'int64']) -> pd.DataFrame:
    """
    Конвертация представления времени <Binance Time> << = >> <pandas.DateTime>
    @param df: pandas.DataFrame
    @param to: Направление конвертации, к какому виду необходимо привести
    @return: pandas.DataFrame
    """
    try:
        # """Проверяем на валидность к Binance DF"""
        # clmns = df.columns.to_list()
        # for el in enums.COLUMNS:
        #     if el not in clmns:
        #         print('Column name:', el)
        #         print(clmns.__str__())
        #         raise TypeError('Incoming DataFrame does not match Binance DF')

        type_time_open = df['time_open'].dtype.__str__()
        if type_time_open == 'datetime64[ns]' and to == 'int64':
            df['time_open'] = df['time_open'].astype('int64').div(1000000).astype(int)
            df['time_close'] = df['time_close'].astype('int64').div(1000000).astype(int).add(999)
            return df
        elif type_time_open == 'int64' and to == 'datetime':
            df['time_open'] = df['time_open'].div(1000).astype(int)
            df['time_open'] = pd.to_datetime(df['time_open'], unit='s')
            df['time_close'] = df['time_close'].div(1000).astype(int)
            df['time_close'] = pd.to_datetime(df['time_close'], unit='s')
            return df
        else:
            return df
    except TypeError as e:
        sys.exit(e)
    except BaseException as e:
        sys.exit(e)


def cut_start_df(_df: pd.DataFrame, starttime: int) -> pd.DataFrame:
    """Отбрасывание начальных данных до <starttime>

        ПЕРЕДЕЛАТЬ
        индекс для удаления может отличаться от порядкового номера строки

    @param _df:
    @param starttime:
    @return:
    """
    delidx = []
    tset = _df['time_open'].copy().to_list()
    for i in range(0, len(tset)):
        if np.int64(tset[i]) >= starttime:
            break
        else:
            delidx.append(i)
    _df = _df.drop(axis=0, index=delidx, inplace=False)
    return _df


def cut_df_empty_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    Отбрасывания начальных данных до ближайшего начала часа
    @param df:
    @return:
    """
    delidx = []
    tset = df['time_close'].to_list()
    for i in range(0, len(tset)):
        if tset[i] < 0:
            delidx.append(i)
    df = df.drop(axis=0, index=delidx, inplace=False)
    df = df.reset_index()
    return df


def df_resample(_df: pd.DataFrame, to: str, on: str = 'time_open') -> pd.DataFrame:
    """

    @param _df:
    @param to:
    @param on:
    @return:
    """
    conversion = {
        # 'time_open': 'first',
        'open': 'first',
        'close': 'last',
        'high': 'max',
        'low': 'min',
        'volume': 'sum',
        'time_close': 'last',
        'q_asset_vol': 'sum',
        'num_trades': 'sum',
        'tb_base_av': 'mean',
        'tb_quote_av': 'mean',
        'ignore': 'sum'
    }
    _df = convert_time_open(_df, to='datetime')
    _df_ = _df.resample(to, on=on).agg(conversion)
    _df = _df_.reset_index()
    _df = convert_time_open(_df, 'int64')
    _df = _df[enums.COLUMNS]

    return _df


def df_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize <df> to standard Binance klines DF"""
    columns = enums.COLUMNS

    # df['time_open'] = df['time_open'].astype('int64')
    df['open'] = df['open'].astype('float')
    df['high'] = df['high'].astype('float')
    df['low'] = df['low'].astype('float')
    df['close'] = df['close'].astype('float')
    df['volume'] = df['volume'].astype('float')
    # df['time_close'] = df['time_close'].astype('int64')
    df['q_asset_vol'] = df['q_asset_vol'].astype('float')
    # df['num_trades'] = df['q_asset_vol'].astype('int')
    df['tb_base_av'] = df['tb_base_av'].astype('float')
    df['tb_quote_av'] = df['tb_quote_av'].astype('float')
    df['ignore'] = df['ignore'].astype('int8')

    # df = df.sort_values('time_open', ignore_index=True)
    # df.reindex(copy=False)
    df = df[columns]

    return df


def get_cross_df(df_numerator_: pd.DataFrame = None, df_denominator_: pd.DataFrame = None) -> pd.DataFrame:
    if df_numerator_ is None or df_denominator_ is None:
        raise Exception('Data is exist.')
    df = pd.merge(df_numerator_, df_denominator_, how='inner', on=['time_open', 'time_close'], sort=False,
                  suffixes=('_n', '_d'))
    df['open'] = round(df['open_n'].div(df['open_d']), 8)
    df['close'] = round(df['close_n'].div(df['close_d']), 8)
    df['high'] = df[['open', 'close']].max(axis=1)
    df['low'] = df[['open', 'close']].min(axis=1)
    df['volume'] = -1
    df['q_asset_vol'] = -1
    df['num_trades'] = -1
    df['tb_base_av'] = -1
    df['tb_quote_av'] = -1
    df['ignore'] = 0

    df = df[enums.COLUMNS]

    return df


def get_cross_tablename(symbol1: str = None, symbol2: str = None, interval: str = None, ema: bool = False) -> str:
    if symbol1 is None or symbol2 is None:
        raise Exception('<symbol1> or/and <symbol2> not specified')
    elif symbol1 not in enums.SYMBOLS_AMPLITUDE_USDT:
        raise Exception(f'Wrong <symbol> {symbol1}')
    elif symbol2 not in enums.SYMBOLS_AMPLITUDE_USDT:
        raise Exception(f'Wrong <symbol> {symbol2}')
    else:
        pair = sorted([symbol1[:-4], symbol2[:-4]])
        name = f'{pair[0]}_{pair[1]}'.lower()
        tablename = f'klines_cross_{name}_{interval}' if not ema else f'klines_cross_{name}_{interval}_ema'

    return tablename


def get_cross_tables(
        symbols: list = None,
        intervals: list | tuple = enums.INTERVALS,
        ema: bool = False
):
    """
    Получение списка имен всех таблиц к удалению
    @param symbols: список пар USDT | BUSD по которым составлять кросы
    @param ema: True если нужны ЕМА таблицы кросов
    @param intervals:
    @return: список всех возможных кросов
    """
    symbols = symbols or sorted(enums.SYMBOLS_AMPLITUDE_USDT)

    if len(symbols) < 2:
        raise ValueError('Method needed two pair in <symbols> minimum')

    crosses_list = []
    while len(symbols) > 1:
        symbol1 = symbols.pop(0)
        for symbol2 in symbols:
            for interval in intervals:
                crosses_list.append(get_cross_tablename(symbol1, symbol2, interval=interval, ema=ema))
    return crosses_list


def get_klines_tablename(symbol: str = None, interval: str = '1m', isMA: bool = False) -> str:
    if symbol is None:
        raise Exception('<symbol> not specified')
    elif symbol not in enums.SYMBOLS:
        raise Exception(f'Wrong <symbol> {symbol}')
    else:
        name = f'klines_{symbol.lower()}_{interval}'

    if isMA:
        name += '_ema'

    return name


def get_spot_klines_as_pd(client=None, symbol: str = None, interval: enums.INTERVALS = None, limit: int = None):
    """
    Load klines data from server for <symbol> and <interval>
    Converts object(string) data to numeric
    return pandas.DataFrame()
    """
    if client is None:
        raise Exception('It must specify <client> for connection to Binance server')

    if symbol is None:
        raise Exception('It must specify <symbol>')

    if interval is None:
        raise Exception('It must specify <interval>')

    limit = 500 if limit is None else limit

    columns = ['time_open', 'open', 'high', 'low', 'close', 'volume', 'time_close', 'q_asset_vol',
               'num_of_trades', 'tb_base_av', 'tb_quote_av', 'ignore']

    # print('in method', symbol)
    df = pd.DataFrame(client.klines(symbol, interval, limit=limit), columns=columns)

    df['open'] = df['open'].astype('float')
    df['high'] = df['high'].astype('float')
    df['low'] = df['low'].astype('float')
    df['close'] = df['close'].astype('float')
    df['volume'] = df['volume'].astype('float')
    df['q_asset_vol'] = df['q_asset_vol'].astype('float')
    df['tb_base_av'] = df['tb_base_av'].astype('float')
    df['tb_quote_av'] = df['tb_quote_av'].astype('float')

    return df


def get_coins_from_cross(cross: str):
    base_coin: str = ''
    quote_coin: str = ''
    return base_coin, quote_coin


def write_crossdf_to_csv_zip(df: pd.DataFrame, symbol1: str = None, symbol2: str = None, interval: str = None):
    """

    @param df:
    @param symbol1:
    @param symbol2:
    @param interval:
    @return:
    """
    folder = '/home/jb/binance/ema'
    # path1 = f'{folder}/{symbol1.upper()}/{interval}/{symbol1.upper()}-{interval}-{day}.zip'

    # path2 = f'{folder}/{symbol2.upper()}/{interval}/{symbol2.upper()}-{interval}-{day}.zip'
    # if not os.path.exists(path1) or not os.path.exists(path2):
    #     print('No file {} or {}'.format(path1, path2))
    #     return

    cross_name = f'cross_{symbol1[:-4].upper()}_{symbol2[:-4].upper()}'
    # os.makedirs(f'{folder}/{cross_name}/{interval}', mode=0o777, exist_ok=True)

    # date = str(today().date())

    path_cross = f'{folder}/{cross_name}-{interval}-to-29092022.zip'
    # path_cross = f'{folder}/{cross_name}/{interval}/{cross_name}-{interval}-{date}.zip'

    # if os.path.exists(path_cross):
    #     return
    #
    # df1 = pd.read_csv(path1, names=self.df_columns, compression='zip')
    # df2 = pd.read_csv(path2, names=self.df_columns, compression='zip')
    # df_cross = self.get_cross_df(df1, df2)
    compression_opts = dict(method='zip', archive_name=f'{cross_name}-{interval}-to-23092022.csv')
    # compression_opts = dict(method='zip', archive_name=f'{cross_name}-{interval}-{date}.csv')
    df.to_csv(path_cross, header=False, index=False, compression=compression_opts)

    print(f'Write file {path_cross}')
