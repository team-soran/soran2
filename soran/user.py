from sqlalchemy import Column, Integer, Unicode, ForeignKey

from .db import Base, services

class User(Base):
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    url = Column(Unicode, nullable=True)

    services = Column(services, nullable=False)

    sort = Column(Unicode, nullable=False)

    __tablename__ = 'users'
    __mapper_args__ = {'polymorphic_on': sort}

class FacebookUser(User):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    
    facebook_id = Column(Unicode, nullable=True)

    __tablename__ = 'facebook_users'
    __mapper_args__ = {'polymorphic_identity': 'facebook'}
