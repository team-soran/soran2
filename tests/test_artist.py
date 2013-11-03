# -*- coding: utf-8 -*-
from pytest import raises, fixture

from sqlalchemy.exc import IntegrityError

from soran.artist import Artist, ArtistTrack
from soran.db import SERVICE_BUGS
def test_create_artist(f_session):
    artist_name = u'Brown eyed soul'
    a = Artist(name=artist_name, services=SERVICE_BUGS)
    f_session.add(a)
    f_session.commit()
    artist = f_session.query(Artist).first()
    assert artist
    assert artist_name == artist.name
    assert SERVICE_BUGS == artist.services

def test_not_null_artist_name(f_session):
    with raises(IntegrityError):
        a = Artist(services=SERVICE_BUGS)
        f_session.add(a)
        f_session.commit()

def test_not_null_artist_services(f_session):
    with raises(IntegrityError):
        a = Artist(name='blah')
        f_session.add(a)
        f_session.commit()

def test_artist_track(f_session, f_artist, f_track):
    at = ArtistTrack(track_id=f_track.id, artist_id=f_artist.id)
    f_session.add(at)
    f_session.commit()
    assert at
    assert at.track_id
    assert at.artist_id
    assert at.created_at
    query_at = f_session.query(ArtistTrack).first()
    assert query_at
    assert at.track_id == query_at.track_id
    assert at.artist_id == query_at.artist_id
    assert at.created_at == query_at.created_at
    assert query_at.track_id == f_track.id
    assert query_at.track.id == f_track.id
    assert query_at.track.name == f_track.name
    assert query_at.artist_id == f_artist.id
    assert query_at.artist.id == f_artist.id
    assert query_at.artist.name == f_artist.name
