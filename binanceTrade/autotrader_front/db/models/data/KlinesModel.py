from sqlalchemy import Column, Float, Integer, BigInteger, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class ModelKlines(object):
    """Base class is a 'mixin'.
    Guidelines for declarative mixins is at:
    http://www.sqlalchemy.org/docs/orm/extensions/declarative.html#mixin-classes

    """
    time_open = Column(BigInteger, unique=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float)
    time_close = Column(BigInteger, unique=True)
    q_asset_vol = Column(Float, comment='Quote asset volume')
    num_trades = Column(Integer)
    tb_base_av = Column(Float, comment='Taker buy base asset volume')
    tb_quote_av = Column(Float, comment='Taker buy quote asset volume')
    ignore = Column(SmallInteger)
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "%s" % (
            self.__class__.__name__
        )


class ModelKlinesTMP(object):
    """Base class is a 'mixin'.
    Guidelines for declarative mixins is at:
    http://www.sqlalchemy.org/docs/orm/extensions/declarative.html#mixin-classes

    """
    time_open = Column(BigInteger, primary_key=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float)
    time_close = Column(BigInteger, unique=True)
    q_asset_vol = Column(Float, comment='Quote asset volume')
    num_trades = Column(Integer)
    tb_base_av = Column(Float, comment='Taker buy base asset volume')
    tb_quote_av = Column(Float, comment='Taker buy quote asset volume')
    ignore = Column(SmallInteger)

    def __repr__(self):
        return "%s" % (
            self.__class__.__name__
        )


class KlinesModel:
    """Generate class with type()

    """
    @staticmethod
    # def create_type(_tablename: str, _Base) -> (ModelKlines, declarative_base):
    def create_type(tablename: str, Base):
        """

        @param tablename: Name of table in DB
        @param Base: declarative_base()
        @return:

        """
        return type(tablename, (ModelKlines, Base), {"__tablename__": tablename})


class KlinesTMPModel:
    # generate class with type()
    @staticmethod
    # def create_type(_tablename: str, _Base) -> (ModelKlines, Base):
    def create_type(_tablename: str, _Base):
        return type(f"{_tablename}", (ModelKlinesTMP, _Base), {"__tablename__": f"{_tablename}"})


if __name__ == '__main__':
    from binanceTrade.db import Base, current_session

    from dotenv import load_dotenv
    load_dotenv()

    tablename = "klines_1inchusdt_1m"

    inchusdt_1m = KlinesModel.create_type(tablename, Base)

    sess = current_session()

    # sess.add_all([kl(time_open = 123456795003, open = 1.123456, high = 1.234567, low = 1.012345, close = 1.123789, volume = 2.2,
    #     time_close = 123456795003, q_asset_vol = 1.234560, num_trades = 23, tb_base_av = 1.222222, tb_quote_av = 1.111222, ignore = 0, data='t2')])
    #
    # sess.commit()

    print('-'*50)
    # print(type(inchusdt_1m))
    # print(inchusdt_1m)
    rows = sess.query(inchusdt_1m).all()
    for idx in range(0, 10):
        print(rows[idx].close)
    print('-'*50)
