"""
# 日志管理
"""
from __future__ import absolute_import

import json

from common.HttpHelper import authorize
from . import BaseHandler


class LogHandler(BaseHandler):
    # 日志管理
    # @admin_log.get('/')
    @authorize("admin:log:main")
    def main(self):
        return self.render_template('admin/admin_log/main.html')


    # 登录日志
    # @admin_log.get('/loginLog')
    @authorize("admin:log:main")
    def login_log(self):
        # orm查询
        # 使用分页获取data需要.items
        # log = AdminLog.query.filter_by(url='/passport/login').order_by(desc(AdminLog.create_time)).layui_paginate()
        # count = log.total
        # return table_api(data= model_to_dicts(schema=LogOutSchema, data=log.items), count=count)
        path = "static/admin/admin/data/loginLog.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])


    # 操作日志
    # @admin_log.get('/operateLog')
    @authorize("admin:log:main")
    def operate_log(self):
        # orm查询
        # 使用分页获取data需要.items
        # log = AdminLog.query.filter(
        #     AdminLog.url != '/passport/login').order_by(
        #     desc(AdminLog.create_time)).layui_paginate()
        # count = log.total
        # return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)
        path = "static/admin/admin/data/operateLog.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])
