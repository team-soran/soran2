# -*- coding: utf-8 -*-
from flask import Blueprint, abort, request, current_app

from ..db import session
from ..user import User
from .response import notfound, ok
from .oauth import create_or_find_token

bp = Blueprint('user', __name__, template_folder='templates/user')

@bp.route('/me/', methods=['GET'])
def me():
    return 'me'


@bp.route('/login/', methods=['POST'])
def login():
    u = session.query(User)\
            .filter(User.mail == request.form.get('username', ''))\
            .first()
    if u and u.password == request.form.get('password', ''):
        token = create_or_find_token(
            current_app.config.get('SORAN_CLIENT_KEY', None), u.id, 'user')
        return ok(username=u.mail)
    return notfound(message='not found user')
