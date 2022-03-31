import datetime
from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.orm import relationship, backref


from common import BaseModel


class Role(BaseModel):
    __tablename__ = 'admin_role'
    id = Column(Integer, primary_key=True, comment='角色ID')
    name = Column(String(255), comment='角色名称')
    code = Column(String(255), comment='角色标识')
    enable = Column(Integer, comment='是否启用')
    remark = Column(String(255), comment='备注')
    details = Column(String(255), comment='详情')
    sort = Column(Integer, default=20, comment='排序')
    create_time = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
    # power = relationship('Power', secondary="admin_role_power", backref=backref('role'))
