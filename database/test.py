from database.xhs_database import SessionLocal
from database.crud import create_note_record, create_comment_record, get_all_notes, get_all_comments

# 创建数据库会话
db = SessionLocal()

# 示例：插入笔记记录
create_note_record(db, title="今日穿搭推荐", content="这是一篇关于穿搭的分享", images=["img1.jpg", "img2.jpg"])

# 示例：插入评论记录
create_comment_record(db, note_id="note12345", comment_text="真不错！学习了！")

# 查询所有笔记
notes = get_all_notes(db)
print("[INFO] 所有笔记记录：")
for note in notes:
    print(note.id, note.title, note.content)

# 查询所有评论
comments = get_all_comments(db)
print("[INFO] 所有评论记录：")
for comment in comments:
    print(comment.id, comment.note_id, comment.comment_text)

# 关闭数据库会话
db.close()
