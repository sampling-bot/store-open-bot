import os

from config import AREAS, KEYWORDS
from line_notify import send_line
from sources.google_news import get_google_news

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

new_articles = []
from sources.prtimes import get_prtimes

articles.extend(get_prtimes())

for place, area_list in AREAS.items():
    for area in area_list:
        articles = get_google_news([area], KEYWORDS)

        for article in articles:
            if article["link"] not in sent:
                article["place"] = place
                new_articles.append(article)
                sent.add(article["link"])

save_sent(sent)

if not new_articles:
    send_line("今日は新しい開店情報はありませんでした😊")

else:
    message = "🆕 新しい開店情報\n\n"

    current_place = ""

    for article in new_articles[:10]:

        if current_place != article["place"]:
            current_place = article["place"]
            message += f"\n🏢 {current_place}\n"

        message += (
            f"📍{article['area']}\n"
            f"{article['title']}\n"
            f"{article['link']}\n\n"
        )

    send_line(message)
