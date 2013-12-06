# -*- coding: utf-8 -*-
from flask import Blueprint

import simplejson as json

from .oauth import auth_required

bp = Blueprint('music', __name__, template_folder='templates/music')
