import os
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db):
    global __factory

    if __factory:
        return

    if db == 'sqlite':
        conn_str = f'sqlite:///db/test.sqlite?check_same_thread=False'
    else:
        if os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")
        conn_str = os.getenv("DATABASE_URL")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
