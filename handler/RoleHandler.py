"""
# 角色管理
"""
from __future__ import absolute_import

import json
import traceback

import tornado
from tornado.escape import json_decode
from tornado.escape import xhtml_escape as xss_escape

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import authorize
from models.admin_role import Role
from . import BaseHandler


class RoleHandler(BaseHandler):

    # 角色管理
    # @admin_role.get('/')
    @authorize("admin:role:main", log=True)
    def main(self):
        return self.render_template('admin/role/main.html')

    # 角色表格数据
    # @admin_role.get('/data')
    @authorize("admin:role:main", log=True)
    def data(self):
        # 获取请求参数
        role_name = self.get_argument('roleName', '')
        role_code = self.get_argument('roleCode', '')
        # # 查询参数构造
        # mf = ModelFilter()
        # if role_name:
        #     mf.vague(field_name="name", value=role_name)
        # if role_code:
        #     mf.vague(field_name="code", value=role_code)
        # # orm查询
        # # 使用分页获取data需要.items
        # role = Role.query.filter(mf.get_filter(Role)).layui_paginate()
        # count = role.total
        # # 返回api
        # return table_api(data=model_to_dicts(schema=RoleOutSchema, data=role.items), count=count)

        result = session.query(Role).order_by(Role.id).all()  # 查找第一个
        data = [object_to_dict(i) for i in result]
        return self.table_api(data=data, count=len(data))

        # path = "static/admin/admin/data/role.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.jsonify(data)

    # 角色增加
    # @admin_role.get('/add')
    @authorize("admin:role:add", log=True)
    def add(self):
        return self.render_template('admin/role/add.html')

    # 角色增加
    # @admin_role.post('/save')
    @authorize("admin:role:add", log=True)
    def save(self):
        req = json_decode(self.request.body)
        details = xss_escape(req.get("details"))
        enable = xss_escape(req.get("enable"))
        roleCode = xss_escape(req.get("roleCode"))
        roleName = xss_escape(req.get("roleName"))
        sort = xss_escape(req.get("sort"))
        role = Role(
            details=details,
            enable=enable,
            code=roleCode,
            name=roleName,
            sort=sort
        )
        try:
            session.add(role)
            session.commit()
        except Exception as e:
            print(traceback.format_exc())
            return self.fail_api()
        return self.success_api(msg="成功")


    # 角色授权
    # @admin_role.get('/power/<int:_id>')
    @authorize("admin:role:power", log=True)
    def power(self):
        _id = ""
        return self.render_template('admin/role/power.html', id=_id)


    # 获取角色权限
    # @admin_role.get('/getRolePower/<int:id>')
    @authorize("admin:role:main", log=True)
    def get_role_power(self):
        # role = Role.query.filter_by(id=id).first()
        # check_powers = role.power
        # check_powers_list = []
        # for cp in check_powers:
        #     check_powers_list.append(cp.id)
        # powers = Power.query.all()
        # power_schema = PowerOutSchema2(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
        # output = power_schema.dump(powers)  # 生成可序列化对象
        # for i in output:
        #     if int(i.get("powerId")) in check_powers_list:
        #         i["checkArr"] = "1"
        #     else:
        #         i["checkArr"] = "0"
        # res = {
        #     "data": output,
        #     "status": {"code": 200, "message": "默认"}
        # }
        # return jsonify(res)
        path = "static/admin/admin/data/power.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    # 保存角色权限
    # @admin_role.put('/saveRolePower')
    @authorize("admin:role:edit", log=True)
    def save_role_power(self):
        # req_form = request.form
        # power_ids = req_form.get("powerIds")
        # power_list = power_ids.split(',')
        # role_id = req_form.get("roleId")
        # role = Role.query.filter_by(id=role_id).first()
        #
        # powers = Power.query.filter(Power.id.in_(power_list)).all()
        # role.power = powers
        #
        # db.session.commit()
        return self.success_api(msg="授权成功")

    # 角色编辑
    # @admin_role.get('/edit/<int:id>')
    @authorize("admin:role:edit", log=True)
    def edit(self):
        # r = get_one_by_id(model=Role, id=id)
        id = xss_escape(self.get_argument('id', ''))
        entity = session.query(Role).filter_by(id=id).first()
        if not entity:
            raise tornado.web.HTTPError(404)
        entity_dict = object_to_dict(entity)
        # entity_dict = {"id": 2, "name": "name", "code": "code", "enable": 1, "sort": 100, "details": "ffff"}
        return self.render_template('admin/role/edit.html', role=entity_dict)

    # 更新角色
    # @admin_role.put('/update')
    @authorize("admin:role:edit", log=True)
    def update(self):
        # req_json = request.json
        # id = req_json.get("roleId")
        # data = {
        #     "code": xss_escape(req_json.get("roleCode")),
        #     "name": xss_escape(req_json.get("roleName")),
        #     "sort": xss_escape(req_json.get("sort")),
        #     "enable": xss_escape(req_json.get("enable")),
        #     "details": xss_escape(req_json.get("details"))
        # }
        # role = Role.query.filter_by(id=id).update(data)
        # db.session.commit()
        # if not role:
        #     return fail_api(msg="更新角色失败")
        return self.success_api(msg="更新角色成功")


    # 启用用户
    # @admin_role.put('/enable')
    @authorize("admin:role:edit", log=True)
    def enable(self):
        # id = request.json.get('roleId')
        # if id:
        #     res = enable_status(Role, id)
        #     if not res:
        #         return fail_api(msg="出错啦")
        #     return success_api(msg="启动成功")
        return self.fail_api(msg="数据错误")

    # 禁用用户
    # @admin_role.put('/disable')
    # @authorize("admin:role:edit", log=True)
    def dis_enable(self):
        # _id = request.json.get('roleId')
        # if _id:
        #     res = disable_status(Role, _id)
        #     if not res:
        #         return fail_api(msg="出错啦")
        #     return success_api(msg="禁用成功")
        return self.fail_api(msg="数据错误")


    # 角色删除
    # @admin_role.delete('/remove/<int:id>')
    @authorize("admin:role:remove", log=True)
    def remove(self):
        # role = Role.query.filter_by(id=id).first()
        # # 删除该角色的权限和用户
        # role.power = []
        # role.user = []
        #
        # r = Role.query.filter_by(id=id).delete()
        # db.session.commit()
        # if not r:
        #     return fail_api(msg="角色删除失败")
        return self.success_api(msg="角色删除成功")

    # 批量删除
    # @admin_role.delete('/batchRemove')
    @authorize("admin:role:remove", log=True)
    # @login_required
    def batch_remove(self):
        # ids = request.form.getlist('ids[]')
        # for id in ids:
        #     role = Role.query.filter_by(id=id).first()
        #     # 删除该角色的权限和用户
        #     role.power = []
        #     role.user = []
        #
        #     r = Role.query.filter_by(id=id).delete()
        #     db.session.commit()
        return self.success_api(msg="批量删除成功")
