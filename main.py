import os

from config import AREAS, KEYWORDS
from line_notify import send_line

from sources.google_news import get_google_news
from sources.prtimes import get_prtimes

SENT_FILE = "sent_store.txt"


def load_sent():
    if not os.path.exists(SENT_FILE):
        return set()

    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)


def save_sent(sent):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(sent)))


sent = load_sent()

# 全記事をここに集める
all_articles = []


# ---------- Google News ----------
for place, area_list in AREAS.items():
    for area in area_list:

        news = get_google_news([area], KEYWORDS)

        for article in news:
            article["place"] = place
            article["source"] = "Google News"
            all_articles.append(article)


# ---------- PR TIMES ----------
for article in get_prtimes():

    title = article["title"]

    for place, area_list in AREAS.items():
        if any(area in title for area in area_list):
            article["place"] = place
            article["area"] = next(
                area for area in area_list if area in title
            )
            all_articles.append(article)
            break


# ---------- 重複除去 ----------
new_articles = []

for article in all_articles:

    if article["link"] in sent:
        continue

    sent.add(article["link"])
    new_articles.append(article)


save_sent(sent)


# ---------- LINE通知 ----------

if not new_articles:
    send_line("今日は新しい開店情報はありませんでした😊")

else:

    message = "🆕 新しい開店情報\n\n"

    current_place = ""

    for article in new_articles[:10]:

        if article["place"] != current_place:
            current_place = article["place"]
            message += f"\n🏢 {current_place}\n"

        message += (
            f"📍{article['area']}\n"
            f"【{article['source']}】\n"
            f"{article['title']}\n"
            f"{article['link']}\n\n"
        )

    send_line(message)
