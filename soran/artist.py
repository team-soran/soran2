from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relationship

from .db import Base, services

__all__ = 'Artist',

class Artist(Base):
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    services = Column(services, nullable=False)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    __tablename__ = 'artists'


class ArtistTrack(Base):

    track_id = Column(Integer, ForeignKey('tracks.id'), primary_key=True)

    track = relationship('Track', uselist=False)

    artist_id = Column(Integer, ForeignKey('artists.id'), primary_key=True)

    artist = relationship(Artist, uselist=False)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    __tablename__ = 'artist_tracks'
