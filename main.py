# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud

# Create tables once at startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sustainability News API")

# Dependency: DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Startup event → auto populate news
@app.on_event("startup")
def populate_news_on_startup():
    db = SessionLocal()
    try:
        # ✅ Example static data (you can replace with API call later)
        initial_news = [
            {"title": "AI in Sustainability", "content": "How AI helps climate change.", "source": "TechCrunch"},
            {"title": "Green Energy", "content": "India moves towards 50% renewable energy by 2030.", "source": "Economic Times"},
            {"title": "Recycling Innovation", "content": "New startup converts plastic waste into fuel.", "source": "BBC"},
        ]
        for item in initial_news:
            crud.create_news(db, item["title"], item["content"], item["source"])
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/news")
def list_news(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_latest_news(db, limit=limit)
