from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class NoteRecord(Base):
    """笔记发布记录表"""
    __tablename__ = "note_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    images = Column(Text, nullable=True)  # 图片列表，存储为 JSON 格式
    created_at = Column(DateTime, default=datetime.utcnow)


class CommentRecord(Base):
    """评论记录表"""
    __tablename__ = "comment_records"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(String(50), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
