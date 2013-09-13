#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask.ext.script import Manager, prompt_bool
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.command import downgrade as alembic_downgrade

from soran.db import get_alembic_config, get_engine, Base
from soran.web.app import app

@Manager
def manager(config=None):
    config = os.path.abspath(config)
    app.config.from_pyfile(config)
    assert 'DATABASE_URL' in app.config, 'DATABASE_URL missing in config.'
    return app


@manager.option('--host', dest='host', default=None)
def sound(host):
    app.run(host=host)


@manager.option('--message', '-m', dest='message', default=None)
def revision(message):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    m = "--autogenerate"
    alembic_revision(config,
                     message=message,
                     autogenerate=prompt_bool(m, default=True))


@manager.option('--revision', '-r', dest='revision', default='head')
def upgrade(revision):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_upgrade(config, revision)


@manager.option('--revision', '-r', dest='revision')
def downgrade(revision):
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_downgrade(config, revision)

manager.add_option('-c', '--config', dest='config', required=True)

if __name__ == '__main__':
    manager.run()
