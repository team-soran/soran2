# -*- coding: utf-8 -*-
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from ..db import session
from .service_provider import NaverMusicProvider
from .response import created, not_acceptable, internal_server_error

bp = Blueprint('naver_music', __name__, template_folder='templates/bugs')
naver = NaverMusicProvider()

@bp.route('/', methods=['POST'])
def create_music():
    payload = request.json
    if not payload:
        return not_acceptable(message='json required.')
    data = naver.transform(request.json)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return internal_server_error()
    return created(track={})
