from dataclasses import dataclass
import pandas as pd


@dataclass
class KlineSymbol:
    """

    """

    df: pd.DataFrame = None
    update: int = None

    def adapter_wss(self, data: dict):
        """Method adapter web socket stream data to pandas.DataFrame

        """

        data = test_data if data is None else data

        dataframe_format = {
            'time_open': [data['t']],
            'open': [float(data['o'])],
            'high': [float(data['h'])],
            'low': [float(data['l'])],
            'close': [float(data['c'])],
            'volume': [float(data['v'])],
            'time_close': [data['T']],
            'q_asset_vol': [float(data['q'])],
            'num_trades': [data['n']],
            'tb_base_av': [float(data['V'])],
            'tb_quote_av': [float(data['Q'])],
            'ignore': [int(data['B'])]
        }

        df = pd.DataFrame(dataframe_format, columns=dataframe_format.keys())

        return df


if __name__ == '__main__':
    test_data = {'t': 1659798240000, 'T': 1659781079999, 's': 'BTCUSDT', 'i': '1m', 'f': 146705,
                 'L': 146757, 'o': '6.17000000', 'c': '23197.50000000', 'h': '23199.14000000',
                 'l': '23196.17000000', 'v': '2.45011400', 'n': 53, 'x': False, 'q': '56836.65111634',
                 'V': '1.10623200', 'Q': '25661.94302789', 'B': '0'}
    kline = KlineSymbol()
    df = kline.adapter_wss(test_data)
    print(df.info())

