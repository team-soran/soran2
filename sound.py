#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask.ext.script import Manager
from alembic.command import revision as alembic_revision

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
    alembic_revision(config, message=message, autogenerate=True)

manager.add_option('-c', '--config', dest='config', required=True)

if __name__ == '__main__':
    manager.run()
