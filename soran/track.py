from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, UnicodeText
from sqlalchemy.orm import relationship

from .db import Base, Jsonable
from .music import MusicService

__all__ = 'Track', 'ListenTrack'

class Track(Base, Jsonable):

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    genre = Column(UnicodeText)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    __tablename__ = 'tracks'

    def __json__(self):
        return {'id': self.id, 'name': self.name}


class MusicServiceTrack(Base):

    track_id = Column(Integer, ForeignKey(Track.id), primary_key=True)

    track = relationship('Track')

    music_service_name = Column(UnicodeText, ForeignKey('music_services.name'),
                                primary_key=True)

    music_service = relationship('MusicService')

    _internal_service_id = Column(UnicodeText, nullable=False)

    __tablename__ = 'music_service_tracks'
    __mapper_args__ = {'polymorphic_on': music_service_name}


class BugsTrack(MusicServiceTrack):

    __mapper_args__ = {'polymorphic_identity': MusicService.SERVICE_BUGS}


class NaverMusicTrack(MusicServiceTrack):

    __mapper_args__ = {'polymorphic_identity': MusicService.SERVICE_NAVER_MUSIC}


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
