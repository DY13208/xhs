import time
from apscheduler.schedulers.background import BackgroundScheduler
from tasks.tasks import run_activity  # 使用绝对导入
from core.utils.logger import logger


def schedule_tasks():
    # """
    # 使用 APScheduler 调度 Celery 任务。
    #
    # 示例：
    #   - 每天 9:00 触发一次 run_activity 任务；
    #   - 每小时触发一次 run_activity 任务；
    # Celery 任务将异步执行单账号的活跃操作。
    # """
    scheduler = BackgroundScheduler()

    # 每天早上9点触发 run_activity 任务（使用 Celery 的 delay 方法）
    scheduler.add_job(run_activity.delay, 'cron', hour=9, minute=0)

    # 每小时触发一次 run_activity 任务
    scheduler.add_job(run_activity.delay, 'interval', hours=1)

    scheduler.start()
    logger.info("任务调度器已启动。")

    try:
        # 持续运行保持调度器活跃
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("任务调度器接收到终止信号，正在关闭...")
        scheduler.shutdown()


if __name__ == "__main__":
    schedule_tasks()
