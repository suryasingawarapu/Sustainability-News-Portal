# models.py
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    link = Column(String(500))
    source = Column(String(100))
    summary = Column(Text)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
