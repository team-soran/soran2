from flask import current_app, g
from alembic.config import Config
from alembic.script import ScriptDirectory
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Enum

import simplejson as json

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
        if hasattr(g, 'sess'):
            if exc:
                g.sess.rollback()
            g.sess.close()

    app.teardown_appcontext(remove_or_rollback)


def get_engine(app=None):
    app = app if app else current_app
    if app.config.get('DATABASE_URL', None) is not None:
        return create_engine(app.config.get('DATABASE_URL', None))


def get_session(engine=None):
    if engine is None:
        engine = get_engine()
    if not hasattr(g, 'sess'):
        setattr(g, 'sess', Session(bind=engine))
    return getattr(g, 'sess')


class Jsonable(object):

    def to_json(self):
        return json.dumps(self.__json__()).encode('utf-8')

    def __json__(self):
        raise NotImplemented()


Session = sessionmaker()
session = LocalProxy(get_session)
