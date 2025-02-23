from sqlalchemy.orm import Session
from database.models import NoteRecord, CommentRecord

def create_note_record(db: Session, title: str, content: str, images: list):
    """创建笔记发布记录"""
    note = NoteRecord(title=title, content=content, images=str(images))
    db.add(note)
    db.commit()
    db.refresh(note)
    print(f"[INFO] 已创建笔记记录：{note.id}")
    return note

def create_comment_record(db: Session, note_id: str, comment_text: str):
    """创建评论记录"""
    comment = CommentRecord(note_id=note_id, comment_text=comment_text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    print(f"[INFO] 已创建评论记录：{comment.id}")
    return comment

def get_all_notes(db: Session):
    """查询所有笔记发布记录"""
    return db.query(NoteRecord).all()

def get_all_comments(db: Session):
    """查询所有评论记录"""
    return db.query(CommentRecord).all()
