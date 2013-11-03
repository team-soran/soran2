# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint('user', __name__, template_folder='templates/user')

@bp.route('/me/', methods=['GET'])
def me():
    return 'me'
