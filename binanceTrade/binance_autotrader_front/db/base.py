import os
import typing
from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import exc

# import dotenv
# dotenv.load_dotenv('/home/jb/PyProjects/binanceTradeFAPI/binanceTrade/.env')


def get_engine(echo: bool = False):
    user = os.getenv("DBUSER")
    password = os.getenv("DBPSSW")
    host = os.getenv("DBHOST")
    port = os.getenv("DBPORT")
    database = os.getenv("DBNAME")

    from sqlalchemy.ext.asyncio import create_async_engine

    db_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    # db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    try:
        engine = create_async_engine(db_url, echo=echo, future=False)
        # engine = create_engine(db_url, echo=echo, future=False)
        # engine = create_engine(db_url, connect_args={'check_same_thread': False}, echo=echo, future=False)
        # print(engine)
    except exc.DBAPIError as e:
        print(f"SQLAlchemy {e=}, {type(e)=}")
        return None
    except ValueError as e:
        print(f'{e=}')
        print(f'{db_url=}')
        return None
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        return None

    return engine


engine = get_engine(echo=False)
metadata = MetaData(bind=engine)
# Session = sessionmaker(autoflush=True, autocommit=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
current_session = scoped_session(Session)


@as_declarative(metadata=metadata)
class Base:
    pass


@contextmanager
def session(**kwargs) -> typing.ContextManager[Session]:
    """Provide a transactional scope around a series of operations."""
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


# ========================================================================================
#
# import typing
# from contextlib import contextmanager
#
# from sqlalchemy import MetaData, create_engine
# from sqlalchemy.ext.declarative import as_declarative
# from sqlalchemy.orm import sessionmaker, scoped_session, Query, Mapper
#
# from todo import settings
#
#
# def _get_query_cls(mapper, session):
#     if mapper:
#         m = mapper
#         if isinstance(m, tuple):
#             m = mapper[0]
#         if isinstance(m, Mapper):
#             m = m.entity
#
#         try:
#             return m.__query_cls__(mapper, session)
#         except AttributeError:
#             pass
#
#     return Query(mapper, session)
#
#
# Session = sessionmaker(query_cls=_get_query_cls)
# engine = create_engine(settings.db_url, connect_args={'check_same_thread': False}, echo=True)
# metadata = MetaData(bind=engine)
# current_session = scoped_session(Session)
#
#
# @as_declarative(metadata=metadata)
# class Base:
#     pass
#
#
# @contextmanager
# def session(**kwargs) -> typing.ContextManager[Session]:
#     """Provide a transactional scope around a series of operations."""
#     new_session = Session(**kwargs)
#     try:
#         yield new_session
#         new_session.commit()
#     except Exception:
#         new_session.rollback()
#         raise
#     finally:
#         new_session.close()


if __name__ == '__main__':
    with engine.connect() as connect:
        for row in connect.execute(f'select * from public.klines_btcusdt_1h where id < %s', 100):
            print(dict(row))

    print(engine)
