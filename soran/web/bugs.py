# -*- coding: utf-8 -*-
from flask import Blueprint

from .service_provider import BugsProvider

bp = Blueprint('bugs', __name__, template_folder='templates/bugs')
bugs = BugsProvider()

@bp.route('/', methods=['POST'])
def create_music():
    #bugs.transform()
    pass
