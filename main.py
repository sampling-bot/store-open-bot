from config import AREAS, KEYWORDS
from sources.google_news import get_google_news
from line_notify import send_line

articles = []

for _, area_list in AREAS.items():
    articles.extend(get_google_news(area_list, KEYWORDS))

if not articles:
    send_line("今日は新しい記事は見つかりませんでした。")
else:
    message = "【テスト】\n\n"

    for article in articles[:5]:
        message += f"📍{article['area']}\n"
        message += f"{article['title']}\n"
        message += f"{article['link']}\n\n"

    send_line(message)
