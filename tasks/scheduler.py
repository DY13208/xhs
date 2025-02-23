import schedule
import time
from core.publish import Publisher
from core.activity import Activity

def daily_task():
    # 示例：执行每日任务
    print("开始执行每日任务...")
    activity = Activity(token="your_token")
    activity.watch_notes()

# 每天早上9点执行任务
schedule.every().day.at("09:00").do(daily_task)

while True:
    schedule.run_pending()
    time.sleep(1)
