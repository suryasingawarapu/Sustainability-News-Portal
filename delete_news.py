from crud import delete_news_by_sources
from database import SessionLocal

def run_delete():
    db = SessionLocal()
    sources_to_remove = [
    "Greenpeace India",
    "Environmentalist Foundation of India",
    "Down To Earth",
    "Centre for Science and Environment",
    "Council on Energy, Environment and Water",
    "Mongabay India",
    "Delhi Greens",
    "Swechha",
    "Eco-Business",
    "India Together",
    "Indian Express",
    "Times of India"
]

    delete_news_by_sources(db, sources_to_remove)
    db.close()

if __name__ == "__main__":
    run_delete()
