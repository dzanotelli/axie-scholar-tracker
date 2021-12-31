from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
engine = create_engine("sqlite:///axieST.db", echo=True, future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

session = Session()
