"""
# 首页
"""
from __future__ import absolute_import

import tornado

from . import BaseHandler


class IndexHandler(BaseHandler):
    # 首页
    def main(self):
        user = self.current_user if self.current_user else {"id": "", "username": "未登录"}
        return self.render_template('index/index.html', user=user)