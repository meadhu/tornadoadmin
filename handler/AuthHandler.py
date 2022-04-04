"""
# 用户登录相关
"""
from __future__ import absolute_import

from . import BaseHandler


class AuthHandler(BaseHandler):
    def login(self):
        # self.write("login page")
        return self.render("admin/login")

    def logout(self):
        self.write("logout page")
