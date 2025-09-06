import asyncio
import feedparser
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

app = FastAPI(title="🌍 Sustainability News API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def init_db():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            link TEXT UNIQUE,
            summary TEXT,
            published_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Feeds + Keywords 
feed_urls = [
    "https://www.pv-tech.org/feed/",
    "https://www.mercomindia.com/feed/",
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "https://www.thehindu.com/sci-tech/energy-and-environment/feeder/default.rss",
    "https://cleantechnica.com/feed/",
    "https://earthobservatory.nasa.gov/feeds/eo.rss",
    "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml",
    "https://www.climatechangenews.com/feed/",
    "https://techcrunch.com/tag/green-tech/feed/",
    "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
    
]

keywords = [
    "climate", "sustainability", "green", "renewable", "solar", "wind", "energy",
    "carbon", "net zero", "decarbonization", "hydrogen", "clean tech",
    "pollution", "biodiversity", "deforestation", "conservation",
    "global warming", "emissions", "environment", "ecology",
    "water crisis", "recycling", "circular economy", "nature",
    "wildlife", "climate action", "climate change", "fossil fuels",
    "climate policy", "carbon footprint", "energy efficiency", "climate resilience",
    "sustainable development", "greenhouse gases", "climate finance", "urban sustainability",
    "electric vehicles", "carbon capture", "afforestation", "reforestation",
    "ocean conservation", "sustainable agriculture", "environmental justice",
    "clean energy", "eco-friendly", "wildlife protection", "water conservation",
    "air quality", "environmental impact", "climate adaptation", "zero emissions",
    "green jobs", "sustainable transport", "electric mobility", "carbon trading",
    "climate summit", "circular economy", "green innovation", "sustainable cities",
    "energy transition", "fossil fuel phase-out"
] 


# Fetch + Store News
async def fetch_news():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    for url in feed_urls:
        feed = feedparser.parse(url)
        source = feed.feed.get("title", "Unknown")

        for entry in feed.entries[:10]:  
            title = entry.title
            summary = getattr(entry, "summary", "")
            link = getattr(entry, "link", "")
            published = getattr(entry, "published", str(datetime.now()))

           
            if any(word in title.lower() for word in keywords):
                
                cursor.execute("SELECT 1 FROM news WHERE link = ?", (link,))
                if cursor.fetchone() is None:
                    cursor.execute("""
                        INSERT INTO news (source, title, link, summary, published_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (source, title, link, summary, published))

    conn.commit()
    conn.close()

async def background_news_updater():
    while True:
        await fetch_news()
        await asyncio.sleep(1800) 

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_news_updater())

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/news")
def get_news(limit: int = 20):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT source, title, link, summary, published_at FROM news ORDER BY id DESC LIMIT ?", 
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    return JSONResponse([
        {"source": r[0], "title": r[1], "link": r[2], "summary": r[3], "published_at": r[4]}
        for r in rows
    ])

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
