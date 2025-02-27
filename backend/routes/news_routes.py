from flask import Blueprint, jsonify, request
from services.news_service import store_news
from database import get_db_connection

news_routes = Blueprint("news_routes", __name__)

@news_routes.route("/fetch-news", methods=["GET"])
def fetch_and_store_news():
    store_news()
    return jsonify({"message": "News fetched and stored successfully!"})

@news_routes.route("/news", methods=["GET"])
def get_news():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news")
    news_list = cursor.fetchall()
    conn.close()
    return jsonify({"news": [dict(row) for row in news_list]})

@news_routes.route("/news/<int:id>/approve", methods=["PUT"])
def approve_news(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET approved = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "News approved successfully!", "id": id})
