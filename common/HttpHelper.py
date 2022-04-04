from __future__ import absolute_import

import json
from functools import wraps
from typing import Dict, Any

import tornado.web
from tornado.escape import xhtml_escape as xss_escape

from common import session
from models import AdminLog


def login_log(request, uid, is_access):
    info = {
        'method': request.method,
        'url': request.path,
        'ip': request.remote_ip,
        'user_agent': xss_escape(request.headers.get('User-Agent')),
        # 'desc': xss_escape(request.get_argument('username', '')),
        'uid': uid,
        'success': int(is_access)
    }
    log = AdminLog(**info)
    session.add(log)
    session.flush()
    session.commit()
    return log.id


def admin_log(request, uid, is_access):
    info = {
        'method': request.method,
        'url': request.path,
        'ip': request.remote_ip,
        'user_agent': xss_escape(request.headers.get('User-Agent')),
        'desc': request.body,
        'uid': uid,
        'success': int(is_access)
    }
    log = AdminLog(**info)
    session.add(log)
    session.commit()
    return log.id


def authorize(power: str, log: bool = False):
    def decorator(func):
        @tornado.web.authenticated
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0].request

            print(request)
            print(request.body)
            print(**kwargs)
            # if not power in session.get('permissions'):
            #     if log:
            #         admin_log(request=request, is_access=False)
            #     if request.method == 'GET':
            #         abort(403)
            #     else:
            #         return jsonify(success=False, msg="权限不足!")
            if log:
                admin_log(request=request, uid=10, is_access=True)
            return func(*args, **kwargs)

        return wrapper

    return decorator


class HttpHelper(tornado.web.RequestHandler):
    def jsonify(self, *args, **kwargs):
        self.set_header("Content-Type", "text/json")
        indent = None
        separators = (",", ":")
        # if debug:  # 获取全局debug配置
        #     indent = 2
        #     separators = (", ", ": ")

        if args and kwargs:
            raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args[0]
        else:
            data = args or kwargs
        self.write(json.dumps(data, indent=indent, separators=separators))

    def write_to_json(self, code=0, msg="", count=0, data=None):
        data = data if data else []
        ret = {"code": code, "msg": msg, "count": count if count else len(data), "data": data}
        self.write(json.dumps(ret))

    def success_api(self, msg: str = "成功"):
        """ 成功响应 默认值”成功“ """
        return self.jsonify(success=True, msg=msg)

    def fail_api(self, msg: str = "失败"):
        """ 失败响应 默认值“失败” """
        return self.jsonify(success=False, msg=msg)

    def table_api(self, msg: str = "", count=0, data=None, limit=10):
        """ 动态表格渲染响应 """
        res = {
            'msg': msg,
            'code': 0,
            'data': data,
            'count': count,
            'limit': limit
        }
        return self.jsonify(res)

    # def authorize(self, code=None):
    #     return authorize(code=code)

    def url_for(self, file_path=None, filename=None):
        if file_path == "static":
            # self.application.static_path
            filename = filename[1:] if filename[:1] == '/' else filename
            return self.static_url(filename)

    def get_template_namespace(self) -> Dict[str, Any]:
        namespace = super().get_template_namespace()
        # namespace.update({"url_for": self.url_for, "authorize": self.authorize})
        namespace.update({"url_for": self.url_for, "authorize": authorize})
        return namespace


class NoResultError(Exception):
    pass