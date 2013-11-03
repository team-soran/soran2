<<<<<<< HEAD
from sqlalchemy import Column, Integer, Unicode

from .db import Base, services

=======
from datetime import datetime

from sqlalchemy import Column, Integer, Unicode, DateTime

from .db import Base, services

__all__ = 'Track',

>>>>>>> 13ba6f7c091faee853a927b17de0c1346bd49431
class Track(Base):
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    length = Column(Integer, nullable=True, default=0)

    services = Column(services, nullable=False)

<<<<<<< HEAD
=======
    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

>>>>>>> 13ba6f7c091faee853a927b17de0c1346bd49431
    __tablename__ = 'tracks'
