"""
# Handler 的父类, 公共函数 可定义在这里
"""
from __future__ import absolute_import

import traceback

import tornado.web
import tornado.util
from tornado.escape import xhtml_escape as xss_escape

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import HttpHelper, NoResultError
from models import User, AdminLog


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
    def get_current_user(self):  # 重写get_current_user()方法
        return self.get_secure_cookie("login_user_id", None)

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
            self.current_user = object_to_dict(session.query(User).filter_by(id=user_id).first())

    def login_log(self, uid, is_access):
        info = {
            'method': self.request.method,
            'url': self.request.path,
            'ip': self.request.remote_ip,
            'user_agent': xss_escape(self.request.headers.get('User-Agent')),
            'desc': xss_escape(self.get_argument('username', '')),
            'uid': uid,
            'success': int(is_access)
        }
        log = AdminLog(**info)
        session.add(log)
        session.flush()
        session.commit()
        return log.id
