from sqlalchemy import Enum
from sqlalchemy.ext.declarative import declarative_base

__all__ = 'Base', 'services'

Base = declarative_base()

services = Enum('bugs', 'naver_music')
