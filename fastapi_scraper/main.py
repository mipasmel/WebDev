from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Base, engine, SessionLocal, Article
from scraper import get_articles
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = SessionLocal()
    articles = db.query(Article).order_by(Article.date_added.desc()).limit(50).all()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/update/{topic}")
def update_articles(topic: str):
    db = SessionLocal()
    data = get_articles(topic)
    count = 0
    for item in data:
        # evitar duplicados
        exists = db.query(Article).filter(Article.link == item["link"]).first()
        if not exists:
            article = Article(
                title=item["title"],
                link=item["link"],
                source=item["source"],
                topic=topic,
                date_added=datetime.utcnow()
            )
            db.add(article)
            count += 1
    db.commit()
    return {"status": "updated", "added": count}