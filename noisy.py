#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask.ext.script import Manager

from soran.web.app import app

@Manager
def manager(config=None):
    config = os.path.abspath(config)
    app.config.from_pyfile(config)
    return app

@manager.option('--host', dest='host', default=None)
def sound(host):
    app.run(host=host)

manager.add_option('-c', '--config', dest='config', required=True)

if __name__ == '__main__':
    manager.run()
