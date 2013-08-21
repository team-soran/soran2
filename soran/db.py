from flask import current_app
from werkzeug.local import LocalProxy
from sqlalchemy import Enum, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

__all__ = ('Base', 'services', 'ensure_shutdown_session', 
           'get_engine', 'get_session')

Base = declarative_base()

services = Enum('bugs', 'naver_music')


def ensure_shutdown_session(app):
    def remove_or_rollback(exc=None):
        if not exc:
            session.remove()
        else:
            session.rollback()

    app.teardown_appcontext(remove_or_rollback)


def get_engine(app=None):
    app = app if app else current_app
    return create_engine(app.config['DATABASE_URL'])


def get_session():
    app = current_app
    sess = scoped_session(sessionmaker(bind=get_engine(),
                                       autocommit=False,
                                       autoflush=False))
    return sess


session = LocalProxy(get_session)
