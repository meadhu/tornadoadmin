

config_params = {
    # MySql 配置信息
    "MYSQL_HOST": "tornadoadmin-mysql",
    "MYSQL_DATABASE": "tornadoadmin",
    "MYSQL_PORT": 3306,
    "MYSQL_USERNAME": "root",
    "MYSQL_PASSWORD": "root",

    # 分页 string 类型
    "default_page": '1',
    "default_page_size": '10',
}

#
SYSTEM_NAME = "tornadoadmin后台"

# 文件上传目录
UPLOADED_PHOTOS_DEST = 'static/upload'
UPLOADED_FILES_ALLOW = ['gif', 'jpg']