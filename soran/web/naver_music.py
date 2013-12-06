# -*- coding: utf-8 -*-
from flask import Blueprint

from .service_provider import NaverMusicProvider

bp = Blueprint('naver_music', __name__, template_folder='templates/bugs')
naver = NaverMusicProvider()

@bp.route('/', methods=['POST'])
def create_music():
    #naver.transform()
    pass
