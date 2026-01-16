import feedparser
import json
from datetime import datetime
import os

KEYWORDS = [
    "Tesla stock",
    "SpaceX launch",
    "Artificial Intelligence regulation",
    "Federal Reserve interest rates",
    "Global economy recession",
    "Elon Musk"
]

def fetch_google_news():
    print(f"[{datetime.now()}] 開始執行新聞抓取...")
    all_news = []

    for topic in KEYWORDS:
        encoded_topic = topic.replace(" ", "+")
        rss_url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:5]:
            news_item = {
                "topic": topic,
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            }
            all_news.append(news_item)
            
    # 確保 data 資料夾存在
    if not os.path.exists('data'):
        os.makedirs('data')

    # 存檔 (存到 data 資料夾內)
    filename = f"data/news_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
        
    print(f"成功儲存: {filename}")

if __name__ == "__main__":
    fetch_google_news()