from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AllPathsModel(Base):
    __tablename__ = 'all_paths'
    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True)
    isupload = Column(Boolean, default=False)

    def __repr__(self):
        return "%s have fields <id>, <path>, <isupload>" % (
            self.__class__.__name__
        )


if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    from trade.bEx.db.get_connect import get_engine

    engine = get_engine(echo=False)
    Session = sessionmaker(engine)


    paths = AllPathsModel()

    with Session() as session:
        print(paths)

        # rows = session.query(AllPathsModel).all()
        # print('*'*50)
        # print('rows',type(rows))
        # print(type(AllPathsModel))
        # print(rows[1].id)
        # print('*'*50)
        #
        # for row in range(3):
        #     print(rows[row].__dict__)