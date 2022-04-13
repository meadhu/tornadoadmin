#!/usr/bin/env python3

from __future__ import absolute_import

import logging
import os
import sys

import tornado.web
import tornado.httpserver
import tornado.ioloop

from tornado.options import define, options

from tornado.log import enable_pretty_logging
enable_pretty_logging()

define("port", default=3001, help="run on the given port", type=int)
define("env", default='dev', type=str)
os.environ['app_env'] = options.env

# 这里配置的是日志的路径，配置好后控制台的相应信息就会保存到目标路径中。
if not os.path.exists("logs"):
    os.mkdir("logs")
options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'logs/tornado_main.log')

# print(os.environ)

from config import *
from handler import *

# 格式化日志输出格式
# 默认是这种的：[I 160807 09:27:17 web:1971] 200 GET / (::1) 7.00ms
# 格式化成这种的：[2016-08-07 09:38:01 执行文件名:执行函数名:执行行数 日志等级] 内容消息
class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super().__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


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
        (r'/', IndexHandler),  # 项目主入口 - 前台页面
        # (r'/', HomeHandler),  # 项目主入口 - 后台页面
        (r"/auth/([^/]+)", AuthHandler),  # 登录相关
        (r"/admin/home/([^/]+)", HomeHandler),  #
        (r"/admin/dict/([^/]+)", DictHandler),  # 字典管理
        (r"/admin/dept/([^/]+)", DeptHandler),  # 部门管理
        (r"/admin/file/([^/]+)", FileHandler),  # 文件管理
        (r"/admin/log/([^/]+)", LogHandler),  # 日志管理
        (r"/admin/monitor/([^/]+)", MonitorHandler),  # 监控管理
        (r"/admin/power/([^/]+)", PowerHandler),  # 权限管理
        (r"/admin/role/([^/]+)", RoleHandler),  # 角色管理
        (r"/admin/task/([^/]+)", TaskHandler),  # 任务管理
        (r"/admin/user/([^/]+)", UserHandler),  # 用户管理
    ]
    #tornado.options.parse_command_line()
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    # http_server = tornado.httpserver.HTTPServer(Application(router, default_handler_class=CustomExceptionHandler, debug=(options.env == 'dev')))
    http_server = tornado.httpserver.HTTPServer(Application(router, debug=(options.env == 'dev')))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    # 通过表名, 反向生成Model
    # python app.py gen_model <表名>
    if 'gen_model' in sys.argv:
        from common.GenTool import GenTool
        gen = GenTool()
        table_name = sys.argv[-1]
        gen.gen_model(table_name=table_name)
    elif 'gen_crud' in sys.argv:
        from common.GenTool import GenTool
        # 通过Model名称，生成CRUD页面和功能
        # python app.py gen_crud <Model名称>
        gen = GenTool()
        table_name = sys.argv[-1]
        gen.gen_crud(table_name=table_name)
    else:
        tornado.options.parse_command_line()
        print("项目已启动, 访问地址: http://localhost:%s" % options.port)
        main()
