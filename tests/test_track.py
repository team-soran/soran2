# -*- coding: utf-8 -*-
from pytest import raises

from sqlalchemy.exc import IntegrityError

from soran.track import Track
from soran.db import SERVICE_BUGS

def test_create_track(f_session):
    track_name = u'똑같다면'
    track = Track(name=track_name, services=SERVICE_BUGS)
    f_session.add(track)
    f_session.commit()
    track = f_session.query(Track).first()
    assert track
    assert track_name == track.name
    assert SERVICE_BUGS == track.services
    assert 0 == track.length


def test_not_null_track_name(f_session):
    with raises(IntegrityError):
        track = Track(services=SERVICE_BUGS)
        f_session.add(track)
        f_session.commit()


def test_not_null_track_services(f_session):
    with raises(IntegrityError):
        track = Track(name='blah')
        f_session.add(track)
        f_session.commit()
