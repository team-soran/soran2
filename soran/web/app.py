from flask import Flask

from ..db import session, ensure_shutdown_session

__all__ = 'app'

app = Flask(__name__)

ensure_shutdown_session(app)
