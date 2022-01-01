from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.expression import table
from sqlalchemy.sql.sqltypes import DateTime

from . import get_session


Base = declarative_base()


class SmartModelMixin:
    """Mixing which adds some smart feature to the base model
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__= {'always_refresh': True}

    def __init__(self, **kwargs):
        super().__init__()

        for field in self.fields:
            if field in kwargs:
                setattr(self, field, kwargs.pop(field))

    def _parse_datetime_strings(self):
        for field in self.__table__.columns.values():
            if isinstance(field.type, DateTime):
                value = getattr(self, field.name, None)
                if isinstance(value, str):
                    setattr(self, field.name, datetime.fromisoformat(value))

    def save(self):
        """Persist the current object to database
        """
        # if any Datetime field has been set to string, we translate it
        # to datetime object before saving. Only isoformat supported.
        self._parse_datetime_strings()

        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def filter_by(cls, **fields):
        return get_session().query(cls).filter_by(**fields)

    @classmethod
    @property
    def fields(cls):
        return list(cls.__table__.columns.keys())