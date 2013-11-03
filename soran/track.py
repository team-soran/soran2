from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relationship

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


class ListenTrack(Base):

    id = Column(Integer, primary_key=True)

    track_id = Column(Integer, ForeignKey('tracks.id'))

    track = relationship('Track')

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User')

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    __tablename__ = 'listen_tracks'
