"""
# 数据字典
"""

from __future__ import absolute_import

import json
import traceback

import tornado
from sqlalchemy import and_
from sqlalchemy_pagination import paginate
from tornado.escape import json_decode
from tornado.escape import xhtml_escape as xss_escape

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import authorize
from models import DictType, DictData
from . import BaseHandler


class DictHandler(BaseHandler):
    # 数据字典
    @authorize("admin:dict:main", log=True)
    def main(self):
        return self.render_template('admin/dict/main.html')

    # @admin_dict.get('/dictType/data')
    @authorize("admin:dict:main", log=True)
    def dict_type_data(self):
        # 获取请求参数
        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))
        type_name = xss_escape(self.get_argument('typeName', ''))
        query = session.query(DictType)
        rule_list = []
        if type_name:
            rule_list.append(DictType.type_name.like("".join(["%", type_name, "%"])))
        query = query.filter(and_(*rule_list))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        for item in data:
            item['typeName'] = item['type_name']
            item['typeCode'] = item['type_code']
        return self.table_api(data=data, count=page_result.total)

        # path = "static/admin/admin/data/dictType.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.jsonify(data)

    # @admin_dict.get('/dictType/add')
    @authorize("admin:dict:add", log=True)
    def dict_type_add(self):
        return self.render_template('admin/dict/add.html')

    # @admin_dict.post('/dictType/save')
    @authorize("admin:dict:add", log=True)
    def dict_type_save(self):
        req_json = json_decode(self.request.body)
        print(req_json)
        description = xss_escape(req_json.get("description"))
        enable = xss_escape(req_json.get("enable"))
        type_code = xss_escape(req_json.get("typeCode"))
        type_name = xss_escape(req_json.get("typeName"))
        d = DictType(type_name=type_name, type_code=type_code, enable=enable, description=description)
        session.add(d)
        session.commit()
        if d.id:
            return self.success_api(msg="增加成功")
        return self.fail_api(msg="增加失败")

    #  编辑字典类型
    # @admin_dict.get('/dictType/edit')
    @authorize("admin:dict:edit", log=True)
    def dict_type_edit(self):
        _id = self.get_argument('dictTypeId', '')
        dict_type_model = session.query(DictType).filter_by(id=_id).first()
        dict_type = object_to_dict(dict_type_model)
        return self.render_template('admin/dict/edit.html', dict_type=dict_type)

    #  编辑字典类型
    # @admin_dict.put('/dictType/update')
    @authorize("admin:dict:edit", log=True)
    def dict_type_update(self):
        req_json = json_decode(self.request.body)
        id = xss_escape(req_json.get("id"))
        description = xss_escape(req_json.get("description"))
        enable = xss_escape(req_json.get("enable"))
        type_code = xss_escape(req_json.get("typeCode"))
        type_name = xss_escape(req_json.get("typeName"))
        session.query(DictType).filter_by(id=id).update({
            "description": description,
            "enable": enable,
            "type_code": type_code,
            "type_name": type_name
        })
        session.commit()
        return self.success_api(msg="更新成功")

    # 启用字典
    # @admin_dict.put('/dictType/enable')
    @authorize("admin:dict:edit", log=True)
    def dict_type_enable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('id', '')
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(DictType).filter_by(id=_id).update({"enable": 1})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api("启动成功")

    # 禁用字典
    # @admin_dict.put('/dictType/disable')
    @authorize("admin:dict:edit", log=True)
    def dict_type_disable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('id', '')
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(DictType).filter_by(id=_id).update({"enable": 0})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api("禁用成功")

    # 删除字典类型
    # @admin_dict.delete('/dictType/remove/<int:_id>')
    @authorize("admin:dict:remove", log=True)
    def dict_type_remove(self):
        _id = self.get_argument('id', '')
        if not _id:
            return self.fail_api("数据错误!")
        res = session.query(DictType).filter_by(id=_id).delete()
        if not res:
            return self.fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")

    # @admin_dict.get('/dictData/data')
    @authorize("admin:dict:main", log=True)
    def dict_data_data(self):
        # type_code = xss_escape(request.args.get('typeCode', type=str))
        # dict_data = DictData.query.filter_by(type_code=type_code).layui_paginate()
        # count = dict_data.total
        # data = curd.model_to_dicts(schema=DictDataOutSchema, data=dict_data.items)
        # path = "static/admin/admin/data/dictData.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.table_api(data=data['data'], count=data['count'])

        # 获取请求参数
        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))
        type_code = xss_escape(self.get_argument('typeCode', ''))
        query = session.query(DictData)
        rule_list = []
        if type_code:
            rule_list.append(DictData.type_code.like("".join(["%", type_code, "%"])))
        query = query.filter(and_(*rule_list))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        for item in data:
            item['dataId'] = item['id']
            item['dataLabel'] = item['data_label']
            item['dataValue'] = item['data_value']
            item['typeCode'] = item['type_code']
        return self.table_api(data=data, count=page_result.total)

    # 增加字典数据
    # @admin_dict.get('/dictData/add')
    @authorize("admin:dict:add", log=True)
    def dict_data_add(self):
        type_code = self.get_argument('typeCode', "")
        return self.render_template('admin/dict/data/add.html', type_code=type_code)

    # 增加字典数据
    # @admin_dict.post('/dictData/save')
    @authorize("admin:dict:add", log=True)
    def dict_data_save(self):
        req_json = json_decode(self.request.body)
        data_label = xss_escape(req_json.get("dataLabel"))
        data_value = xss_escape(req_json.get("dataValue"))
        enable = xss_escape(req_json.get("enable"))
        remark = xss_escape(req_json.get("remark"))
        type_code = xss_escape(req_json.get("typeCode"))
        d = DictData(data_label=data_label, data_value=data_value, enable=enable, remark=remark, type_code=type_code)
        session.add(d)
        session.commit()
        if not d.id:
            return self.fail_api("增加失败")
        return self.success_api("增加成功")

    #  编辑字典数据
    # @admin_dict.get('/dictData/edit')
    @authorize("admin:dict:edit", log=True)
    def dict_data_edit(self):
        _id = self.get_argument("dataId", "")
        if not _id:
            return self.fail_api("数据错误!")
        dict_data_model = session.query(DictData).filter_by(id=_id).first()
        dict_data = object_to_dict(dict_data_model)
        return self.render_template('admin/dict/data/edit.html', dict_data=dict_data)

    #  编辑字典数据
    # @admin_dict.put('/dictData/update')
    @authorize("admin:dict:edit", log=True)
    def dict_data_update(self):
        req_json = json_decode(self.request.body)
        id = req_json.get("dataId")
        session.query(DictData).filter_by(id=id).update({
            "data_label": xss_escape(req_json.get("dataLabel")),
            "data_value": xss_escape(req_json.get("dataValue")),
            "enable": xss_escape(req_json.get("enable")),
            "remark": xss_escape(req_json.get("remark")),
            "type_code": xss_escape(req_json.get("typeCode"))
        })
        session.commit()
        return self.success_api(msg="更新成功")

    # 启用字典数据
    # @admin_dict.put('/dictData/enable')
    @authorize("admin:dict:edit", log=True)
    def dict_data_enable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('dataId')
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(DictData).filter_by(id=_id).update({"enable": 1})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="启动成功")

    # 禁用字典数据
    # @admin_dict.put('/dictData/disable')
    @authorize("admin:dict:edit", log=True)
    def dict_data_disable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('dataId', '')
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(DictData).filter_by(id=_id).update({"enable": 0})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="禁用成功")

    # 删除字典类型
    # @admin_dict.delete('dictData/remove/<int:id>')
    @authorize("admin:dict:remove", log=True)
    def dict_data_remove(self):
        _id = self.get_argument('dataId', '')
        if not _id:
            return self.fail_api("数据错误!")
        res = session.query(DictData).filter_by(id=_id).delete()
        if not res:
            return self.fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")
