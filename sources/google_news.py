import feedparser
from urllib.parse import quote


def get_google_news(areas, keywords):
    articles = []

    for area in areas:
        query = f'{area} ({" OR ".join(keywords)})'

        url = (
            "https://news.google.com/rss/search?"
            f"q={quote(query)}&hl=ja&gl=JP&ceid=JP:ja"
        )

        feed = feedparser.parse(url)

        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "area": area
            })

    return articles
