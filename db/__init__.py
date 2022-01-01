from sqlalchemy import create_engine
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
