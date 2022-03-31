import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref

from common import BaseModel

class AdminLog(BaseModel):
    __tablename__ = 'admin_admin_log'
    id = Column(Integer, primary_key=True)
    method = Column(String(10))
    uid = Column(Integer)
    url = Column(String(255))
    desc = Column(Text)
    ip = Column(String(255))
    success = Column(Integer)
    user_agent = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)