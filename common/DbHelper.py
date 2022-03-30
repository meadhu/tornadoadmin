"""
# ORM  对象关系映射
# SQLAlchemy 连接数据库
"""
import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, class_mapper

from config import config_params


class DbHelper:
    def __init__(self):
        self.db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
            config_params['MYSQL_USERNAME'],
            config_params['MYSQL_PASSWORD'],
            config_params['MYSQL_HOST'],
            config_params['MYSQL_PORT'],
            config_params['MYSQL_DATABASE'])

    def create_instance(self):
        # engine = create_engine(db_url)
        # 打开2个连接池, 超时1200s自动关闭
        engine = create_engine(self.db_url, pool_size=2, pool_recycle=1200)
        return engine


def init_db():
    dbhelper = DbHelper()
    engine = dbhelper.create_instance()
    # 全局 Model
    BaseModel = declarative_base(engine)
    # 创建会话
    Session = sessionmaker(engine)
    session = Session()  # 实例
    conection = engine.connect()
    return engine, BaseModel, session, conection


def object_to_dict(obj, found=None):
    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime.datetime) else (
        c, getattr(obj, c))
    out = dict(map(get_key_value, columns))
    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    out[name] = [object_to_dict(child, found) for child in related_obj]
                else:
                    out[name] = object_to_dict(related_obj, found)
    return out

# 测试
# if __name__ == "__main__":
#     conection = engine.connect()
#     result = conection.execute('select 1')
#     print(result.fetchone())
