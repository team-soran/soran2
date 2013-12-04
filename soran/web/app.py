# -*- coding: utf-8 -*-
from flask import Flask

from . import user, oauth
from ..db import session, ensure_shutdown_session

__all__ = 'app'

API_VERSION = 1

app = Flask(__name__)

app.register_blueprint(oauth.bp, url_prefix="/%d/oauth" % API_VERSION)
app.register_blueprint(user.bp, url_prefix="/%d/users" % API_VERSION)
oauth.oauth.init_app(app)
@app.route('/')
def hello():
    return 'Welcome to soran.'

ensure_shutdown_session(app)
