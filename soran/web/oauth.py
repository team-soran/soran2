# -*- coding: utf-8 -*-
from functools import wraps
from datetime import datetime, timedelta

from flask import Blueprint, request, g
from flask_oauthlib.provider import OAuth2Provider
from sqlalchemy.exc import IntegrityError

from ..oauth import OAuthClient, Token, Grant
from ..db import session
from .response import forbidden


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


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    token = create_or_find_token(request.client.client_id,
                                 request.user.id,
                                 token.get('expires_in', None))
    return token


def create_or_find_token(client_id, user_id, scopes, expires_in=3600 * 12):
    token = session.query(Token)\
                .join(OAuthClient, OAuthClient.client_id == Token.client_id)\
                .filter(Token.client_id == client_id)\
                .filter(Token.user_id == user_id)\
                .first()
    create = not token
    if token and token.is_expired:
        session.delete(token)
        create = True
    if create:
        expires = datetime.utcnow() + timedelta(seconds=expires_in)
        token = Token(user_id=user_id, client_id=client_id,
                      _scopes=scopes, expires=expires)
        session.add(token)
    try:
        session.commit()
    except IntegrityError:
        abort(500)
    return token


def auth_required(f):
    @wraps(f)
    def deco(*args, **kwards):
        access_token = request.args.get('access_token', None)
        auth_header = request.headers.get('Authorization', None)
        token = None
        if access_token is not None:
            token = access_token
        elif auth_header is not None:
            toks = auth_header.split(' ')
            if len(toks) == 2 and toks[0] == 'OAuth':
                token = toks[1]
        if token is None:
            return forbidden(message='access token not contains')
        t = session.query(Token)\
                .filter(Token.access_token == token)\
                .first()
        if not t:
            return forbidden(message='invalid access token')
        g.current_user = t.user
        return f(*args, **kwards)
    return deco


@bp.route('/auth/', methods=['GET'])
@auth_required
def auth():
    return 'auth'
