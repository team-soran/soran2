# -*- coding: utf-8 -*-
from pytest import raises

from sqlalchemy.exc import IntegrityError

from soran.artist import Artist
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
