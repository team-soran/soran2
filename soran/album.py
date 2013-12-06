# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, UnicodeText
from sqlalchemy.orm import relationship

from .db import Base
from .music import MusicService

class Album(Base):

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    __tablename__ = 'albums'


class MusicServiceAlbum(Base):

    album_id = Column(Integer, ForeignKey(Album.id), primary_key=True)

    album = relationship('Album')

    music_service_name = Column(UnicodeText, ForeignKey('music_services.name'),
                                primary_key=True)

    music_service = relationship('MusicService')

    _internal_service_id = Column(UnicodeText, nullable=False)

    __tablename__ = 'music_service_albums'
    __mapper_args__ = {'polymorphic_on': music_service_name}


class BugsAlbum(MusicServiceAlbum):

    __mapper_args__ = {'polymorphic_identity': MusicService.SERVICE_BUGS}


class NaverMusicAlbum(MusicServiceAlbum):

    __mapper_args__ = {'polymorphic_identity': MusicService.SERVICE_NAVER_MUSIC}
