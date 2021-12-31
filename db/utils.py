import logging

from . import Base, engine, session
from .models import *


logger = logging.getLogger(f"{__name__}")


def create_db():
    """
    Create the database
    
    """
    logger.info('Creating initial db ...')
    Base.metadata.create_all(engine)


def persist(obj):
    """
    Persist the given object to database

    """
    session.add(obj)
    session.commit()
