"""
# Handler 的父类, 公共函数 可定义在这里
"""
from __future__ import absolute_import

import traceback

import tornado.web
import tornado.util
from sqlalchemy.exc import InvalidRequestError

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import HttpHelper
from models import User


class CustomExceptionHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 403:
            return self.render("errors/403.html")
        if status_code == 404:
            return self.render("errors/404.html")
        elif status_code == 500:
            return self.render("errors/500.html")
        else:
            self.write("undefined error")
            self.finish()


class BaseHandler(HttpHelper, CustomExceptionHandler):
    def user_is_logged_in(self):
        """
        检测用户是否登录
        :return:
        """
        return True if self.get_current_user() else False

    def get_current_user(self):  # 重写get_current_user()方法
        return self.get_secure_cookie("login_user_id", None)

    def get_current_user_power(self):
        """
        获取指定用户的权限
        :return: ["admin:dept:main", "admin:log:main"]
        """
        uid = self.get_current_user()
        current_user = session.query(User).filter_by(id=uid).first()
        user_roles = current_user.role
        user_power = []
        for i in user_roles:
            if i.enable == 0:
                continue
            for p in i.power:
                if p.enable == 0:
                    continue
                user_power.append(p.code)
        return user_power

    def get(self, slug=None):
        """
        重写父类 get() 方法
        :param slug: action 参数
        :return:
        """
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            raise tornado.web.HTTPError(404)
        eval("self." + slug + "()")

    def post(self, slug=None):
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            raise tornado.web.HTTPError(404)
        eval("self." + slug + "()")

    def delete(self, slug=None):
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            raise tornado.web.HTTPError(404)
        eval("self." + slug + "()")

    def put(self, slug=None):
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            raise tornado.web.HTTPError(404)
        eval("self." + slug + "()")

    def main(self):
        self.write("此处访问的是BaseHandler.main()方法, 请在控制器中实现main()方法")

    def render(self, tpl, **render_data):
        if not tpl.endswith('html'):
            tpl = "{}.html".format(tpl)
        super().render(tpl, **render_data)

    def render_template(self, tpl, **render_data):
        return self.render(tpl, **render_data)

    async def prepare(self):
        # get_current_user cannot be a coroutine, so set
        # self.current_user in prepare instead.
        user_id = self.get_secure_cookie("login_user_id")
        if user_id:
            try:
                user_model = session.query(User).filter_by(id=user_id).first()
                self.current_user = object_to_dict(user_model) if user_model else None
            except InvalidRequestError:
                session.rollback()

    async def on_finish(self):
        session.close()
        super().on_finish()