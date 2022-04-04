"""
# 部门管理
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
from models import Dept, User
from . import BaseHandler


class DeptHandler(BaseHandler):
    @authorize("admin:dept:main", log=False)
    def main(self):
        return self.render_template('admin/dept/main.html')

    @authorize("admin:dept:main", log=False)
    def data(self):
        # path = "static/admin/admin/data/dept.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.jsonify(data)
        # 获取请求参数
        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))
        dept_name = xss_escape(self.get_argument('deptName', ''))
        query = session.query(Dept)
        rule_list = []
        if dept_name:
            rule_list.append(Dept.dept_name.like("".join(["%", dept_name, "%"])))
        query = query.filter(and_(*rule_list))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        for item in data:
            item['deptId'] = item['id']
            item['deptName'] = item['dept_name']
        return self.table_api(data=data, count=page_result.total)

    @authorize("admin:dept:add", log=False)
    def add(self):
        return self.render_template('admin/dept/add.html')

    @authorize("admin:dept:main", log=False)
    def tree(self):
        # path = "static/admin/admin/data/deptTree.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     return self.jsonify(data)
        result = session.query(Dept).order_by(Dept.sort).all()
        data = []
        for item in result:
            data.append({
                "deptId": item.id,
                "deptName": item.dept_name,
                "parentId": item.parent_id,
                "parentName": '',
            })
        res = {
            "status": {"code": 200, "message": "默认"},
            "data": data
        }
        return self.jsonify(res)

    # 保存数据
    @authorize("admin:dept:add", log=True)
    def save(self):
        req_json = json_decode(self.request.body)
        # print(req_json)
        parent_id = xss_escape(req_json.get('parentId', ''))
        dept_name = xss_escape(req_json.get('dept_name', ''))
        sort = xss_escape(req_json.get('sort', ''))
        leader = xss_escape(req_json.get('leader', ''))
        phone = xss_escape(req_json.get('phone', ''))
        email = xss_escape(req_json.get('email', ''))
        enable = xss_escape(req_json.get('enable', ''))
        address = xss_escape(req_json.get('address', ''))
        dept = Dept(
            parent_id=parent_id,
            dept_name=dept_name,
            sort=sort,
            leader=leader,
            phone=phone,
            email=email,
            enable=enable,
            address=address
        )
        try:
            # 只添加，还没有提交，如果出错还可以撤回(rollback)
            session.add(dept)
            # 提交到数据库
            session.commit()
        except Exception as e:
            session.rollback()
            print(traceback.format_exc())
            return self.fail_api()
        return self.success_api(msg="保存成功")

    @authorize("admin:dept:edit", log=False)
    def edit(self):
        _id = self.get_argument('deptId', '')
        dept_model = session.query(Dept).filter_by(id=_id).first()
        dept = object_to_dict(dept_model)
        return self.render_template('admin/dept/edit.html', dept=dept)

    # 启用
    @authorize("admin:dept:edit", log=True)
    def enable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('deptId', '')
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(Dept).filter_by(id=_id).update({"enable": 1})
        if res:
            return self.success_api(msg="启用成功")
        return self.fail_api(msg="出错啦")

    # 禁用
    @authorize("admin:dept:edit", log=True)
    def disable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get("deptId", "")
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(Dept).filter_by(id=_id).update({"enable": 0})
        if res:
            return self.success_api(msg="禁用成功")
        return self.fail_api(msg="出错啦")

    @authorize("admin:dept:edit", log=True)
    def update(self):
        req_json = json_decode(self.request.body)
        id = req_json.get("deptId", "")
        data = {
            "dept_name": xss_escape(req_json.get("deptName", "")),
            "sort": xss_escape(req_json.get("sort", "")),
            "leader": xss_escape(req_json.get("leader", "")),
            "phone": xss_escape(req_json.get("phone", "")),
            "email": xss_escape(req_json.get("email", "")),
            "enable": xss_escape(req_json.get("enable", "")),
            "address": xss_escape(req_json.get("address", ""))
        }
        res = session.query(Dept).filter_by(id=id).update(data)
        if not res:
            return self.fail_api(msg="更新失败")
        return self.success_api(msg="更新成功")

    @authorize("admin:dept:remove", log=True)
    def remove(self):
        _id = self.get_argument("deptId", "")
        if not _id:
            return self.fail_api("数据错误!")
        res = session.query(Dept).filter_by(id=_id).delete()
        if not res:
            return self.fail_api(msg="删除失败1")
        session.query(User).filter_by(dept_id=_id).update({"dept_id": ''})
        return self.success_api(msg="删除成功")
