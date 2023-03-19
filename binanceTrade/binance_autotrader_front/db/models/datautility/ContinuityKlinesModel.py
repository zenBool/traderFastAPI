from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from model.get_connect import get_engine

Base = declarative_base()


class ContinuityKlinesModel(Base):
    """
    Last Continuity Control
    """
    __tablename__ = "cntnt_klines"

    id = Column(Integer, primary_key=True)
    tablectrl = Column(String, nullable=False)
    needcandle = Column(BigInteger, nullable=False, comment='Time Open the candle is need')
    lastctrl = Column(BigInteger, nullable=False, default=1640995200000, comment='Last control time')


if __name__ == '__main__':
    engine = get_engine()
    session = sessionmaker(engine)()

    tbl = ContinuityKlinesModel()

    Base.metadata.create_all(engine)