import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, backref

from common import BaseModel


class Power(BaseModel):
    __tablename__ = 'admin_power'
    id = Column(Integer, primary_key=True, comment='权限编号')
    name = Column(String(255), comment='权限名称')
    type = Column(String(1), comment='权限类型')
    code = Column(String(30), comment='权限标识')
    url = Column(String(255), comment='权限路径')
    open_type = Column(String(10), comment='打开方式')
    parent_id = Column(Integer, comment='父类编号')
    icon = Column(String(128), comment='图标')
    sort = Column(Integer, comment='排序')
    create_time = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    enable = Column(Integer, comment='是否开启')
