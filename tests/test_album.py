# -*- coding: utf-8 -*-
from pytest import raises, fixture

from sqlalchemy.exc import IntegrityError

from soran.album import Album, MusicServiceAlbum, NaverMusicAlbum
from soran.music import MusicService

def test_create_album(f_session):
    name = u'알고있을까'
    a = Album(name=name)
    f_session.add(a)
    f_session.commit()
    artist = f_session.query(Album).first()
    assert name == a.name
    assert a.created_at


def test_create_music_service_album(f_session):
    name = u'알고있을까'
    a = Album(name=name)
    f_session.add(a)
    m = MusicService(name=MusicService.SERVICE_NAVER_MUSIC)
    f_session.add(m)
    ma = MusicServiceAlbum(album=a, music_service_name=m.name,
                           _internal_service_id=u'3201927')
    f_session.add(ma)
    f_session.commit()


def test_create_naver_music_album(f_session):
    name = u'알고있을까'
    a = Album(name=name)
    f_session.add(a)
    m = MusicService(name=MusicService.SERVICE_NAVER_MUSIC)
    f_session.add(m)
    ma = NaverMusicAlbum(album=a, _internal_service_id=u'3201927')
    f_session.add(ma)
    f_session.commit()
