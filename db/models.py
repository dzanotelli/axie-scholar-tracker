from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .core import Base, SmartModelMixin


class Scholar(Base, SmartModelMixin):
    __tablename__ = "scholar"

    id = Column(Integer, primary_key=True)
    internal_id = Column(String, unique=True)
    name = Column(String, nullable=True)
    battle_name = Column(String(30), nullable=True)
    join_date = Column(DateTime) 

    # ronin id without prefixes (e.g. 'ronin:' or '0x')
    ronin_id = Column(String(40))
    
    # relashionship
    tracks = relationship("Track", back_populates="scholar")

    def save(self):
        # do this only if has not been saved yet
        if not self.id and not self.join_date:
            self.join_date = datetime.now()

        super().save()


    def __repr__(self):
        ronin_tag = f"{self.ronin_id[:4]}..{self.ronin_id[:-4]}"
        return f"Scholar(name='{self.name!r} ronin_id='{ronin_tag}"


class Track(Base, SmartModelMixin):
    __tablename__ = "track"

    id = Column(Integer, primary_key=True)
    insert_date = Column(DateTime)
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
