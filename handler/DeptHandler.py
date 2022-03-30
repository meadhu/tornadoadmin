"""
# 部门管理
"""

from __future__ import absolute_import

import json

from common.HttpHelper import authorize
from . import BaseHandler


class DeptHandler(BaseHandler):
    # @dept_bp.get('/')
    @authorize("admin:dept:main", log=True)
    def main(self):
        return self.render_template('admin/dept/main.html')

    # @dept_bp.post('/data')
    @authorize("admin:dept:main", log=True)
    def data(self):
        # dept = Dept.query.order_by(Dept.sort).all()
        # power_data = curd.model_to_dicts(schema=DeptOutSchema, data=dept)
        # res = {
        #     "data": power_data
        # }
        # return jsonify(res)
        path = "static/admin/admin/data/dept.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    # @dept_bp.get('/add')
    @authorize("admin:dept:add", log=True)
    def add(self):
        return self.render_template('admin/dept/add.html')

    # @dept_bp.get('/tree')
    @authorize("admin:dept:main", log=True)
    def tree(self):
        # dept = Dept.query.order_by(Dept.sort).all()
        # power_data = curd.model_to_dicts(schema=DeptOutSchema, data=dept)
        # res = {
        #     "status": {"code": 200, "message": "默认"},
        #     "data": power_data
        #
        # }
        # return jsonify(res)
        path = "static/admin/admin/data/deptTree.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            # res = {
            #     "status": {"code": 200, "message": "默认"},
            #     "data": data['data']
            # }
            return self.jsonify(data)


    # @dept_bp.post('/save')
    # @authorize("admin:dept:add", log=True)
    # @use_args(DeptInSchema(), location="json", unknown=True)
    def save(self):
        # dept = Dept(
        #     parent_id=args['parentId'],
        #     dept_name=args['deptName'],
        #     sort=args['sort'],
        #     leader=args['leader'],
        #     phone=args['phone'],
        #     email=args['email'],
        #     status=args['status'],
        #     address=args['address']
        # )
        # r = db.session.add(dept)
        # db.session.commit()
        return self.success_api(msg="成功")

    # @dept_bp.get('/edit')
    @authorize("admin:dept:edit", log=True)
    def edit(self):
        # _id = request.args.get("deptId")
        # dept = curd.get_one_by_id(model=Dept,id=_id)
        return self.render_template('admin/dept/edit.html', dept=dept)

    # 启用
    # @dept_bp.put('/enable')
    @authorize("admin:dept:edit", log=True)
    def enable(self):
        # id = request.json.get('deptId')
        # if id:
        #     enable = 1
        #     d = Dept.query.filter_by(id=id).update({"status": enable})
        #     if d:
        #         db.session.commit()
        #         return success_api(msg="启用成功")
        #     return fail_api(msg="出错啦")
        return self.fail_api(msg="数据错误")

    # 禁用
    # @dept_bp.put('/disable')
    @authorize("admin:dept:edit", log=True)
    def dis_enable(self):
        # id = request.json.get('deptId')
        # if id:
        #     enable = 0
        #     d = Dept.query.filter_by(id=id).update({"status": enable})
        #     if d:
        #         db.session.commit()
        #         return success_api(msg="禁用成功")
        #     return fail_api(msg="出错啦")
        return self.fail_api(msg="数据错误")

    # @dept_bp.put('/update')
    @authorize("admin:dept:edit", log=True)
    def update(self):
        # json = request.json
        # validate.check_data(DeptSchema(unknown=INCLUDE), json)
        # id = json.get("deptId"),
        # data = {
        #     "dept_name": validate.xss_escape(json.get("deptName")),
        #     "sort": validate.xss_escape(json.get("sort")),
        #     "leader": validate.xss_escape(json.get("leader")),
        #     "phone": validate.xss_escape(json.get("phone")),
        #     "email": validate.xss_escape(json.get("email")),
        #     "status": validate.xss_escape(json.get("status")),
        #     "address": validate.xss_escape(json.get("address"))
        # }
        # d = Dept.query.filter_by(id=id).update(data)
        # if not d:
        #     return fail_api(msg="更新失败")
        # db.session.commit()
        return self.success_api(msg="更新成功")

    # @dept_bp.delete('/remove/<int:_id>')
    @authorize("admin:dept:remove", log=True)
    def remove(self):
        # d = Dept.query.filter_by(id=_id).delete()
        # if not d:
        #     return fail_api(msg="删除失败")
        # res = User.query.filter_by(dept_id=_id).update({"dept_id": None})
        # db.session.commit()
        # if res:
        #     return success_api(msg="删除成功")
        # else:
        #     return fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")
