from sqlalchemy import Integer, String, Column, Boolean

from binanceTrade.db import Base
from binanceTrade.db import BaseMixin


class CoinMarketCapModel(Base, BaseMixin):
    __tablename__ = 'market_cap'
