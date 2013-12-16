# -*- coding: utf-8 -*-
from pytest import fixture
from flask import _request_ctx_stack, g
from sqlalchemy.orm import sessionmaker, scoped_session

import simplejson as json

from .util import url_for
from soran.web.app import app
from soran.web.oauth import create_or_find_token
from soran.db import get_session, Base, get_engine
from soran.track import Track
from soran.artist import Artist
from soran.user import User
from soran.music import MusicService
from soran.oauth import OAuthClient

@fixture
def f_session(request):
    with app.test_request_context() as _ctx:
        Session = sessionmaker(autocommit=False, autoflush=False)
        app.config['DATABASE_URL'] = 'sqlite:///'
        engine = get_engine(app)
        Base.metadata.create_all(engine)
        _ctx.push()
        session = Session(bind=engine)
        setattr(g, 'sess', session)
        def finish():
            session.close()
            Base.metadata.drop_all(engine)
            engine.dispose()

        request.addfinalizer(finish)
        return session


@fixture
def f_bugs(f_session):
    service = MusicService(name=MusicService.SERVICE_BUGS)
    f_session.add(service)
    f_session.commit()
    return MusicService.bugs


@fixture
def f_app(f_session, f_user):
    app = OAuthClient(name=u'soran',
                      user_id=f_user.id,
                      client_id=u'125243794405',
                      redirect_uris=u'http://test.com',
                      is_confidential=True)
    f_session.add(app)
    f_session.commit()
    return app


@fixture
def f_artist(f_session):
    artist_name = u'Brown eyed soul'
    a = Artist(name=artist_name)
    f_session.add(a)
    f_session.commit()
    return a


@fixture
def f_track(f_session):
    track_name = u'똑같다면'
    track = Track(name=track_name)
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


@fixture
def f_login(f_user, f_app):
    m = f_user.mail
    p = 'password'
    url = url_for('user.login')
    with app.test_client() as c:
        r = c.post(url, data={'username': m, 'password': p})
    return json.loads(r.data)


@fixture
def f_bugs_data():
    with open('./tests/web/assets/bugs_track.json', 'r') as f:
        return json.loads(f.read())


@fixture
def f_naver_data():
    with open('./tests/web/assets/naver_track.json', 'r') as f:
        return json.loads(f.read())


@fixture
def f_access_token(f_user, f_app):
    return create_or_find_token(user_id=f_user.id, client_id=f_app.client_id,
                                expires_in=3600, scopes='all')
