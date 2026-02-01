import feedparser
import json
from datetime import datetime
import os

KEYWORDS = [
    # --- 1. 科技巨頭 (Magnificent 7) ---
    "NVIDIA stock NVDA",
    "Microsoft stock MSFT",
    "Google Alphabet stock GOOGL",
    "Apple stock AAPL",
    "Amazon stock AMZN",
    "Meta Platforms stock META",
    "Tesla stock TSLA",

    # --- 2. AI 與 算力 ---
    "AMD stock AI chip",
    "TSMC stock TSM",
    "Palantir stock PLTR",
    "Super Micro Computer stock SMCI",
    "OpenAI Microsoft news",

    # --- 3. 加密貨幣與金融科技 ---
    "Bitcoin price crypto",
    "Ethereum price crypto",
    "Dogecoin price",
    "Coinbase stock COIN",
    "Block Square stock SQ",

    # --- 4. 傳統車廠 ---
    "Ford Motor stock F",
    "General Motors stock GM",
    "Toyota Motor stock TM",
    "Rivian stock RIVN",
    "Lucid Group stock LCID",

    # --- 5. 太空與防衛 ---
    "Boeing stock BA",
    "Lockheed Martin stock LMT",

    # --- 6. 宏觀經濟 ---
    "Federal Reserve interest rate decision",
    "US CPI inflation data",
    "US GDP growth report"
]

def fetch_google_news():
    now = datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 啟動爬蟲任務...")
    print(f"注意：GitHub Actions 伺服器目前時間為 UTC {now.hour}點")
    
    all_news = []

    for topic in KEYWORDS:
        encoded_topic = topic.replace(" ", "+")
        # 加上 when:1d 抓取 24 小時內新聞
        rss_url = f"https://news.google.com/rss/search?q={encoded_topic}+when:1d&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            print(f"⚠️  '{topic}' 過去 24 小時無新內容。")
            continue

        for entry in feed.entries[:3]: # 每個主題抓 3 則
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

    # --- 核心優化：建立包含元數據的存檔內容 ---
    output_data = {
        "last_updated": now.strftime('%Y-%m-%d %H:%M:%S'), # 強制改變內容
        "timezone": "UTC",
        "total_count": len(all_news),
        "news_list": all_news
    }

    # 檔名加入日期和小時，防止 Git 因為內容重疊而不提交
    filename = f"data/news_{now.strftime('%Y-%m-%d_%H')}h.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 成功儲存: {filename} (共 {len(all_news)} 則新聞)")

if __name__ == "__main__":
    fetch_google_news()