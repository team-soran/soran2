# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_oauthlib.provider import OAuth2Provider

from ..oauth import OAuthClient
from ..db import session


__all__ = 'oauth',
bp = Blueprint('oauth', __name__, template_folder='templates/oauth')
oauth = OAuth2Provider()

@oauth.clientgetter
def find_client(client_id):
    return session.query(OAuthClient) \
               .filter(client_id == client_id) \
               .first()


@oauth.grantgetter
def find_grant(client_id, code):
    return session.query(Grant) \
               .filter(Grant.client_id == client_id) \
               .filter(Grant.code == code) \
               .first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwards):
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(client_id=client_id, code=code['code'],
                  redirect_uri=request.redirect_uri,
                  _scopes=','.join(request.scopes),
                  user=[],
                  expires=expires)
    session.add(grant)
    session.commit()


@bp.route('/auth/', methods=['GET'])
def auth():
    return 'auth'
