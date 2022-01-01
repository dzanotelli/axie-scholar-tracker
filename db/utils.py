import logging

from . import Base, engine


logger = logging.getLogger(f"{__name__}")


def create_db():
    """Create the database
    """
    logger.info('Creating initial db ...')
    Base.metadata.create_all(engine)
