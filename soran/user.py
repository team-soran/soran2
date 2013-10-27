# -*- coding: utf-8 -*-
from bcrypt import gensalt, hashpw

from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from .db import Base, services

__all__ = 'User', 'MusicServiceUser', 'Credential', 'PasswordCredential',

class User(Base):

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False, unique=True)

    mail = Column(Unicode, nullable=False, unique=True)

    music_services = relationship('MusicServiceUser')

    credentials = relationship(
                      'Credential', cascade='all, delete-orphan',
                      collection_class=attribute_mapped_collection('sort'))

    @property
    def password(self):
        return self.credentials[PasswordCredential.sort_]


    @password.setter
    def password(self, pw):
        cred = PasswordCredential(password=pw)
        self.credentials[PasswordCredential.sort_] = cred

    __tablename__ = 'users'


class MusicServiceUser(Base):

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)

    service_id = Column(Unicode(255), primary_key=True)

    services = Column(services, primary_key=True)

    __tablename__ = 'music_service_users'


class Credential(Base):

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship('User')

    sort = Column(Unicode, nullable=False)

    __mapper_args__ = {'polymorphic_on': sort}
    __tablename__ = 'credentials'


class PasswordCredential(Credential):
    
    sort_ = 'password'

    id = Column(Integer, ForeignKey(Credential.id), primary_key=True)

    crypted_password = Column(Unicode, nullable=False)

    def __eq__(self, pw):
        return hashpw(pw, self.crypted_password) == self.crypted_password


    def __ne__(self, pw):
        return not hashpw(pw, self.crypted_password) == self.crypted_password


    @property
    def password(self):
        return self


    @password.setter
    def password(self, pw):
        self.crypted_password = hashpw(pw, gensalt())


    __mapper_args__ = {'polymorphic_identity': sort_}
    __tablename__ = 'password_credentials'
