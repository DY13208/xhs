from celery_app import celery_app
from core.auth.account_manager import AccountManager
from core.automator.activity_engine import ActivityEngine

accounts = [{"username": "user1", "password": "pass1"}]

@celery_app.task
def run_activity(account):
    """运行账号活跃任务"""
    account_manager = AccountManager([account])
    client = account_manager.get_active_client()

    if client:
        activity = ActivityEngine(client)
        activity.watch_notes(user_id="user123", count=5)
        activity.like_notes(note_ids=["note1", "note2", "note3"])
        activity.comment_on_notes(note_ids=["note1"], comments=["太棒了！", "学习了！"])
