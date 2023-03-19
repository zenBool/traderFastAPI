from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from trade.bEx.db.get_connect import get_engine

Base = declarative_base()


class MarginSnapshotModel(Base):
    __tablename__ = "snapshot_mrg_acc"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    updateTime = Column(BigInteger, unique=True)

    data = relationship("MarginSnapshotDataModel", backref="margin_snapshot")


class MarginSnapshotDataModel(Base):
    __tablename__ = "margin_data"

    id = Column(Integer, primary_key=True)
    marginLevel = Column(Float, nullable=False)
    totalAssetOfBtc = Column(Float, nullable=False, default=0)
    totalLiabilityOfBtc = Column(Float, nullable=False, default=0)
    totalNetAssetOfBtc = Column(Float, nullable=False, default=0)

    snapshot_id = Column(Integer, ForeignKey('margin_snapshot.id'))
    userAssets = relationship("MarginAssetModel", backref="margin_data")


class MarginAssetModel(Base):
    __tablename__ = "margin_asset"

    id = Column(Integer, primary_key=True)
    asset = Column(String, nullable=False)
    borrowed = Column(Float, nullable=False, default=0)
    free = Column(Float, nullable=False, default=0)
    interest = Column(Float, nullable=False, default=0)
    locked = Column(Float, nullable=False, default=0)
    netAsset = Column(Float, nullable=False, default=0)

    data_id = Column(Integer, ForeignKey('margin_data.id'))


class SpotSnapshotModel(Base):
    __tablename__ = "spot_snapshot"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    updatetime = Column(BigInteger, unique=True)

    data = relationship("SpotSnapshotDataModel", backref="spot_snapshot")


class SpotSnapshotDataModel(Base):
    __tablename__ = "spot_data"

    id = Column(Integer, primary_key=True)
    totalAssetOfBtc = Column(Float, nullable=False)
    spot_snapshot_id = Column(Integer, ForeignKey('spot_snapshot.id'))

    balances = relationship("SpotAssetModel", backref="spot_data")


class SpotAssetModel(Base):
    __tablename__ = "spot_asset"

    id = Column(Integer, primary_key=True)
    asset = Column(String, nullable=False)
    free = Column(Float, nullable=False)
    locked = Column(Float, nullable=False)

    spot_data_id = Column(Integer, ForeignKey('spot_data.id'))

    def __repr__(self):
        return "%s free/lock: %.4f / %.4f" % (
            self.asset, self.free, self.locked
        )


engine = get_engine()
Base.metadata.create_all(engine)