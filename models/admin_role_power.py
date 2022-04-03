from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Table, ForeignKey

# 创建中间表
from common import BaseModel

# role_power = Table(
#     "admin_role_power",  # 中间表名称
#     Column("id", Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
#     Column("power_id", Integer, ForeignKey("admin_power.id"), comment='用户编号'),  # 属性 外键
#     Column("role_id", Integer, ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
# )

role_power = Table(
    "admin_role_power",  # 中间表名称
    BaseModel.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    Column("power_id", Integer, ForeignKey("admin_power.id"), comment='用户编号'),  # 属性 外键
    Column("role_id", Integer, ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)