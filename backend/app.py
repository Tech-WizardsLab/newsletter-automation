from flask import Flask
from flask_cors import CORS
from routes.news_routes import news_routes
from routes.newsletter_routes import newsletter_routes
from database import init_db
from config import DB_NAME

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register Blueprints
app.register_blueprint(news_routes)
app.register_blueprint(newsletter_routes)

if __name__ == "__main__":
    init_db()
    print(f"🚀 Flask is running! Using database: {DB_NAME}")
    app.run(debug=True, host="0.0.0.0", port=5000)
