import feedparser

def get_articles(query: str):
    feeds = [
        ("Real Python", f"https://realpython.com/atom.xml"),
        ("Dev.to", f"https://dev.to/feed/tag/{query.lower()}")
    ]
    articles = []
    for source, url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # top 5 por feed
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "source": source
            })
    return articles