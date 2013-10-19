from flask import current_app
from alembic.config import Config
from alembic.script import ScriptDirectory
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

__all__ = ('Base', 'ensure_shutdown_session', 'get_engine', 'get_session',
           'get_alembic_config')

Base = declarative_base()

def get_alembic_config(engine):
    if engine is not None:
        url = str(engine.url)
        config = Config()
        config.set_main_option('script_location',
                               current_app.config['ALEMBIC_SCRIPT_LOCATION'])
        config.set_main_option('sqlalchemy.url', url)
        config.set_main_option('url', url)
        return config, ScriptDirectory.from_config(config)
    else:
        raise 'no engine founded. DATABASE_URL can be misconfigured.'


def ensure_shutdown_session(app):
    def remove_or_rollback(exc=None):
        if not exc:
            session.remove()
        else:
            session.rollback()

    app.teardown_appcontext(remove_or_rollback)


def get_engine(app=None):
    app = app if app else current_app
    if app.config.get('DATABASE_URL', None) is not None:
        return create_engine(app.config.get('DATABASE_URL', None))


def get_session():
    app = current_app
    sess = scoped_session(sessionmaker(bind=get_engine(),
                                       autocommit=False,
                                       autoflush=False))
    return sess


session = LocalProxy(get_session)
