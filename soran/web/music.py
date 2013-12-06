# -*- coding: utf-8 -*-
from collections import namedtuple

from flask import Blueprint

import simplejson as json

from ..track import Track, BugsTrack
from ..album import Album, BugsAlbum
from ..artist import Artist, BugsArtist

bp = Blueprint('music', __name__, template_folder='templates/music')

Music = namedtuple('Music', ['artist', 'track', 'album'])

class MusicServiceProvider(object):
    """소란에서 지원하는 음악 서비스 정보를 소란데이터로 바꾸는 객체 베이스"""

    def _track_transform(self, d):
        raise NotImplemented()

    def _album_transform(self, d):
        raise NotImplemented()

    def _artist_transform(self, d):
        raise NotImplemented()

    def transform(self, d):
        return Music(track=self.track(d),
                     artist=self.artist(d),
                     album=self.album(d))

    def track(self, d):
        return self._track_transform(d)

    def album(self, d):
        return self._album_transform(d)

    def artist(self, d):
        return self._artist_transform(d)


class BugsProvider(MusicServiceProvider):
    """벅스 정보 제공"""

    def _track_transform(self, d):
        _json = json.loads(d)
        t = Track(genre=_json['track']['genre_dtl'],
                  name=_json['track']['track_title'])
        bugs_t = BugsTrack(
            _internal_service_id=unicode(_json['track']['track_id']),
            track=t)
        return bugs_t

    def _artist_transform(self, d):
        _json = json.loads(d)
        a = Artist(name=_json['track']['artist_nm'])
        bugs_a = BugsArtist(
            artist=a,
            _internal_service_id=unicode(_json['track']['artist_id']))
        return bugs_a

    def _album_transform(self, d):
        _json = json.loads(d)
        a = Album(name=_json['track']['album_title'])
        bugs_a = BugsAlbum(
            _internal_service_id=unicode(_json['track']['album_id']),
            album=a)
        return bugs_a


class NaverMusicProvider(MusicServiceProvider):
    """네이버 뮤직  정보 제공"""

    def _track_transform(self, d):
        return d

    def _artist_transform(self, d):
        pass

    def _album_transform(self, d):
        pass
