from datetime import datetime
from typing import Dict, List

from sqlalchemy.orm import Session

# from .binance_api_manager import BinanceAPIManager
# from .config import Config
# from autotrader.config import Config
# from autotrader.clients import Client
#
# from autotrader.database import Database
from autotrader.logger import Logger
# from autotrader.models import Coin, CoinValue, Pair


class AutoTrader:
    # def __init__(self, binance_manager: Client, database: Database, logger: Logger, config: Config):
    def __init__(self, logger: Logger):
    #     self.manager = binance_manager
    #     self.db = database
        self.logger = logger
    #     self.config = config

    def initialize(self):
        self.initialize_datastore()

    def buy(self):
        pass

    def sell(self):
        pass

    def initialize_datastore(self):
        pass

    def scout(self):
        """
        Scout for potential jumps from the current coin to another coin
        """
        raise NotImplementedError()

    # def update_values(self):
    #     """
    #     Log current value state of all altcoin balances against BTC and USDT in DB.
    #     """
    #     now = datetime.now()
    #
    #     session: Session
    #     with self.db.db_session() as session:
    #         coins: List[Coin] = session.query(Coin).all()
    #         for coin in coins:
    #             balance = self.manager.get_currency_balance(coin.symbol)
    #             if balance == 0:
    #                 continue
    #             usd_value = self.manager.get_ticker_price(coin + "USDT")
    #             btc_value = self.manager.get_ticker_price(coin + "BTC")
    #             cv = CoinValue(coin, balance, usd_value, btc_value, datetime=now)
    #             session.add(cv)
    #             self.db.send_update(cv)


if __name__ == '__main__':
    import sys


    class Test:
        def func(self):
            print(f'Print from {sys._getframe().f_code.co_name}')


    test = Test()
    print(test.func())