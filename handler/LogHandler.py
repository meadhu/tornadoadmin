"""
# 日志管理
"""
from __future__ import absolute_import

import json
import traceback

import tornado
from sqlalchemy import and_, desc
from sqlalchemy_pagination import paginate
from tornado.escape import json_decode
from tornado.escape import xhtml_escape as xss_escape

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import authorize
from models import AdminLog
from models.admin_role import Role
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
        # path = "static/admin/admin/data/loginLog.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.table_api(data=data['data'], count=data['count'])
        # orm查询
        # 使用分页获取data需要.items
        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))
        query = session.query(AdminLog).filter_by(url='/passport/login').order_by(desc(AdminLog.create_time))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        return self.table_api(data=data, count=page_result.total)

    # 操作日志
    # @admin_log.get('/operateLog')
    @authorize("admin:log:main")
    def operate_log(self):
        # path = "static/admin/admin/data/operateLog.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.table_api(data=data['data'], count=data['count'])
        # orm查询
        # 使用分页获取data需要.items
        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))
        query = session.query(AdminLog).filter(AdminLog.url != '/passport/login').order_by(desc(AdminLog.create_time))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        return self.table_api(data=data, count=page_result.total)

