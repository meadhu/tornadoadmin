"""
# 角色管理
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
        # path = "static/admin/admin/data/role.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     return self.jsonify(data)
        # 获取请求参数
        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))
        role_name = xss_escape(self.get_argument('roleName', ''))
        role_code = xss_escape(self.get_argument('roleCode', ''))
        query = session.query(Role)
        rule_list = []
        if role_name:
            rule_list.append(Role.name.like("".join(["%", role_name, "%"])))
        if role_code:
            rule_list.append(Role.code.like("".join(["%", role_code, "%"])))
        query = query.filter(and_(*rule_list))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        for item in data:
            item['roleName'] = item['name']
            item['roleCode'] = item['code']
        return self.table_api(data=data, count=page_result.total)

    # 角色增加
    @authorize("admin:role:add", log=True)
    def add(self):
        return self.render_template('admin/role/add.html')

    # 角色增加
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
        # _id = "2"
        _id = self.get_argument('id', '')
        return self.render_template('admin/role/power.html', id=_id)


    # 获取角色权限
    # @admin_role.get('/getRolePower/<int:id>')
    @authorize("admin:role:main", log=True)
    def get_role_power(self):
        id = self.get_argument('id', '')
        role = session.query(Role).filter_by(id=id).first()
        check_powers = role.power
        print(check_powers)
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
        req_json = json_decode(self.request.body)
        id = req_json.get("roleId")
        data = {
            "code": xss_escape(req_json.get("roleCode")),
            "name": xss_escape(req_json.get("roleName")),
            "sort": xss_escape(req_json.get("sort")),
            "enable": xss_escape(req_json.get("enable")),
            "details": xss_escape(req_json.get("details"))
        }
        role = session.query(Role).filter_by(id=id).update(data)
        session.commit()
        if not role:
            return self.fail_api(msg="更新角色失败")
        return self.success_api(msg="更新角色成功")


    # 启用用户
    # @admin_role.put('/enable')
    @authorize("admin:role:edit", log=True)
    def enable(self):
        req_json = json_decode(self.request.body)
        id = req_json.get('roleId')
        if id:
            res = session.query(Role).filter_by(id=id).update({"enable": 1})
            if not res:
                return self.fail_api(msg="出错啦")
            return self.success_api(msg="启动成功")
        return self.fail_api(msg="数据错误")

    # 禁用用户
    # @admin_role.put('/disable')
    # @authorize("admin:role:edit", log=True)
    def disable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('roleId')
        if _id:
            res = session.query(Role).filter_by(id=_id).update({"enable": 0})
            if not res:
                return self.fail_api(msg="出错啦")
            return self.success_api(msg="禁用成功")
        return self.fail_api(msg="数据错误")


    # 角色删除
    # @admin_role.delete('/remove/<int:id>')
    @authorize("admin:role:remove", log=True)
    def remove(self):
        id = self.get_argument('id', '')
        if not id:
            return self.fail_api("参数异常!")
        # TODO: 删除该角色的权限和用户
        r = session.query(Role).filter_by(id=id).delete()
        session.commit()
        if not r:
            return self.fail_api("角色删除失败")
        return self.success_api(msg="角色删除成功")

    # 批量删除
    # @admin_role.delete('/batchRemove')
    @authorize("admin:role:remove", log=True)
    # @login_required
    def batch_remove(self):
        ids = self.get_arguments('ids[]')
        # TODO: 删除该角色的权限和用户
        # 返回受影响的行数
        effect_row_num = session.query(Role).filter(Role.id.in_(ids)).delete()
        session.commit()
        return self.success_api(msg="批量删除成功")
