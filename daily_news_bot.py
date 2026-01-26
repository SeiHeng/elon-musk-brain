import feedparser
import json
from datetime import datetime
import os

KEYWORDS = [
    # --- 1. 科技巨頭 (Magnificent 7) - 市場的領頭羊 ---
    "NVIDIA stock NVDA",
    "Microsoft stock MSFT",
    "Google Alphabet stock GOOGL",
    "Apple stock AAPL",
    "Amazon stock AMZN",
    "Meta Platforms stock META",
    "Tesla stock TSLA",

    # --- 2. AI 與 算力 (Elon 認為未來的貨幣) ---
    "AMD stock AI chip",
    "TSMC stock TSM",       # 台積電 (晶片製造核心)
    "Palantir stock PLTR",  # 矽谷最像馬斯克風格的軟體公司
    "Super Micro Computer stock SMCI",
    "OpenAI Microsoft news", # 雖然 OpenAI 沒上市，但會影響微軟

    # --- 3. 加密貨幣與金融科技 (去中心化) ---
    "Bitcoin price crypto",
    "Ethereum price crypto",
    "Dogecoin price",       # 馬斯克的寵物
    "Coinbase stock COIN",
    "Block Square stock SQ",

    # --- 4. 傳統車廠 (Legacy Auto) - 馬斯克眼中的「諾基亞」 (潛在做空對象) ---
    "Ford Motor stock F",
    "General Motors stock GM",
    "Toyota Motor stock TM",
    "Rivian stock RIVN",    # 競爭對手 (觀察是否破產)
    "Lucid Group stock LCID",

    # --- 5. 太空與防衛 (SpaceX 相關領域) ---
    "Boeing stock BA",      # 波音 (馬斯克常批評他們的工程失敗)
    "Lockheed Martin stock LMT",

    # --- 6. 宏觀經濟 (影響大盤的水位) ---
    "Federal Reserve interest rate decision", # 聯準會利率
    "US CPI inflation data",                  # 通膨數據
    "US GDP growth report"
]

def fetch_google_news():
    print(f"[{datetime.now()}] 開始執行新聞抓取 (強制 24 小時內)...")
    all_news = []

    for topic in KEYWORDS:
        encoded_topic = topic.replace(" ", "+")
        
        # ⬇️ 修改重點在這裡：加上 when:1d
        rss_url = f"https://news.google.com/rss/search?q={encoded_topic}+when:1d&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(rss_url)
        
        # 如果這主題完全沒新新聞，feed.entries 可能是空的
        if not feed.entries:
            print(f"⚠️ 主題 '{topic}' 在過去 24 小時內沒有新聞。")
            continue

        for entry in feed.entries[:3]: # 只抓前 3 則最新的
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

    # 存檔
    filename = f"data/news_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
        
    print(f"成功儲存: {filename} (包含 {len(all_news)} 則新聞)")