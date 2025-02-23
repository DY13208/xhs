import time
import random
from core.utils.logger import logger

class ActivityEngine:
    """活跃引擎（自动点赞/评论/收藏）"""

    def __init__(self, client):
        self.client = client

    def watch_notes(self, user_id, count=5):
        """随机观看指定数量的笔记"""
        notes = self.client.fetch_notes(user_id)
        for note in random.sample(notes, min(count, len(notes))):
            logger.info(f"模拟观看笔记：{note['title']}")
            time.sleep(random.uniform(1, 3))  # 模拟阅读笔记的时间

    def like_notes(self, note_ids):
        """自动点赞多个笔记"""
        for note_id in note_ids:
            self.client.like_note(note_id)
            time.sleep(random.uniform(2, 5))  # 模拟人工操作的时间间隔

    def comment_on_notes(self, note_ids, comments):
        """自动评论多个笔记"""
        for note_id in note_ids:
            comment = random.choice(comments)
            logger.info(f"在笔记 {note_id} 上发表评论：{comment}")
            # 这里可以调用实际评论 API
            time.sleep(random.uniform(3, 6))
