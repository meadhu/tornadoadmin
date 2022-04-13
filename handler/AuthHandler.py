"""
# 用户登录相关
"""
from __future__ import absolute_import

from tornado.escape import json_decode
from tornado.escape import xhtml_escape as xss_escape
from common import session
from models import User
from . import BaseHandler


class AuthHandler(BaseHandler):
    # 登录页面
    def login(self):
        return self.render("admin/login")

    # 登录检测
    def login_post(self):
        req_json = json_decode(self.request.body)
        username = req_json.get('username')
        password = req_json.get('password')
        if not username or not password:
            return self.fail_api(msg="用户名或密码没有输入")
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return self.fail_api(msg="用户不存在")
        if not user.enable:
            return self.fail_api(msg="用户被暂停使用")
        if username == user.username and user.validate_password(password.encode("utf-8")):
            # 登录
            self.set_secure_cookie("login_user_id", str(user.id))
            # 记录登录日志
            self.login_log(uid=user.id, is_access=True)
            # 存入权限
            # index_curd.add_auth_session()
            return self.success_api(msg="登录成功")
        self.login_log(uid=user.id, is_access=False)
        return self.fail_api(msg="用户名或密码错误")

    def logout(self):
        self.set_secure_cookie("login_user_id", "")
        return self.success_api(msg="退出成功")

