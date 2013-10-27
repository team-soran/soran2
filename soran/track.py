from datetime import datetime

from sqlalchemy import Column, Integer, Unicode, DateTime

from .db import Base, services

__all__ = 'Track',

class Track(Base):
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    length = Column(Integer, nullable=True, default=0)

    services = Column(services, nullable=False)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    __tablename__ = 'tracks'
