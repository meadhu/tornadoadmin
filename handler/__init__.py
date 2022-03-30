"""
初始化文件
"""

from __future__ import absolute_import

from .BaseHandler import BaseHandler


class My404(BaseHandler):
    def get(self):
        self.render('errors/404')


from .AuthHandler import AuthHandler
from .DeptHandler import DeptHandler
from .DictHandler import DictHandler
from .FileHandler import FileHandler
from .HomeHandler import HomeHandler
from .IndexHandler import IndexHandler
from .LogHandler import LogHandler
from .MonitorHandler import MonitorHandler
from .PowerHandler import PowerHandler
from .RoleHandler import RoleHandler
from .TaskHandler import TaskHandler
from .UserHandler import UserHandler