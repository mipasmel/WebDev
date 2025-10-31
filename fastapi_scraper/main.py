from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import feedparser
from datetime import datetime, date
from scraper import get_articles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

cached_articles = []
cache_date = None

def update_cache():
    global cached_articles, cache_date
    today = date.today()
    if cache_date != today:
        cached_articles = get_articles("python")  # contenido por defecto
        cache_date = today

@app.get("/")
async def home(request: Request, query: str = None):
    update_cache()
    
    if query:
        articles = get_articles(query)
    else:
        articles = cached_articles

    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": articles,
        "query": query or "python"
    })

DEFAULT_QUERY = "programming"  # Artículos por defecto al abrir la app

def get_articles(query: str):
    results = []

    print(f"Buscando artículos sobre: {query}")

    # --- Fuente 1: Towards Data Science (RSS) ---
    try:
        feed_url = "https://towardsdatascience.com/feed"
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if query.lower() in entry.title.lower():
                results.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": "Towards Data Science"
                })
            if len(results) >= 5:
                break
    except Exception as e:
        print("Error en Towards Data Science:", e)

    # --- Fuente 2: Medium "Programming" RSS ---
    try:
        feed_url = "https://medium.com/feed/tag/programming"
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if query.lower() in entry.title.lower():
                results.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": "Medium"
                })
            if len(results) >= 5:
                break
    except Exception as e:
        print("Error en Medium:", e)

    # Si no hay resultados, mostramos artículos genéricos recientes
    if not results:
        try:
            for feed_url in ["https://towardsdatascience.com/feed", "https://medium.com/feed/tag/programming"]:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    results.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": "Towards Data Science" if "towardsdatascience" in feed_url else "Medium"
                    })
        except:
            pass

    print(f"Artículos encontrados: {len(results)}")
    return results[:5]


# -------- Ruta principal -------- #
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, query: str = None):
    search_term = query if query else DEFAULT_QUERY
    articles = get_articles(search_term)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles, "query": search_term})