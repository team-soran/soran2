# -*- coding: utf-8 -*-
from pytest import raises, fixture

from sqlalchemy.exc import IntegrityError

from soran.album import Album

def test_create_albut(f_session):
    name = u'알고있을까'
    a = Album(name=name)
    f_session.add(a)
    f_session.commit()
    artist = f_session.query(Album).first()
    assert name == a.name
    assert a.created_at
