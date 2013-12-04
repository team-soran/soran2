# -*- coding: utf-8 -*-
from flask import url_for as flask_url_for

from soran.web.app import app

def url_for(*args, **kwards):
    with app.test_request_context() as _ctx:
        return flask_url_for(*args, **kwards)
