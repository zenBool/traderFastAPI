from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SymbolsGroupModel(Base):
    __tablename__ = 'all_paths'
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "%s" % (
            self.__class__.__name__
        )
