# -*- coding: utf-8 -*-
from flask import Blueprint, request

from .service_provider import NaverMusicProvider
from .music import create_music

bp = Blueprint('naver_music', __name__, template_folder='templates/bugs')
naver = NaverMusicProvider()

@bp.route('/', methods=['POST'])
def create_naver_music():
    return create_music(request, naver)
