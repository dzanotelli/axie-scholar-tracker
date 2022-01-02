from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
engine = create_engine("sqlite:///axieST.db", echo=False, future=True)
Session = sessionmaker(bind=engine)

_session = None


def get_session():
    global _session

    if _session is None:
        _session = Session()
    return _session


# enable foreign keys in SQLite3 - need to be set up to each connection
# https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#foreign-key-support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
