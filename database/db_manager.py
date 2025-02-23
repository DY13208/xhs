from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    content = Column(Text)
    publish_time = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('mysql+pymysql://root:yourpassword@localhost/xiaohongshu')
Session = sessionmaker(bind=engine)
session = Session()

# 插入数据
new_note = Note(account_id=1, content="今天分享我的生活点滴！")
session.add(new_note)
session.commit()
