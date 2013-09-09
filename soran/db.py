from flask import current_app
from alembic.config import Config
from alembic.script import ScriptDirectory
from werkzeug.local import LocalProxy
from sqlalchemy import Enum, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

__all__ = ('Base', 'services', 'ensure_shutdown_session', 
           'get_engine', 'get_session', 'get_alembic_config')

Base = declarative_base()

services = Enum('bugs', 'naver_music')

def get_alembic_config(engine):
    url = str(engine.url)
    config = Config()
    config.set_main_option('script_location', 'soran:migration')
    config.set_main_option('sqlalchemy.url', url)
    config.set_main_option('url', url)
    return config, ScriptDirectory.from_config(config)


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
