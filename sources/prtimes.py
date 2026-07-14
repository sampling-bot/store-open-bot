import feedparser

RSS_URL = "https://prtimes.jp/topics/rss.xml"


def get_prtimes():
    feed = feedparser.parse(RSS_URL)

    articles = []

    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "area": "",
            "source": "PR TIMES"
        })

    return articles
