import requests
from database import get_db_connection
from config import NEWS_API_KEY, BASE_URL, CATEGORIES

def fetch_news():
    params = {
        "q": "energy storage OR batteries OR renewable energy",
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

def store_news():
    articles = fetch_news()
    conn = get_db_connection()
    cursor = conn.cursor()

    for article in articles:
        cursor.execute("""
            INSERT INTO news (title, link, category, date)
            VALUES (?, ?, ?, ?)""",
            (article["title"], article["url"], categorize_news(article["title"]), article["publishedAt"].split("T")[0])
        )
    
    conn.commit()
    conn.close()
