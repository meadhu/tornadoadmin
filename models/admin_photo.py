import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, CHAR
from sqlalchemy.orm import relationship, backref

from common import BaseModel


class Photo(BaseModel):
    __tablename__ = 'admin_photo'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    href = Column(String(255))
    mime = Column(CHAR(50), nullable=False)
    size = Column(CHAR(30), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now)