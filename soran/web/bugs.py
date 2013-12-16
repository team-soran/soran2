# -*- coding: utf-8 -*-
from flask import Blueprint, request

from .service_provider import BugsProvider
from .music import create_music
from .oauth import auth_required

bp = Blueprint('bugs', __name__, template_folder='templates/bugs')
bugs = BugsProvider()

@bp.route('/', methods=['POST'])
@auth_required
def create_bugs():
    return create_music(request, bugs)
