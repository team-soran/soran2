# -*- coding -*-: utf-8
import os

from flask.ext.script import Manager, prompt_bool
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.command import downgrade as alembic_downgrade
from alembic.command import history as alembic_history
from alembic.command import branches as alembic_branch
from alembic.command import current as alembic_current

from soran.db import get_alembic_config, get_engine, Base
from soran.web.app import app

__all__ = 'manager', 'run'

@Manager
def manager(config=None):
    config = os.path.abspath(config)
    app.config.from_pyfile(config)
    assert 'DATABASE_URL' in app.config, 'DATABASE_URL missing in config.'
    return app


@manager.option('--message', '-m', dest='message', default=None)
def revision(message):
    """Add a revision"""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    m = "--autogenerate"
    alembic_revision(config,
                     message=message,
                     autogenerate=prompt_bool(m, default=True))


@manager.option('--revision', '-r', dest='revision', default='head')
def upgrade(revision):
    """Upgrade a revision to --revision or newest revision"""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_upgrade(config, revision)


@manager.option('--revision', '-r', dest='revision')
def downgrade(revision):
    """Downgrade a revision to --revision"""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_downgrade(config, revision)


@manager.command
def history():
    """List of revision history."""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_history(config)


@manager.command
def branches():
    """Show current un-spliced branch point."""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_branch(config)

@manager.command
def current():
    """Current revision."""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_current(config)


@manager.command
def init_soran_app():
    from soran.db import session
    from soran.oauth import OAuthClient
    from soran.user import User
    hyojun = session.query(User)\
                 .filter(User.mail == u'hyojun@admire.kr')\
                 .first()
    if not hyojun:
        hyojun = User(name=u'kanghyojun',
                      mail=u'hyojun@admire.kr',
                      password=u'p:hyojun')
        session.add(hyojun)
    app = session.query(OAuthClient)\
              .filter(OAuthClient.user == hyojun)\
              .filter(OAuthClient.is_confidential == True)\
              .first()
    if not app:
        app = OAuthClient(name=u'soran',
                          user=hyojun,
                          redirect_uri=u'http://undefined.com',
                          is_confidential=True,
                          client_id=u'125243794405',
                          client_secret=u'$2a$12$UIJvYUYtYW0TGtnRv'
                                        u'8hnbO9WYajGzaxs6o1FCSURLRjdX9se5f7Pe')
        session.add(app)
    session.commit()

manager.add_option('-c', '--config', dest='config', required=True)

if __name__ == '__main__':
    manager.run()
