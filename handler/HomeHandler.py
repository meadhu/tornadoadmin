"""
后台首页 - 监控面板
"""
from __future__ import absolute_import

import copy
import json
from collections import OrderedDict

import tornado

from common import session
from common.DbHelper import object_to_dict
from config import SYSTEM_NAME
from models import Power
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
        # 网站配置
        :return:
        """
        # path = "static/admin/admin/data/rights_configs.json"
        # with open(path, 'r') as load_f:
        #     # aa = load_f.read()
        #     self.jsonify(json.loads(load_f.read()))
        config = dict(
            logo={
                "title": SYSTEM_NAME,  # 网站名称
                "image": "/static/admin/admin/images/logo.png"  # 网站图标
            },
            menu={  # 菜单配置
                "data": "/admin/home/rights_menu",  # 菜单数据来源
                "collaspe": False,
                "accordion": True,  # 是否同时只打开一个菜单目录
                "method": "GET",
                "control": False,  # 是否开启多系统菜单模式
                "controlWidth": 500,  # 顶部菜单宽度 PX
                "select": "0",  # 默认选中的菜单项
                "async": True  # 是否开启异步菜单，false 时 data 属性设置为菜单数据，false 时为 json 文件或后端接口
            },
            tab={  # 是否开启多选项卡
                "enable": True,
                "keepState": True,  # 切换选项卡时，是否刷新页面状态
                "session": True,  # 是否开启 Tab 记忆
                "max": 30,  # 最大可打开的选项卡数量
                "index": {
                    "id": "10",  # 标识 ID , 建议与菜单项中的 ID 一致
                    "href": "/admin/home/welcome",  # 页面地址
                    "title": "首页"  # 标题
                }
            },
            theme={
                "defaultColor": "2",  # 默认主题色，对应 colors 配置中的 ID 标识
                "defaultMenu": "dark-theme",  # 默认的菜单主题 dark-theme 黑 / light-theme 白
                "allowCustom": True  # 是否允许用户切换主题，false 时关闭自定义主题面板
            },
            colors=[{"id": "1", "color": "#2d8cf0"},
                    {"id": "2", "color": "#5FB878"},
                    {"id": "3", "color": "#1E9FFF"},
                    {"id": "4", "color": "#FFB800"},
                    {"id": "5", "color": "darkgray"}],
            links=[],
            other={
                "keepLoad": 1200,  # 主页动画时长
                "autoHead": False  # 布局顶部主题
            },
            header=False)
        return self.jsonify(config)

    def rights_menu(self):
        """
        右侧 菜单
        :return:
        """
        path = "static/admin/admin/data/rights_menu.json"
        with open(path, 'r') as load_f:
            # aa = load_f.read()
            self.jsonify(json.loads(load_f.read()))