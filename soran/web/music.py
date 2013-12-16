# -*- coding: utf-8 -*-
from flask import Blueprint
from sqlalchemy.exc import IntegrityError

import simplejson as json

from ..db import session
from .oauth import auth_required
from .response import created, not_acceptable, internal_server_error

bp = Blueprint('music', __name__, template_folder='templates/music')

def create_music(request, provider):
    payload = request.json
    if not payload:
        return not_acceptable(message='json required.')
    music = provider.transform(payload)
    session.add(music.album)
    session.add(music.artist)
    session.add(music.track)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return internal_server_error()
    return created(track={'id': music.track.track.id},
                   album={'id': music.album.album.id},
                   artist={'id': music.artist.artist.id})
