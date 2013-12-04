# -*- coding: utf-8 -*-
from flask import Blueprint, abort, request, current_app, g

from ..db import session
from ..user import User
from .response import notfound, ok
from .oauth import create_or_find_token, auth_required

bp = Blueprint('user', __name__, template_folder='templates/user')

@bp.route('/me/', methods=['GET'])
@auth_required
def me():
    return ok(message='', username=g.current_user.mail)


@bp.route('/login/', methods=['POST'])
def login():
    u = session.query(User)\
            .filter(User.mail == request.form.get('username', ''))\
            .first()
    if u and u.password == request.form.get('password', ''):
        token = create_or_find_token(
            current_app.config.get('SORAN_CLIENT_KEY', None), u.id, 'user')
        return ok(username=u.mail, access_token=token.access_token,
                  refresh_token=token.refresh_token,
                  token_type=token.token_type,
                  expires=token.expires)
    return notfound(message='not found user')
