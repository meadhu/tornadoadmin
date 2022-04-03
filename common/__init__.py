# 创建全局连接池
import os

# 定时任务
from common.ApsChedulerHelper import scheduler_proj

from common.DbHelper import init_db

engine, BaseModel, session, conection = init_db()

if os.environ.get('app_env') == 'dev':
    print(__file__)