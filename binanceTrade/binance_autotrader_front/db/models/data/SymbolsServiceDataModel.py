from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SymbolsServiceDataModel(Base):
    __tablename__ = 'symbols_service_data'

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    interval = Column(String)
    first_time = Column(Integer, comment='The first time(ms) in the table')
    last_time = Column(Integer, comment='The last time(ms) in the table')
    continuity_last_time = Column(Integer, comment='Last time of continuity interval from first to last')
    symbols_service_data_symbol_interval_key = UniqueConstraint(symbol, interval)

    def __repr__(self):
        return "%s" % (
            self.__class__.__name__
        )


if __name__ == '__main__':
    pass
