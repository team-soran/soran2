# -*- coding: utf-8 -*-
from pytest import fixture
from lxml.html import document_fromstring

import simplejson as json

from ..util import url_for
from soran.oauth import OAuthClient, Grant
from soran.web.app import app

@fixture
def f_other_app(f_session, f_user):
    app = OAuthClient(name=u'soran extensions',
                      user_id=f_user.id,
                      client_id=u'135243794406',
                      redirect_uris=u'http://test.com',
                      is_confidential=False)
    f_session.add(app)
    f_session.commit()
    return app


def test_oauth_flow(f_user, f_other_app, f_login, f_session):
    url = url_for('oauth.auth',
                  client_id=f_other_app.client_id,
                  redirect_uri=f_other_app.default_redirect_uri,
                  response_type='code', scopes='user')
    auth_header = {'Authorization': 'Auth %s' % f_login['access_token']}
    with app.test_client() as c:
        r = c.get(
            url,
            headers=auth_header)
    assert 200 == r.status_code
    assert 'text/html' == r.mimetype
    doc = document_fromstring(r.data)
    assert doc
    assert doc.forms
    with app.test_client() as c:
        r = c.post(
            url,
            headers=auth_header,
            data={'confirm': 'yes', 'scope': 'user'})
    assert 302 == r.status_code
    grant = f_session.query(Grant)\
                .first()
    assert grant
    assert grant.code

    token_url = url_for('oauth.auth',
                        client_id=f_other_app.client_id,
                        client_secret=f_other_app.client_secret,
                        redirect_uri=f_other_app.default_redirect_uri,
                        code=grant.code,
                        response_type='authorization_code',
                        scopes='user')
    with app.test_client() as c:
        r = c.get(token_url,
                  headers=auth_header)
    assert 200 == r.status_code
    assert r.data
    data = json.loads(r.data)
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'expires' in data
    assert 'token_type' in data
