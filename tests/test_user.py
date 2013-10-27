# -*- coding: utf-8 -*-
from pytest import fixture

from soran.user import User, Credential

@fixture
def f_user(f_session):
    n = 'admire'
    m = 'admire9@gmail.com'
    u = User(name=n, mail=m, password='password')
    f_session.add(u)
    f_session.commit()
    return u


def test_create_user(f_session):
    n = 'admire'
    m = 'admire9@gmail.com'
    u = User(name=n, mail=m)
    f_session.add(u)
    f_session.commit()
    user = f_session.query(User).first()
    assert user
    assert n == user.name
    assert m == user.mail


def test_create_user_with_password(f_session):
    n = 'admire'
    m = 'admire9@gmail.com'
    u = User(name=n, mail=m)
    u.password = 'pwd'
    print u
    f_session.add(u)
    f_session.commit()
    user = f_session.query(User).first()
    cred = f_session.query(Credential).first()
    assert user
    assert cred


def test_user_password_crypted(f_user):
    assert f_user.password == 'password'
    assert f_user.password.crypted_password != 'password'
