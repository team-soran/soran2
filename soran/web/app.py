# -*- coding: utf-8 -*-
from flask import Flask

from . import user, oauth, music, bugs, naver_music
from ..db import session, ensure_shutdown_session

__all__ = 'app'

API_VERSION = 1

app = Flask(__name__)

app.register_blueprint(oauth.bp, url_prefix="/%d/oauth" % API_VERSION)
app.register_blueprint(user.bp, url_prefix="/%d/users" % API_VERSION)
app.register_blueprint(music.bp, url_prefix="/%d/musics" % API_VERSION)
app.register_blueprint(bugs.bp, url_prefix="/%d/bugs" % API_VERSION)
app.register_blueprint(naver_music.bp, url_prefix="/%d/naver-music" % API_VERSION)

oauth.oauth.init_app(app)

@app.route('/')
def hello():
    return 'Welcome to soran.'

ensure_shutdown_session(app)
