"""
# 权限管理
"""
from __future__ import absolute_import


import json
import traceback

import tornado
from sqlalchemy import and_
from sqlalchemy_pagination import paginate
from tornado.escape import json_decode
from tornado.escape import xhtml_escape as xss_escape

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import authorize
from models import Power
from . import BaseHandler


class PowerHandler(BaseHandler):
    # 权限管理
    # @admin_power.get('/')
    @authorize("admin:power:main", log=True)
    def main(self):
        return self.render_template('admin/power/main.html')

    # @admin_power.post('/data')
    @authorize("admin:power:main", log=True)
    def data(self):
        result = session.query(Power).all()
        data = [object_to_dict(i) for i in result]
        for item in data:
            item['powerId'] = item['id']
            item['powerName'] = item['name']
            item['powerType'] = item['type']
            item['parentId'] = item['parent_id']
        return self.jsonify({"data": data})
        # path = "static/admin/admin/data/power.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.jsonify(data)

    # @admin_power.get('/add')
    @authorize("admin:power:add", log=True)
    def add(self):
        return self.render_template('admin/power/add.html')

    # @admin_power.get('/selectParent')
    @authorize("admin:power:main", log=True)
    def select_parent(self):
        result = session.query(Power).all()
        data = [object_to_dict(i) for i in result]
        for item in data:
            item['powerId'] = item['id']
            item['powerName'] = item['name']
            item['powerType'] = item['type']
            item['parentId'] = item['parent_id']
        data.append({"powerId": 0, "powerName": "顶级权限", "parentId": -1})
        res = {
            "status": {"code": 200, "message": "默认"},
            "data": data
        }
        return self.jsonify(res)
        # path = "static/admin/admin/data/powerSelectParent.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.jsonify(data)

    # 增加
    # @admin_power.post('/save')
    @authorize("admin:power:add", log=True)
    def save(self):
        req_json = json_decode(self.request.body)
        icon = xss_escape(req_json.get("icon", ""))
        openType = xss_escape(req_json.get("openType", ""))
        parentId = xss_escape(req_json.get("parentId", ""))
        powerCode = xss_escape(req_json.get("powerCode", ""))
        powerName = xss_escape(req_json.get("powerName", ""))
        powerType = xss_escape(req_json.get("powerType", ""))
        powerUrl = xss_escape(req_json.get("powerUrl", ""))
        sort = xss_escape(req_json.get("sort", ""))
        power = Power(
            icon=icon,
            open_type=openType,
            parent_id=parentId,
            code=powerCode,
            name=powerName,
            type=powerType,
            url=powerUrl,
            sort=sort,
            enable=1
        )
        try:
            session.add(power)
            session.commit()
        except:
            session.rollback()
            print(traceback.format_exc())
            return self.fail_api()
        return self.success_api(msg="保存成功")

    # 权限编辑
    # @admin_power.get('/edit/<int:_id>')
    @authorize("admin:power:edit", log=True)
    def edit(self):
        _id = self.get_argument("powerId", "")
        if not _id:
            return self.fail_api("数据错误!")
        power = session.query(Power).filter_by(id=_id).first()
        icon_list = str(power.icon).split()
        icon = icon_list[1] if len(icon_list) == 2 else None
        return self.render_template('admin/power/edit.html', power=object_to_dict(power), icon=icon)

    # 权限更新
    # @admin_power.put('/update')
    @authorize("admin:power:edit", log=True)
    def update(self):
        req_json = json_decode(self.request.body)
        id = req_json.get("powerId", "")
        data = {
            "icon": xss_escape(req_json.get("icon", "")),
            "open_type": xss_escape(req_json.get("openType", "")),
            "parent_id": xss_escape(req_json.get("parentId", "")),
            "code": xss_escape(req_json.get("powerCode", "")),
            "name": xss_escape(req_json.get("powerName", "")),
            "type": xss_escape(req_json.get("powerType", "")),
            "url": xss_escape(req_json.get("powerUrl", "")),
            "sort": xss_escape(req_json.get("sort", ""))
        }
        res = session.query(Power).filter_by(id=id).update(data)
        session.commit()
        if not res:
            return self.fail_api(msg="更新权限失败")
        return self.success_api(msg="更新权限成功")

    # 启用
    # @admin_power.put('/enable')
    @authorize("admin:power:edit", log=True)
    def enable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get("powerId", "")
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(Power).filter_by(id=_id).update({"enable": 1})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="启用成功")

    # 禁用
    # @admin_power.put('/disable')
    @authorize("admin:power:edit", log=True)
    def disable(self):
        req_json = json_decode(self.request.body)
        _id = req_json.get("powerId", "")
        if not _id:
            return self.fail_api(msg="数据错误")
        res = session.query(Power).filter_by(id=_id).update({"enable": 0})
        if not res:
            return self.fail_api(msg="出错啦")
        return self.success_api(msg="禁用成功")


    # 权限删除
    # @admin_power.delete('/remove/<int:id>')
    @authorize("admin:power:remove", log=True)
    def remove(self):
        # power = Power.query.filter_by(id=id).first()
        # power.role = []
        #
        # r = Power.query.filter_by(id=id).delete()
        # db.session.commit()
        # if r:
        #     return success_api(msg="删除成功")
        # else:
        #     return fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")


    # 批量删除
    # @admin_power.delete('/batchRemove')
    @authorize("admin:power:remove", log=True)
    def batch_remove(self):
        # ids = request.form.getlist('ids[]')
        # for id in ids:
        #     power = Power.query.filter_by(id=id).first()
        #     power.role = []
        #
        #     r = Power.query.filter_by(id=id).delete()
        #     db.session.commit()
        return self.success_api(msg="批量删除成功")
