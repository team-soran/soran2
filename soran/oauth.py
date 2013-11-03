# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.types import Unicode, UnicodeText, DateTime, Integer, Boolean
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from .db import Base, session

class OAuthClient(Base):

    name = Column(Unicode(50))

    description = Column(Unicode(300))

    client_id = Column(Unicode(100), primary_key=True)

    client_secret = Column(Unicode(100), unique=True, index=True,
                           nullable=False)

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

    user_id = Column(Integer, ForeignKey('users.id'), ondelete='cascade')

    user = relationship('User')

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
