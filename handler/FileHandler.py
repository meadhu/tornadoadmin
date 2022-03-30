"""
# 图片管理
"""
from __future__ import absolute_import

import json

from common.HttpHelper import authorize
from . import BaseHandler


class FileHandler(BaseHandler):
    # @admin_file.get('/')
    @authorize("admin:file:main", log=True)
    def main(self):
        return self.render_template('admin/file/main.html')


    #  图片数据
    # @admin_file.get('/table')
    @authorize("admin:file:main", log=True)
    def data(self):
        # page = request.args.get('page', type=int)
        # limit = request.args.get('limit', type=int)
        # data, count = upload_curd.get_photo(page=page, limit=limit)
        # return table_api(data=data, count=count)
        path = "static/admin/admin/data/fileTable.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])


    #   上传
    # @admin_file.get('/upload')
    @authorize("admin:file:add", log=True)
    def upload(self):
        return self.render_template('admin/file/upload.html')


    #   上传接口
    # @admin_file.post('/upload')
    @authorize("admin:file:add", log=True)
    def upload_api(self):
        # if 'file' in request.files:
        #     photo = request.files['file']
        #     mime = request.files['file'].content_type
        #
        #     file_url = upload_curd.upload_one(photo=photo, mime=mime)
        #     res = {
        #         "msg": "上传成功",
        #         "code": 0,
        #         "success": True,
        #         "data":
        #             {"src": file_url}
        #     }
        #     return jsonify(res)
        return self.fail_api()


    #    图片删除
    # @admin_file.route('/delete', methods=['GET', 'POST'])
    @authorize("admin:file:delete", log=True)
    def delete(self):
        # _id = request.form.get('id')
        # res = upload_curd.delete_photo_by_id(_id)
        # if res:
        #     return success_api(msg="删除成功")
        # else:
        #     return fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")


    # 图片批量删除
    # @admin_file.route('/batchRemove', methods=['GET', 'POST'])
    @authorize("admin:file:delete", log=True)
    def batch_remove(self):
        # ids = request.form.getlist('ids[]')
        # photo_name = Photo.query.filter(Photo.id.in_(ids)).all()
        # upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
        # for p in photo_name:
        #     os.remove(upload_url + '/' + p.name)
        # photo = Photo.query.filter(Photo.id.in_(ids)).delete(synchronize_session=False)
        # db.session.commit()
        # if photo:
        #     return success_api(msg="删除成功")
        # else:
        #     return fail_api(msg="删除失败")
        return self.success_api(msg="删除成功")
