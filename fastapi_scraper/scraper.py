import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_realpython(query="python"):
    url = f"https://realpython.com/search?q={query}"
    response = requests.get(url)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".card .card-body h2 a")[:5]  # tomar solo 5 primeros
        for r in results:
            articles.append({
                "title": r.text.strip(),
                "link": "https://realpython.com" + r["href"],
                "source": "Real Python"
            })
    return articles

def scrape_devto(query="python"):
    url = f"https://dev.to/search?q={query}"
    response = requests.get(url)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".crayons-story__title a")[:5]
        for r in results:
            articles.append({
                "title": r.text.strip(),
                "link": "https://dev.to" + r["href"],
                "source": "Dev.to"
            })
    return articles

def get_articles(query="python"):
    articles = scrape_realpython(query) + scrape_devto(query)
    return articles[:5]  # máximo 5 artículos combinados