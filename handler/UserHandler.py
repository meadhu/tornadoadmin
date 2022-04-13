"""
# 用户管理
"""
from __future__ import absolute_import

import json

import tornado
from sqlalchemy import and_, desc

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import authorize
from models import User, Role, AdminLog
from . import BaseHandler
from sqlalchemy_pagination import paginate
from tornado.escape import json_decode
from tornado.escape import xhtml_escape as xss_escape


class UserHandler(BaseHandler):
    # 用户管理
    @authorize("admin:user:main", log=False)
    def main(self):
        return self.render_template('admin/user/main.html')

    # 用户分页查询
    @authorize("admin:user:main", log=False)
    def data(self):
        # 获取请求参数
        # real_name = xss_escape(request.args.get('realName', type=str))
        # username = xss_escape(request.args.get('username', type=str))
        # dept_id = request.args.get('deptId', type=int)
        # # 查询参数构造
        # mf = ModelFilter()
        # if real_name:
        #     mf.contains(field_name="realname", value=real_name)
        # if username:
        #     mf.contains(field_name="username", value=username)
        # if dept_id:
        #     mf.exact(field_name="dept_id", value=dept_id)
        # # orm查询
        # # 使用分页获取data需要.items
        # user = User.query.filter(mf.get_filter(model=User)).layui_paginate()
        # count = user.total
        # # 返回api
        # return table_api(data=model_to_dicts(schema=UserOutSchema, data=user.items), count=count)
        # path = "static/admin/admin/data/user.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.table_api(data=data['data'], count=data['count'])

        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))
        realname = xss_escape(self.get_argument('realName', ''))
        username = xss_escape(self.get_argument('username', ''))
        dept_id = xss_escape(self.get_argument('deptId', ''))
        query = session.query(User)
        rule_list = []
        if realname:
            rule_list.append(User.realname.like("".join(["%", realname, "%"])))
        if username:
            rule_list.append(User.username.like("".join(["%", username, "%"])))
        if dept_id:
            rule_list.append(User.dept_id == dept_id)
        query = query.filter(and_(*rule_list))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        for i, item in enumerate(data):
            item['userId'] = item['id']
            item['realName'] = item['realname']
            item['dept'] = result[i].dept.dept_name if result[i].dept else ''
        return self.table_api(data=data, count=page_result.total)

    # 用户增加
    @authorize("admin:user:add", log=False)
    def add(self):
        roles = []
        # roles_model_list = session.query(Role).filter(Role.enable==1).all()
        roles_model_list = session.query(Role).filter_by(enable=1).all()
        for item in roles_model_list:
            roles.append({'id': item.id, 'name': item.name})
        return self.render_template('admin/user/add.html', roles=roles)

    @authorize("admin:user:add", log=True)
    def save(self):
        req_json = json_decode(self.request.body)
        a = req_json.get("roleIds")
        username = xss_escape(req_json.get('username'))
        real_name = xss_escape(req_json.get('realName'))
        password = xss_escape(req_json.get('password'))
        role_ids = a.split(',')

        if not username or not real_name or not password:
            return self.fail_api(msg="账号姓名密码不得为空")

        if session.query(User).filter_by(username=username).count():
            return self.fail_api(msg="用户已经存在")
        user = User(username=username, realname=real_name)
        user.set_password(password.encode("utf8"))
        session.add(user)
        roles = session.query(Role).filter(Role.id.in_(role_ids)).all()
        for r in roles:
            user.role.append(r)
        session.commit()
        return self.success_api(msg="增加成功")

    # 删除用户
    @authorize("admin:user:remove", log=True)
    def remove(self):
        id = self.get_argument('id', '')
        if not id:
            return self.fail_api("参数异常!")
        user = session.query(User).filter_by(id=id).first()
        user.role = []

        res = session.query(User).filter_by(id=id).delete()
        session.commit()

        if not res:
            return self.fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")

    # 编辑用户
    @authorize("admin:user:edit", log=False)
    def edit(self):
        id = self.get_argument('id', '')
        if not id:
            return self.fail_api("参数异常!")
        user = session.query(User).filter_by(id=id).first()
        user_dict = object_to_dict(user)
        checked_roles = [r.id for r in user.role]
        roles = session.query(Role).filter_by(enable=1).all()
        roles_list = [{"id": m.id, "name": m.name} for m in roles]
        # user_dict = {"id": 2, "username": "xxxx", "realname": "xxx", "dept_id": 2}
        # roles_list = [{"id": 20, "name": "角色1"}, {"id": 30, "name": "角色2"}, {"id": 40, "name": "角色3"}]
        # checked_roles = [20, 30]
        return self.render_template('admin/user/edit.html', user=user_dict, roles=roles_list,
                                    checked_roles=checked_roles)

    #  编辑用户
    @authorize("admin:user:edit", log=True)
    def update(self):
        req_json = json_decode(self.request.body)
        a = xss_escape(req_json.get("roleIds"))
        id = xss_escape(req_json.get("userId"))
        username = xss_escape(req_json.get('username'))
        real_name = xss_escape(req_json.get('realName'))
        dept_id = xss_escape(req_json.get('deptId'))
        role_ids = a.split(',')
        session.query(User).filter_by(id=id).update({'username': username, 'realname': real_name, 'dept_id': dept_id})
        u = session.query(User).filter_by(id=id).first()

        roles = session.query(Role).filter(Role.id.in_(role_ids)).all()
        u.role = roles

        session.commit()
        return self.success_api(msg="更新成功")

    # 个人中心
    @tornado.web.authenticated
    def center(self):
        # user_info = current_user
        # TODO: 读取当前登录用户
        uid = 1
        user_logs = session.query(AdminLog).filter_by(url='/passport/login').filter_by(uid=uid).order_by(
            desc(AdminLog.create_time)).limit(10)
        user_info = session.query(User).filter_by(id=uid).first()
        user_info = object_to_dict(user_info)
        user_logs = [object_to_dict(i) for i in user_logs]
        return self.render_template('admin/user/center.html', user_info=user_info, user_logs=user_logs)

    # 修改头像
    @tornado.web.authenticated
    def profile(self):
        return self.render_template('admin/user/profile.html')

    # 修改头像
    @tornado.web.authenticated
    def update_avatar(self):
        uid = self.get_current_user()
        req_json = json_decode(self.request.body)
        # url = request.json.get("avatar").get("src")
        url = req_json.get('url', '')
        res = session.query(User).filter_by(id=uid).update({"avatar": url})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="修改成功")

    # 修改当前用户信息
    @tornado.web.authenticated
    def update_info(self):
        uid = self.get_current_user()
        req_json = json_decode(self.request.body)
        data = {
            "realname": req_json.get("realName", ""),
            "remark": req_json.get("details", "")
        }
        res = User.query.filter_by(id=uid).update(data)
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="更新成功")

    # 修改当前用户密码
    @tornado.web.authenticated
    def edit_password(self):
        return self.render_template('admin/user/edit_password.html')

    # 修改当前用户密码
    @tornado.web.authenticated
    def edit_password_post(self):
        # TODO
        current_user = session.query(User).filter_by(id=1).first()
        res_json = json_decode(self.request.body)
        old_password = res_json.get("oldPassword", "")
        new_password = res_json.get("newPassword", "")
        confirm_password = res_json.get("confirmPassword", "")
        if not new_password:
            return self.fail_api("新密码不得为空")
        if new_password != confirm_password:
            return self.fail_api("俩次密码不一样")
        is_right = current_user.validate_password(password=old_password.encode("UTF-8"))
        if not is_right:
            return self.fail_api("旧密码错误")
        current_user.set_password(res_json.get("newPassword").encode("UTF-8"))
        session.add(current_user)
        session.commit()

        return self.success_api("更改成功")

    # 启用用户
    @authorize("admin:user:edit", log=True)
    def enable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('userId', '')
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(User).filter_by(id=_id).update({"enable": 1})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="启动成功")

    # 禁用用户
    @authorize("admin:user:edit", log=True)
    def disable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get('userId', '')
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(User).filter_by(id=_id).update({"enable": 0})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="禁用成功")

    # 批量删除
    @authorize("admin:user:remove", log=True)
    def batch_remove(self):
        ids = self.get_arguments("ids[]")
        for id in ids:
            user = session.query(User).filter_by(id=id).first()
            user.role = []
            session.query(User).filter_by(id=id).delete()
        return self.success_api(msg="批量删除成功")

    # 退出登录
    @tornado.web.authenticated
    def logout(self):
        self.set_secure_cookie("login_user_id", "")
        return self.success_api(msg="退出登录")
