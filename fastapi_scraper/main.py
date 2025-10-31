from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from scraper import get_articles  # import local

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI()

DEFAULT_QUERY = "Python"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, query: str = DEFAULT_QUERY):
    articles = get_articles(query)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})