from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
engine = create_engine("sqlite:///axieST.db", echo=True, future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

_session = None


def get_session():
    global _session

    if _session is None:
        _session = Session()
    return _session


# give to Base the ability to persist data on the db
def save(self):
    """Persist the current object to database
    
    """
    session = get_session()
    session.add(self)
    session.commit()

Base.save = save