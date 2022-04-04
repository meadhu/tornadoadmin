"""
# 图片管理
"""
from __future__ import absolute_import

import datetime
import json
import os

import tornado
from sqlalchemy import and_
from sqlalchemy_pagination import paginate
from tornado.escape import json_decode
from tornado.escape import xhtml_escape as xss_escape

from common import session
from common.DbHelper import object_to_dict
from common.HttpHelper import authorize
from config import UPLOADED_PHOTOS_DEST
from models import Photo
from . import BaseHandler


class FileHandler(BaseHandler):
    @authorize("admin:file:main", log=True)
    def main(self):
        return self.render_template('admin/file/main.html')

    # 图片数据
    @authorize("admin:file:main", log=True)
    def data(self):
        # path = "static/admin/admin/data/fileTable.json"
        # with open(path, 'r') as load_f:
        #     data = json.loads(load_f.read())
        #     self.table_api(data=data['data'], count=data['count'])

        # 获取请求参数
        page = xss_escape(self.get_argument('page', self.settings['config']['default_page'].encode()))
        page_size = xss_escape(self.get_argument('limit', self.settings['config']['default_page_size'].encode()))

        query = session.query(Photo)
        rule_list = []
        query = query.filter(and_(*rule_list))
        page_result = paginate(query=query, page=int(page), page_size=int(page_size))
        result = page_result.items
        data = [object_to_dict(i) for i in result]
        domain_url = self.request.protocol + "://" + self.request.host + "/"
        for item in data:
            item['href'] = domain_url + UPLOADED_PHOTOS_DEST+item['href']
        return self.table_api(data=data, count=page_result.total)

    # 上传页面
    @authorize("admin:file:add", log=True)
    def upload(self):
        return self.render_template('admin/file/upload.html')

    # 上传接口
    @authorize("admin:file:add", log=True)
    def uploadapi(self):
        # print(self.get_argument("files", ""))
        # print(self.request.files)
        # return self.fail_api()
        if 'file' in self.request.files:
            file_obj = self.request.files['file'][0]
            filename = file_obj['filename']
            file_ext = filename.split(".")[-1]
            filename = ".".join([datetime.datetime.now().strftime("%Y%m%d%H%M%S"), file_ext])
            mime = file_obj['content_type']
            body = file_obj['body']
            # 文件夹不存在时 创建
            file_url = '/photos/' + filename
            if not os.path.exists(UPLOADED_PHOTOS_DEST + '/photos/'):
                os.mkdir(UPLOADED_PHOTOS_DEST + '/photos/')
            # 写入文件
            fd = os.open(UPLOADED_PHOTOS_DEST + file_url, os.O_RDWR | os.O_CREAT)
            os.write(fd, body)
            # 计算文件大小
            size = os.path.getsize(UPLOADED_PHOTOS_DEST + file_url)
            # 存储到DB
            photo = Photo(name=filename, href=file_url, mime=mime, size=size)
            session.add(photo)
            session.commit()
            res = {
                "msg": "上传成功",
                "code": 0,
                "success": True,
                "data": {"src": file_url}
            }
            return self.jsonify(res)

    # 图片删除
    @authorize("admin:file:delete", log=True)
    def delete(self):
        _id = self.get_argument('id', '')
        if not _id:
            return self.fail_api(msg="数据格式错误!")
        res = session.query(Photo).filter_by(id=_id).delete()
        if res:
            return self.success_api(msg="删除成功")
        else:
            return self.fail_api(msg="删除失败")

    # 图片批量删除
    @authorize("admin:file:delete", log=True)
    def batch_remove(self):
        ids = self.get_arguments('ids[]')
        photo_name = session.query(Photo).filter(Photo.id.in_(ids)).all()
        upload_url = UPLOADED_PHOTOS_DEST
        for p in photo_name:
            os.remove(upload_url + '/' + p.name)
        photo = session.query(Photo).filter(Photo.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        if photo:
            return self.success_api(msg="删除成功")
        else:
            return self.fail_api(msg="删除失败")
