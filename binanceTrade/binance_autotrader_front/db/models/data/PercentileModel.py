from sqlalchemy import Float, Integer, String, Column, Boolean, TIME
from binanceTrade.db import BaseMixin, Base


class PercentileModel(BaseMixin, Base):
    """Percentile Delta EMA

    """
    __tablename__ = 'percentile_ema'

    symbol = Column(String, nullable=False)
    interval = Column(String, nullable=False)
    start = Column(Tim)
