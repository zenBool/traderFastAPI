from sqlalchemy import Column, Float, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from trade.bEx.models.data.KlinesModel import KlinesModel

Base = declarative_base()


class ModelMA(object):
    """Base class is a 'mixin'.
    Guidelines for declarative mixins is at:
    http://www.sqlalchemy.org/docs/orm/extensions/declarative.html#mixin-classes
    """
    id = Column(Integer, primary_key=True)
    ma_5 = Column(Float, nullable=False)
    ma_8 = Column(Float, nullable=False)
    ma_13 = Column(Float, nullable=False)
    ma_21 = Column(Float, nullable=False)
    ma_34 = Column(Float, nullable=False)
    ma_55 = Column(Float, nullable=False)
    ma_89 = Column(Float, nullable=False)
    ma_144 = Column(Float, nullable=False)
    ma_5_delta = Column(Float, nullable=False)
    ma_8_delta = Column(Float, nullable=False)
    ma_13_delta = Column(Float, nullable=False)
    ma_21_delta = Column(Float, nullable=False)
    ma_34_delta = Column(Float, nullable=False)
    ma_55_delta = Column(Float, nullable=False)
    ma_89_delta = Column(Float, nullable=False)
    ma_144_delta = Column(Float, nullable=False)

    def __repr__(self):
        return "%s" % (
            self.__class__.__name__
        )


class MAModel:
    @staticmethod
    def create_type(_tablename: str, _Base, type_ma=1) -> (ModelMA, Base):
        if type_ma == 1:
            return type(f"{_tablename}_ema", (ModelMA, _Base),
                        {
                            "__tablename__": f"{_tablename}_ema",
                            "time_open": Column(BigInteger, ForeignKey(f"{_tablename}.time_open")),
                            "candle": relationship(f"{_tablename}", backref=backref(f"{_tablename}_ema", uselist=False))
                        })
        else:
            return None


if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker, backref
    from trade.bEx.db.get_connect import get_engine

    tablename = "klines_1inchusdt_1d"
    KlinesClass = KlinesModel.create_type(tablename, Base)

    MAClass = MAModel.create_type(tablename, Base)

    engine = get_engine()
    Base.metadata.create_all(engine)
    sess = sessionmaker(engine)()

    # sess.add_all([kl(time_open = 123456795003, open = 1.123456, high = 1.234567, low = 1.012345, close = 1.123789, volume = 2.2,
    #     time_close = 123456795003, q_asset_vol = 1.234560, num_trades = 23, tb_base_av = 1.222222, tb_quote_av = 1.111222, ignore = 0, data='t2')])
    #
    # sess.commit()

    print('-' * 50)
    print(type(MAClass))
    # rows = sess.query(ema_instance).all()
    # rows = sess.query(KlinesModel.create_type(tablename)).all()
    # for idx in range(0, 100):
    # print(type(rows[0].close))
    # print(ema_instance[0].close)
    print('-' * 50)
