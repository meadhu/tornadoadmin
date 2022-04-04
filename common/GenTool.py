"""
代码生成工具
"""
import json
import os

import jinja2
import pymysql

from config import config_params

# MySql配置信息
HOST = config_params.get('MYSQL_HOST') or '127.0.0.1'
PORT = config_params.get('MYSQL_PORT') or 3306
DATABASE = config_params.get('MYSQL_DATABASE') or 'tornadoadmin'
USERNAME = config_params.get('MYSQL_USERNAME') or 'root'
PASSWORD = config_params.get('MYSQL_PASSWORD') or '123456'


class GenTool:
    def __init__(self):
        pass

    def create_database(self):
        db = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, charset='utf8mb4')
        cursor1 = db.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS %s CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;" % DATABASE
        res = cursor1.execute(sql)
        db.close()
        return res

    def gii_name(self, table_name):
        """
        示例: {"table_name": "admin_dept", "model_file_name": "admin_dept.py",
        "view_name": "dept", "class_name": "Dept"}
        :param table_name:
        :return:
        """
        result = {
            "table_name": table_name,
            "model_file_name": "%s" % table_name,
            "view_name": table_name.replace("admin_", ""),
            "class_name": "".join([name.capitalize() for name in table_name.replace("admin_", "").split("_")])
        }
        return result

    def get_table_column(self, table_name):
        # 查询表结构
        db = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, database=DATABASE,
                             charset='utf8mb4')
        cursor1 = db.cursor()
        sql = "SHOW FULL COLUMNS FROM %s" % table_name
        cursor1.execute(sql)
        column_result = cursor1.fetchall()
        db.close()
        # 拼装数据
        column_list, field_name_list = [], []
        for item in column_result:
            # _field, _type, _collation, _is_null, _key, _default, _extra, _privileges, _comment = item
            column_list.append({
                "field_name": item[0],
                "field_type": item[1],
                "field_collation": item[2],
                "field_is_null": item[3],
                "field_key": item[4],
                "field_default": item[5],
                "field_extra": item[6],
                "field_privileges": item[7],
                "field_comment": item[8],
            })
            field_name_list.append(item[0])
        return {"column_list": column_list, "field_name_list": field_name_list}

    def gen_model(self, table_name):
        """
        生成 model
        :param table_name:
        :return:
        """
        # 查询表结构
        column_result = self.get_table_column(table_name=table_name)
        column_list = column_result.get('column_list', [])
        # 生成model文件
        gii_name_dict = self.gii_name(table_name=table_name)
        body = []
        body.append("import datetime\n")
        body.append("from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text\n")
        body.append("from common import BaseModel\n\n")
        body.append("class %s(BaseModel):" % gii_name_dict['class_name'])
        body.append("%s__tablename__ = '%s'" % (" " * 4, gii_name_dict['table_name']))
        for item in column_list:
            _field, _type, _collation = item['field_name'], item['field_type'], item['field_collation']
            _is_null, _key, _default = item['field_is_null'], item['field_key'], item['field_default']
            _extra, _privileges, _comment = item['field_extra'], item['field_privileges'], item['field_comment']
            # 拼装 column 数据
            _type_name = ""
            _column_items = []
            # 类型
            if "int" in _type:
                _column_items.append("Integer")
                if _key:
                    _column_items.append("primary_key=True")
            elif "varchar" in _type:
                _column_items.append(_type.replace("varchar", "String"))
            elif "text" in _type:
                _column_items.append(_type.replace("text", "Text"))
            elif "boolean" in _type:
                _column_items.append(_type.replace("boolean", "Boolean"))
            elif "datetime" in _type:
                _column_items.append(_type.replace("datetime", "DateTime"))
                if _field in ["create_at", "update_at"]:
                    _column_items.append("default=datetime.datetime.now")
                    if _field == "update_at":
                        _column_items.append("onupdate=datetime.datetime.now")
            # 字段备注
            _column_items.append('comment="%s"' % _comment)
            body.append("%s%s = Column(%s)" % (" " * 4, _field, ", ".join(_column_items)))
        # 生成 model 文件
        with open("models/%s.py" % gii_name_dict['model_file_name'], "w+") as file:
            file.write("\n".join(body))
        print("生成文件成功: models/%s.py" % gii_name_dict['model_file_name'])
        # 写入 __init__.py 文件中
        with open("models/__init__.py", "a+") as file:
            file.write(
                "\nfrom .%s import %s  # gii_model" % (gii_name_dict['model_file_name'], gii_name_dict['class_name']))
        print("写入引用文件成功: models/__init__.py")

    def gen_crud(self, table_name):
        """
        生成 CRUD
        :param table_name:
        :return:
        """
        column_result = self.get_table_column(table_name=table_name)
        field_name_list = column_result.get('field_name_list', [])
        column_list = column_result.get('column_list', [])
        gii_name_dict = self.gii_name(table_name=table_name)
        # 给模板文件中变量赋值
        template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='common/gen_templates/'))
        template_file = "DefaultHandler"
        template = template_env.get_template(template_file)
        gii_name_dict.update({"field_name_list": field_name_list})
        output = template.render(**gii_name_dict)
        # 生成 handler 文件
        with open(f"handler/%sHandler.py" % gii_name_dict['class_name'], "w+", encoding='utf-8') as file:
            file.write(output)
        print("生成handler文件成功: hander/%sHandler.py" % gii_name_dict['class_name'])
        # 添加 handler 引用
        with open(f"handler/__init__.py", "a+", encoding='utf-8') as file:
            file.write("\nfrom .%sHandler import %sHandler  # gii_model" % (
                gii_name_dict['class_name'], gii_name_dict['class_name']))
        print("添加handler引用成功: handler/__init__.py")

        # 生成前端页面
        print("开始 生成前端页面 ")
        template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='common/gen_templates/views/'))
        for html_file_name in ["main.html", "add.html", "edit.html"]:
            # html_file_name = "main.html"
            template = template_env.get_template(html_file_name)
            gii_name_dict.update({
                "field_name_list": field_name_list,
                "column_list": column_list,
            })
            output = template.render(**gii_name_dict)
            # 生成 views 文件
            view_path = "templates/admin/%s/" % gii_name_dict['view_name']
            if not os.path.exists(view_path):
                os.mkdir(view_path)
            with open(view_path + html_file_name, "w+", encoding='utf-8') as file:
                file.write(output)
            print("生成前端页面成功: %s" % html_file_name)
