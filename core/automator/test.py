from core.automator.activity_engine import ActivityEngine
from core.automator.publish_engine import PublishEngine

note_ids = ["note1", "note2", "note3"]  # 示例笔记 ID 列表

# 模拟自动活跃行为
activity_engine = ActivityEngine(client)
activity_engine.simulate_activity(note_ids, max_actions=10)

# 定时发布笔记
notes = [
    {"title": "旅行笔记", "content": "分享我的旅行故事", "images": ["image1.jpg", "image2.jpg"]},
    {"title": "时尚穿搭", "content": "今日穿搭推荐", "images": ["image3.jpg"]}
]
publish_engine = PublishEngine(client)
publish_engine.schedule_publish(notes, publish_interval=86400)  # 每天发布一篇
