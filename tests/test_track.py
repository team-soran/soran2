# -*- coding: utf-8 -*-
from pytest import raises

from sqlalchemy.exc import IntegrityError

from soran.track import Track, ListenTrack
from soran.artist import Artist

def test_create_track(f_session):
    track_name = u'똑같다면'
    track = Track(name=track_name)
    f_session.add(track)
    f_session.commit()
    track = f_session.query(Track).first()
    assert track
    assert track_name == track.name


def test_not_null_track_name(f_session):
    with raises(IntegrityError):
        track = Track()
        f_session.add(track)
        f_session.commit()


def test_listen_track(f_session, f_track, f_user):
    lt = ListenTrack(track_id=f_track.id, user_id=f_user.id)
    f_session.add(lt)
    f_session.commit()
    assert lt
    assert lt.track_id
    assert lt.user_id
    assert lt.created_at
    query_lt = f_session.query(ListenTrack).first()
    assert query_lt
    assert lt.track_id == query_lt.track_id
    assert lt.user_id == query_lt.user_id
    assert lt.created_at == query_lt.created_at
    assert query_lt.track_id == f_track.id
    assert query_lt.track.id == f_track.id
    assert query_lt.track.name == f_track.name
    assert query_lt.user_id == f_user.id
    assert query_lt.user.id == f_user.id
    assert query_lt.user.name == f_user.name
