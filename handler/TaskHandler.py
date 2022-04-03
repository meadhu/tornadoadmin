"""
# 任务管理
"""
from __future__ import absolute_import

import json

from common import scheduler_proj
from . import BaseHandler


class TaskHandler(BaseHandler):
    # 任务管理
    # @admin_task.route('/add_job', methods=['GET'])
    def add_task(self):
        # scheduler.add_job(func=tasks.get(), id='4', args=(1, 1), trigger='interval', seconds=3,
        #                   replace_existing=True)
        return '6'

    # @admin_task.get('/')
    def main(self):
        return self.render_template('admin/task/main.html')

    # 获取
    # @admin_task.route('/data', methods=['GET'])
    def data(self):
        # jobs = scheduler_proj.get_jobs()
        # print(jobs)
        # jobs_list = []
        # for job in jobs:
        #     jobs_list.append(job_to_dict(job))
        # return self.table_api(data=jobs_list, count=len(jobs_list))
        path = "static/admin/admin/data/taskList.json"
        with open(path, 'r') as load_f:
            data = json.loads(load_f.read())
            self.table_api(data=data['data'], count=data['count'])

    # 增加
    # @admin_task.get('/add')
    def add(self):
        task_list = []
        return self.render_template('admin/task/add.html', task_list=task_list)

    # @admin_task.post('/save')
    def save(self):
        # _id = request.json.get("id")
        # name = request.json.get("id")
        # type = request.json.get("type")
        # functions = request.json.get("functions")
        # datetime = request.json.get("datetime")
        # time = request.json.get("time")
        # if not hasattr(tasks, functions):
        #     return fail_api()
        # if type == 'date':
        #     scheduler.add_job(
        #         func=getattr(tasks, functions),
        #         id=_id,
        #         name=name,
        #         args=(1, 1),
        #         trigger=type,
        #         run_date=datetime,
        #         replace_existing=True)
        # elif type == 'interval':
        #     scheduler.add_job(
        #         func=getattr(tasks, functions),
        #         id=_id,
        #         name=name,
        #         args=(1, 1),
        #         trigger=type,
        #         replace_existing=True)
        # elif type == 'cron':
        #     scheduler.add_job(
        #         func=getattr(tasks, functions),
        #         id=_id,
        #         name=name,
        #         args=(1, 1),
        #         trigger=type,
        #         replace_existing=True)
        return self.success_api()

    # 恢复
    # @admin_task.put('/enable')
    def enable(self):
        # _id = request.json.get('id')
        # # print(id)
        # if _id:
        #     scheduler.resume_job(str(_id))
        #     return success_api(msg="启动成功")
        return self.fail_api(msg="数据错误")

    # 暂停
    # @admin_task.put('/disable')
    def disable(self):
        # _id = request.json.get('id')
        # if _id:
        #     scheduler.pause_job(str(_id))
        #     return success_api(msg="暂停成功")
        return self.fail_api(msg="数据错误")

    # 移除
    # @admin_task.delete('/remove/<int:_id>')
    def remove(self):
        # scheduler.remove_job(str(_id))
        return self.success_api(msg="删除成功")

        #     scheduler.add_job(func=task1, id='2', args=(1, 1), trigger='cron', day_of_week='0-6', hour=18, minute=24,
        #                       second=10, replace_existing=True)

        #     scheduler.add_job(func=task4, id='4', args=(2, 2), trigger='interval', seconds=3,
        #                       replace_existing=True, misfire_grace_time=3)

        #     # trigger='interval' 表示是一个循环任务，每隔多久执行一次
        #     scheduler.add_job(func=task2, id='3', args=(2, 2), trigger='interval', seconds=3,
        #                       replace_existing=True)
