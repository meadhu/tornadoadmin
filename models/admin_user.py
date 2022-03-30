import datetime
from hashlib import md5
from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.orm import relationship, backref

from common.DbHelper import BaseModel


class User(BaseModel):
    __tablename__ = 'admin_user'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = Column(String(20), comment='用户名')
    realname = Column(String(20), comment='真实名字')
    avatar = Column(String(255), comment='头像', default="/static/admin/admin/images/avatar.jpg")
    remark = Column(String(255), comment='备注')
    password_hash = Column(String(128), comment='哈希密码')
    enable = Column(Integer, default=0, comment='启用')
    dept_id = Column(Integer, comment='部门id')
    create_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='创建时间')
    role = relationship('Role', secondary="admin_user_role", backref=backref('user'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = md5(password)

    def validate_password(self, password):
        # return check_password_hash(self.password_hash, password)
        return self.password_hash == md5(password)
