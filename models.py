from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import registry, relationship


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
mapper_registry = registry()
Base = mapper_registry.generate_base()


class Scholar(Base):
    __tablename__ = "scholar"

    id = Column(Integer, primary_key=True)
    scholar_id = Column(Integer)
    name = Column(String)
    battle_name = Column(String(30), nullable=True)

    # ronin id without prefixes (e.g. 'ronin:' or '0x')
    ronin_id = Column(String(String(40)))  
    personal_ronin_id = Column(String(40), nullable=True)

    def __repr__(self):
        ronin_tag = f"{self.ronin_id[:4]}..{self.ronin_id[:-4]}"
        return f"Scholar(name='{self.name!r} ronin_id='{ronin_tag}"


class Track(Base):
    __tablename__ = "track"

    id = Column(Integer, primary_key=True)
    recording_date = Column(DateTime)
    slp_total = Column(Integer)
    slp_raw_total = Column(Integer)
    slp_ronin = Column(Integer)
    slp_ingame = Column(Integer)
    mmr = Column(Integer)
    rank = Column(Integer)

    # relations
    scholar = relationship("Scholar", back_populates="tracks")
