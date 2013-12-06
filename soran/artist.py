# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, UnicodeText
from sqlalchemy.orm import relationship

from .db import Base
from .music import MusicService

__all__ = 'Artist',

class Artist(Base):

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

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


class MusicServiceArtist(Base):

    artist_id = Column(Integer, ForeignKey(Artist.id), primary_key=True)

    artist = relationship('Artist')

    music_service_name = Column(UnicodeText, ForeignKey('music_services.name'),
                                primary_key=True)

    music_service = relationship('MusicService')

    _internal_service_id = Column(UnicodeText, nullable=False)

    __tablename__ = 'music_service_artists'
    __mapper_args__ = {'polymorphic_on': music_service_name}


class BugsArtist(MusicServiceArtist):

    __mapper_args__ = {'polymorphic_identity': MusicService.SERVICE_BUGS}


class NaverMusicArtist(MusicServiceArtist):

    __mapper_args__ = {'polymorphic_identity': MusicService.SERVICE_NAVER_MUSIC}
