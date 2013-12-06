# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, UnicodeText

from .db import Base, Session

class MusicService(Base):

    SERVICE_BUGS = 'bugs'

    SERVICE_NAVER_MUSIC = 'naver-music'

    name = Column(UnicodeText,
                  primary_key=True)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    @property
    def bugs(self):
        sess = Session.object_session(MusicService)
        return sess.query(MusicService).get(SERVICE_BUGS)

    @property
    def naver_music(self):
        sess = Session.object_session(MusicService)
        return sess.query(MusicService).get(SERVICE_NAVER_MUSIC)

    __tablename__  = 'music_services'
