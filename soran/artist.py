from sqlalchemy import Column, Integer, Unicode

from .db import Base, services

class Artist(Base):
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    services = Column(services, nullable=False)

    __tablename__ = 'artists'
