"""
# 首页
"""
from __future__ import absolute_import

from . import BaseHandler


class IndexHandler(BaseHandler):
    # 首页
    # @admin_bp.get('/')
    # @login_required
    def main(self):
        # user = current_user
        user = {"id": "", "username": ""}
        return self.render_template('index/index.html', user=user)