"""
# 首页
"""
from __future__ import absolute_import

from . import BaseHandler


class IndexHandler(BaseHandler):
    # 首页
    # @admin_bp.get('/')
    # @login_required
    def index(self):
        # user = current_user
        user = {"id": "", "username": ""}
        return self.render_template('admin/index.html', user=user)


    # 控制台页面
    # @admin_bp.get('/welcome')
    # @login_required
    def welcome(self):
        return self.render_template('admin/console/console.html')
