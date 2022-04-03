#!/usr/bin/env python3

from __future__ import absolute_import

import os
import sys

import tornado.web
import tornado.httpserver
import tornado.ioloop

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)
define("env", default='dev', type=str)
os.environ['app_env'] = options.env

# print(os.environ)

from config import *
from handler import *


class Application(tornado.web.Application):
    def __init__(self, router, NotFound=None, **settings):
        # 读取配置文件 页面上: handler.settings["site_title"] , handler中 self.settings["site_title"]
        default = dict(
            config=config_params,
            site_title="TornadoAdmin",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # ui_modules={"Entry": EntryModule},
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
            default_handler_class=NotFound
        )
        super().__init__(handlers=router, **{**default, **settings})


def main():
    router = [
        # (r'/', IndexHandler),  # 后台首页
        (r'/', HomeHandler),  # 后台首页
        (r"/admin/home/([^/]+)", HomeHandler),  #
        (r"/auth/([^/]+)", AuthHandler),  # 登录相关
        (r"/admin/dict/([^/]+)", DictHandler),  #
        (r"/admin/dept/([^/]+)", DeptHandler),  # 部门管理
        (r"/admin/file/([^/]+)", FileHandler),  # 文件管理
        (r"/admin/log/([^/]+)", LogHandler),  # 日志管理
        (r"/admin/monitor/([^/]+)", MonitorHandler),  # 监控管理
        (r"/admin/power/([^/]+)", PowerHandler),  # 权限管理
        (r"/admin/role/([^/]+)", RoleHandler),  # 角色管理
        (r"/admin/task/([^/]+)", TaskHandler),  # 任务管理
        (r"/admin/user/([^/]+)", UserHandler),  # 用户管理
    ]
    tornado.options.parse_command_line()
    # http_server = tornado.httpserver.HTTPServer(Application(router, default_handler_class=CustomExceptionHandler, debug=(options.env == 'dev')))
    http_server = tornado.httpserver.HTTPServer(Application(router, debug=(options.env == 'dev')))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    print("项目已启动, 访问地址: http://localhost:%s" % options.port)
    main()
