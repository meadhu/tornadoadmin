"""
后台首页 - 监控面板
"""
from __future__ import absolute_import

import json

import tornado

from . import BaseHandler


class HomeHandler(BaseHandler):
    def main(self):
        """
        主入口 文件
        :return:
        """
        return self.render("admin/home.html")

    def welcome(self):
        """
        默认主页
        :return:
        """
        self.render("admin/console/console.html")
        # self.render("home/welcome.html")

    def rights_configs(self):
        """
        :return:
        """
        path = "static/admin/admin/data/rights_configs.json"
        with open(path, 'r') as load_f:
            # aa = load_f.read()
            self.jsonify(json.loads(load_f.read()))

    def rights_menu(self):
        path = "static/admin/admin/data/rights_menu.json"
        with open(path, 'r') as load_f:
            # aa = load_f.read()
            self.jsonify(json.loads(load_f.read()))