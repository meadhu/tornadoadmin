import time

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler_proj = BlockingScheduler()

@scheduler_proj.scheduled_job('interval', seconds=10)
def my_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# scheduler_proj.start()
