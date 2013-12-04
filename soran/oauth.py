# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from bcrypt import gensalt, hashpw
from sqlalchemy.types import Unicode, UnicodeText, DateTime, Integer, Boolean
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship, validates

from .db import Base, session

class OAuthClient(Base):

    CLIENT_SECRET_FORM = '{0} from {1} by {2}'.format

    def generate_client_id(context):
        user_id = context.current_parameters['user_id']
        url = context.current_parameters['redirect_uri'][7:].encode('hex')[7:12]
        return (user_id + int(url, base=16)) ** 2 + user_id

    def generate_client_secret(context):
        user_id = context.current_parameters['client_id']
        client_id = context.current_parameters['client_id']
        redirect_uri = context.current_parameters['client_id']
        form_ = OAuthClient.CLIENT_SECRET_FORM(
            client_id, redirect_uri, user_id
        ) 
        return hashpw(form_, gensalt())

    name = Column(Unicode(50))

    description = Column(Unicode(300))

    client_id = Column(Unicode(100), primary_key=True,
                       default=generate_client_id)

    client_secret = Column(Unicode(100), unique=True,
                           nullable=False, index=True,
                           default=generate_client_secret)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    is_confidential = Column(Boolean, nullable=False, default=False)

    redirect_uri = Column(UnicodeText, nullable=False)

    _default_scopes = Column(UnicodeText)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def default_redirect_url(self):
        return self.redirect_uri

    @property
    def default_scopes(self):
        if self._default_scopes is None:
            return []
        return self._default_scopes.split(',')

    __tablename__ = 'oauth_clients'


class Grant(Base):

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', cascade='all, delete')

    client_id = Column(Unicode(100), ForeignKey(OAuthClient.client_id),
                       nullable=False)

    code = Column(Unicode(255), index=True, nullable=False)

    redirect_uri = Column(UnicodeText)

    _scopes = Column(UnicodeText)

    expires = Column(DateTime(timezone=True), default=datetime.utcnow,
                     nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow,
                        nullable=False)

    @property
    def scopes(self):
        if self._default_scopes is None:
            return []
        return self._default_scopes.split(',')


    def delete(self):
        session.delete(self)
        session.commit()
        return self


    __tablename__ = 'grants'


class Token(Base):

    id = Column(Integer, primary_key=True)

    client_id =  Column(Unicode(100), ForeignKey(OAuthClient.client_id))

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User')

    access_token = Column(Unicode(255), unique=True)

    refresh_token = Column(Unicode(255), unique=True)

    expires = Column(DateTime(timezone=True), default=datetime.utcnow,
                     nullable=False)

    _scopes = Column(UnicodeText)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow,
                        nullable=False)

    @property
    def scopes(self):
        if self._default_scopes is None:
            return []
        return self._default_scopes.split(',')


    __tablename__ = 'tokens'
