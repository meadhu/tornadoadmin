"""
# Handler 的父类, 公共函数 可定义在这里
"""
from __future__ import absolute_import

import traceback

import tornado.web
import tornado.util

from common.HttpHelper import HttpHelper, NoResultError


class CustomExceptionHandler(tornado.web.RequestHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    # def prepare(self):
    #     self.set_status(404)
    #     self.render("errors/404.html")

    def write_error(self, status_code, **kwargs):
        if status_code == 403:
            return self.render("errors/403.html")
        if status_code == 404:
            return self.render("errors/404.html")
        elif status_code == 500:
            excp = kwargs['exc_info'][1]
            tb = kwargs['exc_info'][2]
            stack = traceback.extract_tb(tb)
            clean_stack = [i for i in stack if i[0][-6:] != 'gen.py' and i[0][-13:] != 'concurrent.py']
            error_msg = '{}\n  Exception: {}'.format(''.join(traceback.format_list(clean_stack)), excp)
            # do something with this error now... e.g., send it to yourself
            # on slack, or log it.
            # logging.error(error_msg)  # do something with your error...
            # don't forget to show a user friendly error page!
            return self.render("errors/500.html", error_msg=error_msg)
        else:
            self.write("undefined error")
            self.finish()


class BaseHandler(HttpHelper, CustomExceptionHandler):
    def get(self, slug=None):
        """
        重写父类 get() 方法
        :param slug: action 参数
        :return:
        """
        # super().get()
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            # return self.render("errors/404")
            raise tornado.web.HTTPError(404)
        # print("slug: %s", slug)
        eval("self." + slug + "()")

    def post(self, slug=None):
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            # return self.render("errors/404")
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

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        # TODO:
        # return self.backend.get_user_by_id(user_id)

    def row_to_obj(self, row, cur):
        """Convert a SQL row to an object supporting dict and attribute access."""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc[0]] = val
        return obj

    async def execute(self, stmt, *args):
        """Execute a SQL statement.
        Must be called with ``await self.execute(...)``
        """
        with (await self.application.conn.cursor()) as cur:
            await cur.execute(stmt, args)

    async def query(self, stmt, *args):
        """Query for a list of results.
        Typical usage::
            results = await self.query(...)
        Or::
            for row in await self.query(...)
        """
        with (self.application.conn.cursor()) as cur:
            cur.execute(stmt, args)
            return [self.row_to_obj(row, cur) for row in cur.fetchall()]

    async def queryone(self, stmt, *args):
        """Query for exactly one result.
        Raises NoResultError if there are no results, or ValueError if
        there are more than one.
        """
        results = await self.query(stmt, *args)
        if len(results) == 0:
            raise NoResultError()
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]

    async def prepare(self):
        # get_current_user cannot be a coroutine, so set
        # self.current_user in prepare instead.
        user_id = self.get_secure_cookie("blogdemo_user")
        if user_id:
            self.current_user = self.queryone(
                "SELECT * FROM authors WHERE id = %s", int(user_id)
            )
        # if self.request.headers['Content-Type'] == 'application/x-json':
        #     self.args = json_decode(self.request.body)
        # Access self.args directly instead of using self.get_argument.

    async def any_author_exists(self):
        return bool(self.query("SELECT * FROM authors LIMIT 1"))
