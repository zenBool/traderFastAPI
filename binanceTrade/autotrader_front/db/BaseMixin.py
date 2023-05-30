from sqlalchemy import Column, Integer


class BaseMixin:
    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.lower().removesuffix('model')

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(cls):
        return "%s" % (
            cls.__name__
        )