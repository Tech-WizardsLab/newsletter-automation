from database import get_db_connection  # FIX: Import database connection
from datetime import datetime

def get_newsletter():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, link, category FROM news WHERE approved = 1")
    news_list = cursor.fetchall()
    conn.close()
    
    categorized_news = {"USA": [], "Europe": [], "LATAM": [], "Central America": [], "Global": []}
    for news in news_list:
        categorized_news.setdefault(news["category"], []).append(f"- [{news['title']}]({news['link']})")

    newsletter = f"""
🔋✨ {get_month()} is here! Welcome to NewStorage 🚀

Stay updated with the latest energy storage news!

"""
    for category, articles in categorized_news.items():
        if articles:
            newsletter += f"🌎🔋⚡ **{category.upper()} NEWS**\n" + "\n".join(articles) + "\n\n"

    newsletter += """
🖥️ **Upcoming Webinars & Events**
- [Webinar 1](#)
- [Event 1](#)

That’s all for this month! See you next issue.
"""
    return newsletter

def get_month():
    return datetime.now().strftime("%B")
