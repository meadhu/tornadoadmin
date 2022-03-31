from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from common import BaseModel

# 创建中间表
user_role = Table(
    "admin_user_role",  # 中间表名称
    Column("id", Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    Column("user_id", Integer, ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
    Column("role_id", Integer, ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)
