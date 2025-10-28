import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_medium(topic: str):
    """Extrae artículos de Medium relacionados con un tema."""
    url = f"https://medium.com/search?q={topic.replace(' ', '%20')}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    for tag in soup.find_all("a", href=True):
        title = tag.get_text(strip=True)
        link = tag["href"]
        if title and link.startswith("https://medium.com/") and len(title) > 25:
            articles.append({"title": title, "link": link.split("?")[0], "source": "Medium"})
        if len(articles) >= 5:
            break
    return articles


def scrape_devto(topic: str):
    """Extrae artículos de Dev.to."""
    url = f"https://dev.to/search?q={topic.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = []
    for post in soup.find_all("a", class_="crayons-story__hidden-navigation-link", href=True)[:5]:
        link = "https://dev.to" + post["href"]
        title = post["href"].split("/")[-1].replace("-", " ").capitalize()
        articles.append({"title": title, "link": link, "source": "Dev.to"})
    return articles


def scrape_towards_data_science(topic: str):
    """Extrae artículos de Towards Data Science."""
    url = f"https://towardsdatascience.com/search?q={topic.replace(' ', '%20')}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = []
    for tag in soup.find_all("a", href=True):
        if "/towardsdatascience.com/" in tag["href"]:
            title = tag.get_text(strip=True)
            if title and len(title) > 25:
                link = tag["href"].split("?")[0]
                articles.append({"title": title, "link": link, "source": "Towards Data Science"})
        if len(articles) >= 5:
            break
    return articles


def get_articles(topic: str):
    """Combina las tres fuentes y devuelve hasta 5 artículos únicos por fuente."""
    data = scrape_medium(topic) + scrape_devto(topic) + scrape_towards_data_science(topic)
    # eliminar duplicados
    seen = set()
    unique = []
    for d in data:
        if d["link"] not in seen:
            unique.append(d)
            seen.add(d["link"])
    return unique[:15]  # total máx. 15 (5 por fuente)