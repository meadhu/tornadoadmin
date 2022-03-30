"""
# Handler 的父类, 公共函数 可定义在这里
"""
from __future__ import absolute_import

import tornado.web
import tornado.util

from common.HttpHelper import HttpHelper, NoResultError


class BaseHandler(HttpHelper):
    def get(self, slug=None):
        """
        重写父类 get() 方法
        :param slug: action 参数
        :return:
        """
        # super().get()
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            return self.render("errors/404")
        # print("slug: %s", slug)
        eval("self." + slug + "()")

    def post(self, slug=None):
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            return self.render("errors/404")
        eval("self." + slug + "()")

    def delete(self, slug=None):
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            return self.render("errors/404")
        eval("self." + slug + "()")

    def put(self, slug=None):
        slug = slug if slug else "main"
        if not hasattr(self, slug):
            return self.render("errors/404")
        eval("self." + slug + "()")

    def main(self):
        self.write("此处访问的是BaseHandler.main()方法, 请在控制器中实现main()方法")

    def render(self, tpl, **render_data):
        if not tpl.endswith('html'):
            tpl = "{}.html".format(tpl)
        super().render(tpl, **render_data)

    def render_template(self, tpl, **render_data):
        return self.render(tpl, **render_data)

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
