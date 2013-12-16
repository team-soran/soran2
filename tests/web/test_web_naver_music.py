# -*- coding: utf-8 -*-
import simplejson as json

from ..util import url_for

from soran.web.app import app
from soran.album import Album
from soran.artist import Artist
from soran.track import Track

def test_naver_music_create_music(f_session, f_naver_data, f_access_token):
    url = url_for('naver_music.create_naver_music',
                  access_token=f_access_token.access_token)
    with app.test_client() as c:
        r = c.post(url, data=json.dumps(f_naver_data),
                   content_type='application/json')
    assert 200 == r.status_code
    data = json.loads(r.data)
    assert data
    assert 'status_code' in data
    assert 201 == data['status_code']
    assert 'message' in data
    assert 'ok' in data
    assert data['ok']
    assert 'track' in data
    assert 'id' in data['track']
    assert 'album' in data
    assert 'id' in data['album']
    assert 'artist' in data
    assert 'id' in data['artist']
    album = f_session.query(Album).first()
    artist = f_session.query(Artist).first()
    track = f_session.query(Track).first()
    assert album
    assert artist
    assert track
    assert album.id == data['album']['id']
    assert artist.id == data['artist']['id']
    assert track.id == data['track']['id']
