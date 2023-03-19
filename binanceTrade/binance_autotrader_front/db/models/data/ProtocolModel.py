from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProtocolModel(Base):
    __tablename__ = 'protocol'
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "%s" % (
            self.__class__.__name__
        )
