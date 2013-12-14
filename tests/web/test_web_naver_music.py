# -*- coding: utf-8 -*-
import simplejson as json

from ..util import url_for

from soran.web.app import app

def test_naver_music_create_music(f_naver_data):
    url = url_for('naver_music.create_music')
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
    assert 'artist' in data
