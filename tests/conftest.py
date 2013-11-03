# -*- coding: utf-8 -*-
from pytest import fixture

from soran.web.app import app
from soran.db import get_session, Base, SERVICE_BUGS, get_engine
from soran.track import Track
from soran.artist import Artist
from soran.user import User

@fixture
def f_session(request):
    with app.app_context():
        app.config['DATABASE_URL'] = 'sqlite:///'
        engine = get_engine(app)
        Base.metadata.create_all(engine)
        session = get_session(engine)
        def finish():
            session.remove()
            session.close()
            Base.metadata.drop_all(engine)
            engine.dispose()

        request.addfinalizer(finish)
        return session

@fixture
def f_artist(f_session):
    artist_name = u'Brown eyed soul'
    a = Artist(name=artist_name, services=SERVICE_BUGS)
    f_session.add(a)
    f_session.commit()
    return a

@fixture
def f_track(f_session):
    track_name = u'똑같다면'
    track = Track(name=track_name, services=SERVICE_BUGS)
    f_session.add(track)
    f_session.commit()
    return track

@fixture
def f_user(f_session):
    n = 'admire'
    m = 'admire9@gmail.com'
    u = User(name=n, mail=m, password='password')
    f_session.add(u)
    f_session.commit()
    return u


