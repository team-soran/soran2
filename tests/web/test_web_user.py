# -*- coding: utf-8 -*-
from pytest import fixture
from flask import url_for

import simplejson as json

from ..util import url_for
from soran.user import User
from soran.oauth import Token
from soran.web.app import app

def test_login(f_app, f_session, f_user):
    m = f_user.mail
    p = 'password'
    url = url_for('user.login')
    with app.test_client() as c:
        r = c.post(url, data={'username': m, 'password': p})
    assert 200 == r.status_code
    data = json.loads(r.data)
    assert data
    assert 'ok' in data
    assert data['ok']
    assert 'status_code' in data
    assert 200 == data['status_code']
    assert 'username' in data
    assert m == data['username']
    token = f_session.query(Token)\
                 .filter(Token.user_id == f_user.id)\
                 .first()
    assert token
