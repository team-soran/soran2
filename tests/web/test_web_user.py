# -*- coding: utf-8 -*-
from pytest import fixture
from flask import url_for

from ..util import url_for
from soran.web.app import app

def test_login(f_app, f_session, f_user):
    from soran.user import User
    m = 'admire9@gmail.com'
    p = 'password'
    url = url_for('user.login', data={'username': m, 'password': p})
    with app.test_client() as c:
        r = c.post(url)
    assert 200 == r.status_code
