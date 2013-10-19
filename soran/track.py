from sqlalchemy import Column, Integer, Unicode

from .db import Base, services

class Track(Base):
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    length = Column(Integer, nullable=True, default=0)

    services = Column(services, nullable=False)

    __tablename__ = 'tracks'
