# -*- coding: utf-8 -*-
from flask import Blueprint, abort, request

from .response import notfound, ok
from ..db import session
from ..user import User

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
        return ok(username=username)
    return notfound(message='not found user')
