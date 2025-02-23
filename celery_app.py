# from celery import Celery
#
# celery_app = Celery(
#     "xhs_tasks",
#     broker="redis://localhost:6379/0",  # 任务队列使用 Redis
#     backend="redis://localhost:6379/0"
# )
#
# celery_app.conf.update(
#     task_serializer="json",
#     result_serializer="json",
#     timezone="Asia/Shanghai",
#     enable_utc=False
# )
from celery import Celery

celery_app = Celery(
    "xhs_tasks",
    broker="memory://",           # 使用内存作为消息队列，仅限于测试环境
    backend="cache+memory://"      # 使用内存缓存作为结果后端
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=False
)
