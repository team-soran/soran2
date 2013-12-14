# -*- coding: utf-8 -*-
from pytest import fixture

import simplejson as json

from soran.web.service_provider import BugsProvider, NaverMusicProvider
from soran.music import MusicService

def test_bugs_track_provider(f_bugs_data):
    bugs = BugsProvider()
    # 2636433 == 제이레빗 '알고있을까?' in Looking Around
    t = bugs.track(f_bugs_data)
    track = t.track
    assert u'알고있을까?' == track.name
    assert u'2636433' == t._internal_service_id


def test_bugs_album_provider(f_bugs_data):
    bugs = BugsProvider()
    # 2636433 == 제이레빗 '알고있을까?' in Looking Around
    a = bugs.album(f_bugs_data)
    album = a.album
    assert u'Looking Around' == album.name
    assert u'327530' == a._internal_service_id


def test_bugs_artist_provider(f_bugs_data):
    bugs = BugsProvider()
    # 2636433 == 제이레빗 '알고있을까?' in Looking Around
    a = bugs.artist(f_bugs_data)
    artist = a.artist
    assert u'제이레빗(J Rabbit)' == artist.name
    assert u'80087093' == a._internal_service_id


def test_naver_music_track_provider(f_naver_data):
    naver = NaverMusicProvider()
    # 3201927 == 제이레빗 '알고있을까?' in Looking Around
    t = naver.track(f_naver_data)
    track = t.track
    assert u'알고있을까?' == track.name
    assert u'3201927' == t._internal_service_id


def test_naver_music_album_provider(f_naver_data):
    naver = NaverMusicProvider()
    # 3201927 == 제이레빗 '알고있을까?' in Looking Around
    a = naver.album(f_naver_data)
    album = a.album
    assert u'2집 Looking Around' == album.name
    assert u'318909' == a._internal_service_id


def test_naver_music_artist_provider(f_naver_data):
    naver = NaverMusicProvider()
    # 3201927 == 제이레빗 '알고있을까?' in Looking Around
    a = naver.artist(f_naver_data)
    artist = a.artist
    assert u'제이레빗(J Rabbit)' == artist.name
    assert u'145629' == a._internal_service_id
