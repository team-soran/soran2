from flask import Flask

from ..db import session, ensure_shutdown_session

app = Flask(__name__)

ensure_shutdown_session(app)
