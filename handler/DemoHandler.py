### 以下是示例 ####

import json
from . import BaseHandler


class DemoHanlder(BaseHandler):
    # 用户管理 ###############################
    def admin_user_main(self):
        return self.render('admin/user/main.html')

    #   用户分页查询
    def admin_user_data(self):
        # 获取请求参数
        # real_name = xss_escape(request.args.get('realName', type=str))
        # username = xss_escape(request.args.get('username', type=str))
        # dept_id = request.args.get('deptId', type=int)
        # 查询参数构造
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
        # 返回api
        path = "static/admin/admin/data/user.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    # 用户增加
    def admin_user_add(self):
        # roles = Role.query.all()
        roles = []
        return self.render('admin/user/add.html', roles=roles)

    def admin_user_save(self):
        return self.success_api(msg="增加成功")

    # 删除用户
    def admin_user_remove(self):
        return self.fail_api(msg="删除失败")
        # return self.success_api(msg="删除成功")

    #  编辑用户
    def admin_user_edit(self):
        user = {"id": 2, "username": "xxxx", "realname": "xxx", "dept_id": 2}
        roles = [{"id": 20, "name": "角色1"}, {"id": 30, "name": "角色2"}, {"id": 40, "name": "角色3"}]
        checked_roles = [20, 30]
        return self.render('admin/user/edit.html', user=user, roles=roles, checked_roles=checked_roles)

    #  编辑用户
    def admin_user_update(self):
        return self.success_api(msg="更新成功")

    # 个人中心
    def admin_user_center(self):
        user_info = {}
        user_logs = []
        return self.render('admin/user/center.html', user_info=user_info, user_logs=user_logs)

    # 修改头像
    def admin_user_profile(self):
        return self.render('admin/user/profile.html')

    # 修改头像
    def admin_user_update_avatar(self):
        return self.success_api(msg="修改成功")

    # 修改当前用户信息
    def admin_user_update_info(self):
        return self.success_api(msg="更新成功")

    # 修改当前用户密码
    def admin_user_edit_password(self):
        return self.render('admin/user/edit_password.html')

    # 修改当前用户密码
    def admin_user_edit_password_put(self):
        return self.success_api("更改成功")

    # 启用用户
    def admin_user_enable(self):
        return self.fail_api(msg="数据错误")

    # 禁用用户
    def admin_user_disable(self):
        return self.fail_api(msg="数据错误")

    # 批量删除
    def admin_user_batch_remove(self):
        return self.success_api(msg="批量删除成功")

    # 部门管理 ###############################
    def admin_dept_main(self):
        return self.render('admin/dept/main.html')

    def admin_dept_data(self):
        path = "static/admin/admin/data/dept.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    def admin_dept_add(self):
        return self.render('admin/dept/add.html')

    def admin_dept_tree(self):
        path = "static/admin/admin/data/deptTree.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            # res = {
            #     "status": {"code": 200, "message": "默认"},
            #     "data": data['data']
            # }
            return self.jsonify(data)

    def admin_dept_save(self):
        return self.success_api(msg="成功")

    def admin_dept_edit(self):
        dept = {"id": "2", "dept_name": "dept_name", "leader": "leader", "email": "email", "phone": "phone",
                "status": 1, "sort": 10,
                "address": "上海XXX"}
        return self.render('admin/dept/edit.html', dept=dept)

    # 启用
    def admin_dept_enable(self):
        return self.fail_api(msg="数据错误")

    # 禁用
    def admin_dept_disable(self):
        return self.fail_api(msg="数据错误")

    def admin_dept_update(self):
        return self.success_api(msg="更新成功")

    def admin_dept_remove(self):
        return self.success_api(msg="删除成功")

    # 角色管理 ###############################
    def admin_role_main(self):
        return self.render('admin/role/main.html')

    # 角色表格数据
    def admin_role_data(self):
        path = "static/admin/admin/data/role.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    # 角色增加
    def admin_role_add(self):
        return self.render('admin/role/add.html')

    # 角色增加
    def admin_role_save(self):
        return self.success_api(msg="成功")

    # 角色授权
    def admin_role_power(self):
        return self.render('admin/role/power.html', id=2)

    # 获取角色权限
    def admin_role_get_role_power(self):
        path = "static/admin/admin/data/power.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    # 保存角色权限
    def admin_role_save_role_power(self):
        return self.success_api(msg="授权成功")

    # 角色编辑
    def admin_role_edit(self):
        role = {"id": 2, "name": "name", "code": "code", "enable": 1, "sort": 100, "details": "ffff"}
        return self.render('admin/role/edit.html', role=role)

    # 更新角色
    def admin_role_update(self):
        return self.success_api(msg="更新角色成功")

    # 启用用户
    def admin_role_enable(self):
        return self.fail_api(msg="数据错误")

    # 禁用用户
    def admin_role_disable(self):
        return self.fail_api(msg="数据错误")

    # 角色删除
    def admin_role_remove(self):
        return self.success_api(msg="角色删除成功")

    # 批量删除
    def admin_role_batch_remove(self):
        return self.success_api(msg="批量删除成功")

    # 权限管理 ###############################
    def admin_power_main(self):
        return self.render('admin/power/main.html')

    def admin_power_data(self):
        path = "static/admin/admin/data/power.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    def admin_power_add(self):
        return self.render('admin/power/add.html')

    def admin_power_select_parent(self):
        # res = []
        # res.append({"powerId": 0, "powerName": "顶级权限", "parentId": -1})
        # res = {
        #     "status": {"code": 200, "message": "默认"},
        #     "data": {}
        # }
        # return self.jsonify(res)
        path = "static/admin/admin/data/powerSelectParent.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    # 增加
    def admin_power_save(self):
        return self.success_api(msg="成功")

    # 权限编辑
    def admin_power_edit(self):
        power = {"id": 2, "name": "name", "code": "", "type": 1, "url": "", "open_type": "_frame",
                 "icon": "", "sort": 200, "parent_id": 20, }
        icon = {}
        return self.render('admin/power/edit.html', power=power, icon=icon)

    # 权限更新
    def admin_power_update(self):
        return self.success_api(msg="更新权限成功")

    # 启用权限
    def admin_power_enable(self):
        return self.fail_api(msg="数据错误")

    # 禁用权限
    def admin_power_disable(self):
        return self.fail_api(msg="数据错误")

    # 权限删除
    def admin_power_remove(self):
        return self.success_api(msg="删除成功")

    # 批量删除
    def admin_power_batch_remove(self):
        return self.success_api(msg="批量删除成功")

    # 数据字典 ###############################
    def admin_dict_main(self):
        return self.render('admin/dict/main.html')

    # 获取请求参数
    def admin_dict_type_data(self):
        path = "static/admin/admin/data/dictType.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.jsonify(data)

    def admin_dict_type_add(self):
        return self.render('admin/dict/add.html')

    def admin_dict_type_save(self):
        return self.success_api(msg="增加成功")

    #  编辑字典类型
    def admin_dict_type_edit(self):
        dict_type = {"id": 2, "type_name": "name", "type_code": "ff", "enable": 1, "description": "dddd"}
        return self.render('admin/dict/edit.html', dict_type=dict_type)

    #  编辑字典类型
    def admin_dict_type_update(self):
        return self.success_api(msg="更新成功")

    # 启用字典
    def admin_dict_type_enable(self):
        return self.success_api("启动成功")

    # 禁用字典
    def admin_dict_type_disable(self):
       return self.success_api("禁用成功")

    # 删除字典类型
    def admin_dict_type_remove(self):
        return self.success_api(msg="删除成功")

    # @admin_dict.get('/dictData/data')
    # @authorize("admin:dict:main", log=True)
    def admin_dict_data_data(self):
        path = "static/admin/admin/data/dictData.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    # 增加字典数据
    def admin_dict_data_add(self):
        type_code = "fff"
        return self.render('admin/dict/data/add.html', type_code=type_code)

    # 增加字典数据
    def admin_dict_data_save(self):
        return self.jsonify(success=True, msg="增加成功")

    #  编辑字典数据
    def admin_dict_data_edit(self):
        dict_data = {"id": 1, "data_label": 'data_label', "data_value": "data_value", "type_code": '',
                     'enable': 1, 'remark': 'remarkremarkremark'}
        return self.render('admin/dict/data/edit.html', dict_data=dict_data)

    #  编辑字典数据
    def admin_dict_data_update(self):
        return self.success_api(msg="更新成功")

    # 启用字典数据
    def admin_dict_data_enable(self):
        return self.success_api(msg="启动成功")

    # 禁用字典数据
    def admin_dict_data_disable(self):
        return self.success_api(msg="禁用成功")

    # 删除字典类型
    def admin_dict_data_remove(self):
        return self.success_api(msg="删除成功")

    # ???? ###############################

    # 日志管理 ###############################
    def admin_log_main(self):
        self.render('admin/admin_log/main.html')

    def admin_log_login_log(self):
        path = "static/admin/admin/data/loginLog.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    def admin_log_operate_log(self):
        path = "static/admin/admin/data/operateLog.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    # 图片管理 ###############################
    def admin_file_main(self):
        self.render('admin/photo/photo.html')

    # 图片数据
    def admin_file_table(self):
        path = "static/admin/admin/data/fileTable.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    # 图片上传
    def admin_file_upload(self):
        self.render('admin/photo/photo_add.html')

    # 上传接口
    def admin_file_upload_api(self):
        res = {
            "msg": "上传成功",
            "code": 0,
            "success": True,
            "data":
                {"src": ''}
        }
        return self.jsonify(res)
        # return self.fail_api()

    # 图片删除
    def admin_file_delete(self):
        # print(self.get_argument("id"))
        # _id = request.form.get('id')
        # res = upload_curd.delete_photo_by_id(_id)
        # if res:
        #     return success_api(msg="删除成功")
        # else:
        #     return fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")
        # return self.fail_api(msg="删除失败")

    # 图片批量删除
    def admin_file_batch_remove(self):
        # ids = request.form.getlist('ids[]')
        # photo_name = Photo.query.filter(Photo.id.in_(ids)).all()
        # upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
        # for p in photo_name:
        #     os.remove(upload_url + '/' + p.name)
        # photo = Photo.query.filter(Photo.id.in_(ids)).delete(synchronize_session=False)
        # db.session.commit()
        # if photo:
        #     return success_api(msg="删除成功")
        # else:
        #     return fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")

    # 定时任务 ###############################
    def admin_task_main(self):
        self.render('admin/task/main.html')

    # 获取
    def admin_task_data(self):
        path = "static/admin/admin/data/taskList.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    # 增加
    def admin_task_add(self):
        task_list = []
        return self.render('admin/task/add.html', task_list=task_list)

    # 修改
    def admin_task_edit(self):
        task_list = []
        return self.render('admin/task/add.html', task_list=task_list)

    def admin_task_save(self):
        # _id = request.json.get("id")
        # name = request.json.get("id")
        # type = request.json.get("type")
        # functions = request.json.get("functions")
        # datetime = request.json.get("datetime")
        # time = request.json.get("time")
        # if not hasattr(tasks, functions):
        #     return fail_api()
        return self.success_api()

    # 恢复
    def admin_task_enable(self):
        # _id = request.json.get('id')
        # print(id)
        # if _id:
        #     scheduler.resume_job(str(_id))
        #     return success_api(msg="启动成功")
        return self.fail_api(msg="数据错误")

    # 暂停
    def admin_task_disable(self):
        # _id = request.json.get('id')
        # if _id:
        #     scheduler.pause_job(str(_id))
        #     return success_api(msg="暂停成功")
        return self.fail_api(msg="数据错误")

    # 移除
    def admin_task_remove(self):
        return self.success_api(msg="删除成功")

    # 登录相关 ###############################
    # @passport_bp.get('/login')
    def login(self):
        # if current_user.is_authenticated:
        #     return redirect(url_for('admin.index'))
        return self.render('admin/login.html')

    # 登录
    def login_post(self):
        return self.success_api(msg="登录成功")

    # 退出登录
    def logout(self):
        return self.success_api(msg="注销成功")

    # ??? ###############################
    # ??? ###############################
