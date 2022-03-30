"""
# 用户管理
"""
from __future__ import absolute_import

import json

from common.HttpHelper import authorize
from . import BaseHandler


class UserHandler(BaseHandler):
    # 用户管理
    # @admin_user.get('/')
    @authorize("admin:user:main", log=True)
    def main(self):
        return self.render_template('admin/user/main.html')

    # 用户分页查询
    # @admin_user.get('/data')
    @authorize("admin:user:main", log=True)
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
        path = "static/admin/admin/data/user.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    # 用户增加
    # @admin_user.get('/add')
    @authorize("admin:user:add", log=True)
    def add(self):
        # roles = Role.query.all()
        roles = []
        return self.render_template('admin/user/add.html', roles=roles)


    # @admin_user.post('/save')
    @authorize("admin:user:add", log=True)
    def save(self):
        # req_json = request.json
        # a = req_json.get("roleIds")
        # username = xss_escape(req_json.get('username'))
        # real_name = xss_escape(req_json.get('realName'))
        # password = xss_escape(req_json.get('password'))
        # role_ids = a.split(',')
        #
        # if not username or not real_name or not password:
        #     return fail_api(msg="账号姓名密码不得为空")
        #
        # if bool(User.query.filter_by(username=username).count()):
        #     return fail_api(msg="用户已经存在")
        # user = User(username=username, realname=real_name)
        # user.set_password(password)
        # db.session.add(user)
        # roles = Role.query.filter(Role.id.in_(role_ids)).all()
        # for r in roles:
        #     user.role.append(r)
        # db.session.commit()
        return self.success_api(msg="增加成功")


    # 删除用户
    # @admin_user.delete('/remove/<int:id>')
    @authorize("admin:user:remove", log=True)
    def delete(self):
        # user = User.query.filter_by(id=id).first()
        # user.role = []
        #
        # res = User.query.filter_by(id=id).delete()
        # db.session.commit()
        # if not res:
        #     return fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")

    # 编辑用户
    # @admin_user.get('/edit/<int:id>')
    @authorize("admin:user:edit", log=True)
    def edit(self):
        # user = curd.get_one_by_id(User,id)
        # roles = Role.query.all()
        # checked_roles = []
        # for r in user.role:
        #     checked_roles.append(r.id)
        user = {"id": 2, "username": "xxxx", "realname": "xxx", "dept_id": 2}
        roles = [{"id": 20, "name": "角色1"}, {"id": 30, "name": "角色2"}, {"id": 40, "name": "角色3"}]
        checked_roles = [20, 30]
        return self.render_template('admin/user/edit.html', user=user, roles=roles, checked_roles=checked_roles)


    #  编辑用户
    # @admin_user.put('/update')
    @authorize("admin:user:edit", log=True)
    def update(self):
        # req_json = request.json
        # a = xss_escape(req_json.get("roleIds"))
        # id = xss_escape(req_json.get("userId"))
        # username = xss_escape(req_json.get('username'))
        # real_name = xss_escape(req_json.get('realName'))
        # dept_id = xss_escape(req_json.get('deptId'))
        # role_ids = a.split(',')
        # User.query.filter_by(id=id).update({'username': username, 'realname': real_name, 'dept_id': dept_id})
        # u = User.query.filter_by(id=id).first()
        #
        # roles = Role.query.filter(Role.id.in_(role_ids)).all()
        # u.role = roles
        #
        # db.session.commit()
        return self.success_api(msg="更新成功")


    # 个人中心
    # @admin_user.get('/center')
    # @login_required
    def center(self):
        # user_info = current_user
        # user_logs = AdminLog.query.filter_by(url='/passport/login').filter_by(uid=current_user.id).order_by(
        #     desc(AdminLog.create_time)).limit(10)
        user_info = {}
        user_logs = []
        return self.render_template('admin/user/center.html', user_info=user_info, user_logs=user_logs)


    # 修改头像
    # @admin_user.get('/profile')
    # @login_required
    def profile(self):
        return self.render_template('admin/user/profile.html')


    # 修改头像
    # @admin_user.put('/updateAvatar')
    # @login_required
    def update_avatar(self):
        # url = request.json.get("avatar").get("src")
        # r = User.query.filter_by(id=current_user.id).update({"avatar": url})
        # db.session.commit()
        # if not r:
        #     return fail_api(msg="出错啦")
        return self.success_api(msg="修改成功")


    # 修改当前用户信息
    # @admin_user.put('/updateInfo')
    # @login_required
    def update_info(self):
        # req_json = request.json
        # r = User.query.filter_by(id=current_user.id).update(
        #     {"realname": req_json.get("realName"), "remark": req_json.get("details")})
        # db.session.commit()
        # if not r:
        #     return fail_api(msg="出错啦")
        return self.success_api(msg="更新成功")

    # 修改当前用户密码
    # @admin_user.get('/editPassword')
    # @login_required
    def edit_password(self):
        return self.render_template('admin/user/edit_password.html')


    # 修改当前用户密码
    # @admin_user.put('/editPassword')
    # @login_required
    def edit_password_put(self):
        # res_json = request.json
        # if res_json.get("newPassword") == '':
        #     return fail_api("新密码不得为空")
        # if res_json.get("newPassword") != res_json.get("confirmPassword"):
        #     return fail_api("俩次密码不一样")
        # user = current_user
        # is_right = user.validate_password(res_json.get("oldPassword"))
        # if not is_right:
        #     return fail_api("旧密码错误")
        # user.set_password(res_json.get("newPassword"))
        # db.session.add(user)
        # db.session.commit()
        return self.success_api("更改成功")

    # 启用用户
    # @admin_user.put('/enable')
    @authorize("admin:user:edit", log=True)
    def enable(self):
        # _id = request.json.get('userId')
        # if _id:
        #     res = enable_status(model=User, id=_id)
        #     if not res:
        #         return fail_api(msg="出错啦")
        #     return success_api(msg="启动成功")
        return self.fail_api(msg="数据错误")

    # 禁用用户
    # @admin_user.put('/disable')
    @authorize("admin:user:edit", log=True)
    def dis_enable(self):
        # _id = request.json.get('userId')
        # if _id:
        #     res = disable_status(model=User,id=_id)
        #     if not res:
        #         return fail_api(msg="出错啦")
        #     return success_api(msg="禁用成功")
        return self.fail_api(msg="数据错误")


    # 批量删除
    # @admin_user.delete('/batchRemove')
    @authorize("admin:user:remove", log=True)
    def batch_remove(self):
        # ids = request.form.getlist('ids[]')
        # for id in ids:
        #     user = User.query.filter_by(id=id).first()
        #     user.role = []
        #
        #     res = User.query.filter_by(id=id).delete()
        #     db.session.commit()
        return self.success_api(msg="批量删除成功")
