from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .core import Base, SmartModelMixin


class Scholar(Base, SmartModelMixin):
    __tablename__ = "scholar"

    id = Column(Integer, primary_key=True)
    internal_id = Column(String, unique=True)
    name = Column(String, nullable=True)
    battle_name = Column(String(30), nullable=True)
    join_date = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    # ronin id without prefixes (e.g. 'ronin:' or '0x')
    ronin_id = Column(String(40))
    
    # relashionship
    tracks = relationship("Track", back_populates="scholar")

    def __repr__(self):
        s = f"Scholar(internal_id={self.internal_id!r} name={self.name!r})"
        return s


class Track(Base, SmartModelMixin):
    __tablename__ = "track"

    id = Column(Integer, primary_key=True)
    insert_date = Column(DateTime, default=datetime.now)
    slp_total = Column(Integer)
    slp_raw_total = Column(Integer)
    slp_ronin = Column(Integer)
    slp_ingame = Column(Integer)
    mmr = Column(Integer)
    rank = Column(Integer)

    # relations
    scholar_id = Column(Integer, ForeignKey('scholar.id'))
    scholar = relationship("Scholar", back_populates="tracks")

    def __repr__(self):
        return f"{self.track_id} - {self.scholar}"
