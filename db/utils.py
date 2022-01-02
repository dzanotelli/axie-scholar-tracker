import logging

from datetime import date, datetime


logger = logging.getLogger(f"{__name__}")


def create_db():
    """Create the database
    """
    from . import engine
    from .core import Base
    
    logger.info('Creating initial db ...')
    Base.metadata.create_all(engine)


def json_serial(obj):
    """JSON serializer for objects not serializable 
    by default json code
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")