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
    tracks = relationship("Track", back_populates="scholar", 
                          cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        r = f"Scholar(internal_id={self.internal_id!r} name={self.name!r})"
        return r


class Track(Base, SmartModelMixin):
    __tablename__ = "track"

    id = Column(Integer, primary_key=True)
    insert_date = Column(DateTime, default=datetime.now)
    mmr = Column(Integer)
    rank = Column(Integer)
    total_slp = Column(Integer)
    raw_total = Column(Integer)
    in_game_slp = Column(Integer)
    ronin_slp = Column(Integer)
    lifetime_slp = Column(Integer)
    last_claim = Column(DateTime)
    next_claim = Column(DateTime)
    player_name = Column(String) 

    # relations
    scholar_id = Column(Integer, ForeignKey('scholar.id', ondelete="CASCADE"))
    scholar = relationship("Scholar", back_populates="tracks")

    def __repr__(self):
        r = f"Track(insert_date={self.insert_date.isoformat()!r} "
        r += f"scholar={self.scholar!r})"
        return r
