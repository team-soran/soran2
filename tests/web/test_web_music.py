# -*- coding: utf-8 -*-
from pytest import fixture
import simplejson as json

from soran.web.music import BugsProvider, NaverMusicProvider
from soran.music import MusicService

def test_bugs_track_provider(f_bugs):
    bugs = BugsProvider()
    # 2636433 == 제이레빗 '알고있을까?' in Looking Around
    with open('./tests/web/assets/bugs_track.json', 'r') as f:
        _data = f.read()
        t = bugs.track(_data)
    track = t.track
    assert u'알고있을까?' == track.name
    assert u'2636433' == t._internal_service_id


def test_bugs_album_provider(f_bugs):
    bugs = BugsProvider()
    # 2636433 == 제이레빗 '알고있을까?' in Looking Around
    with open('./tests/web/assets/bugs_track.json', 'r') as f:
        _data = f.read()
        a = bugs.album(_data)
    album = a.album
    assert u'Looking Around' == album.name
    assert u'327530' == a._internal_service_id


def test_bugs_artist_provider(f_bugs):
    bugs = BugsProvider()
    # 2636433 == 제이레빗 '알고있을까?' in Looking Around
    with open('./tests/web/assets/bugs_track.json', 'r') as f:
        _data = f.read()
        a = bugs.artist(_data)
    artist = a.artist
    assert u'제이레빗(J Rabbit)' == artist.name
    assert u'80087093' == a._internal_service_id


def test_naver_music_track_provider(f_bugs):
    naver = NaverMusicProvider()
    # 3201927 == 제이레빗 '알고있을까?' in Looking Around
    with open('./tests/web/assets/naver_track.json', 'r') as f:
        _data = f.read()
        t = naver.track(_data)
    track = t.track
    assert u'알고있을까?' == track.name
    assert u'3201927' == t._internal_service_id


def test_naver_music_album_provider(f_bugs):
    naver = NaverMusicProvider()
    # 3201927 == 제이레빗 '알고있을까?' in Looking Around
    with open('./tests/web/assets/naver_track.json', 'r') as f:
        _data = f.read()
        a = naver.album(_data)
    album = a.album
    assert u'2집 Looking Around' == album.name
    assert u'318909' == a._internal_service_id


def test_naver_music_artist_provider(f_bugs):
    naver = NaverMusicProvider()
    # 3201927 == 제이레빗 '알고있을까?' in Looking Around
    with open('./tests/web/assets/naver_track.json', 'r') as f:
        _data = f.read()
        a = naver.artist(_data)
    artist = a.artist
    assert u'제이레빗(J Rabbit)' == artist.name
    assert u'145629' == a._internal_service_id
