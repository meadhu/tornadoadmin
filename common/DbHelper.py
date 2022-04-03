"""
# ORM  对象关系映射
# SQLAlchemy 连接数据库
"""
import datetime
import traceback

import pymysql
import sqlparse
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, class_mapper

from config import config_params

# MySql配置信息
HOST = config_params.get('MYSQL_HOST') or '127.0.0.1'
PORT = config_params.get('MYSQL_PORT') or 3306
DATABASE = config_params.get('MYSQL_DATABASE') or 'tornadoadmin'
USERNAME = config_params.get('MYSQL_USERNAME') or 'root'
PASSWORD = config_params.get('MYSQL_PASSWORD') or '123456'


class DbHelper:
    def __init__(self):
        self.db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
        self.first_install_check()

    def create_instance(self):
        engine = create_engine(self.db_url)
        # 打开2个连接池, 超时1200s自动关闭
        # engine = create_engine(self.db_url, pool_size=2, pool_recycle=1200)
        return engine

    def first_install_check(self):
        if self.is_exist_database():
            # print('数据库已经存在,为防止误初始化，请手动删除 %s 数据库' % str(DATABASE))
            return
        if self.create_database():
            print('数据库%s创建成功' % str(DATABASE))
        self.execute_fromfile('docs/install.sql')
        print('表创建成功')
        print('欢迎使用 tornadoadmin, 请使用 python run 命令启动程序')

    ##### 以下是数据库 初始化 #####
    def is_exist_database(self):
        db = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, charset='utf8mb4')
        cursor1 = db.cursor()
        sql = "select * from information_schema.SCHEMATA WHERE SCHEMA_NAME = '%s'  ; " % DATABASE
        res = cursor1.execute(sql)
        db.close()
        return res

    def create_database(self):
        db = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, charset='utf8mb4')
        cursor1 = db.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS %s CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;" % DATABASE
        res = cursor1.execute(sql)
        db.close()
        return res

    def execute_fromfile(self, filename):
        db = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, database=DATABASE,
                             charset='utf8mb4')
        fd = open(filename, 'r', encoding='utf-8')
        cursor = db.cursor()
        sqlfile = fd.read()
        sqlfile = sqlparse.format(sqlfile, strip_comments=True).strip()
        sqlcommamds = sqlfile.split(';')
        for command in sqlcommamds:
            try:
                cursor.execute(command)
                db.commit()
            except Exception as msg:
                db.rollback()
                print(traceback.format_exc())
        db.close()


def init_db():
    # SQLAlchemy 处理
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
