from sqlalchemy.orm import Session
from models import News
from datetime import datetime


# Create a new news entry
def create_news(db: Session, title: str, content: str, source: str):
    db_news = News(
        title=title,
        summary=content,
        source=source,
        published_at=datetime.utcnow()
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


# Get latest news
def get_latest_news(db: Session, limit: int = 10):
    return db.query(News).order_by(News.published_at.desc()).limit(limit).all()


# Delete news entries by source list
def delete_news_by_sources(db: Session, sources_to_delete: list):
    db.query(News).filter(News.source.in_(sources_to_delete)).delete(synchronize_session="fetch")
    db.commit()
