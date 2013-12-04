# -*- coding: utf-8 -*-
from soran.oauth import Token

def test_access_token(f_app, f_user, f_session):
    t = Token(user_id=f_user.id, client_id=f_app.client_id, _scopes='user')
    f_session.add(t)
    f_session.commit()
    tf = f_session.query(Token).first()
    assert tf
    assert tf.access_token
    assert tf.refresh_token
    assert t.access_token == tf.access_token
    print tf.access_token
    print tf.refresh_token
    assert False
