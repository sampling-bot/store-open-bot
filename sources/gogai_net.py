import requests
from bs4 import BeautifulSoup

AREAS = [
    ("小平", "https://kodaira.goguynet.jp/"),
    ("西東京", "https://nishitokyo.goguynet.jp/"),
    ("東久留米・清瀬", "https://higashikurume-kiyose.goguynet.jp/"),
]

OPEN_KEYWORDS = [
    "開店",
    "オープン",
    "NEW OPEN",
    "新店舗",
    "オープニング",
    "グランドオープン",
]

NG_KEYWORDS = [
    "閉店",
    "イベント",
    "オープンキャンパス",
    "オープン戦",
]


def get_gogai():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    articles = []

    for area, url in AREAS:

        r = requests.get(url, headers=headers, timeout=20)

        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "lxml")

        for a in soup.select("a"):

            title = a.get_text(" ", strip=True)
            link = a.get("href")

            if not title or not link:
                continue

            if not link.startswith("http"):
                continue

            if not any(k in title for k in OPEN_KEYWORDS):
                continue

            if any(k in title for k in NG_KEYWORDS):
                continue

            articles.append({
                "title": title,
                "link": link,
                "area": area,
                "place": "自宅",
                "source": "号外NET"
            })

    return articles
