import os

# Database Configuration
DB_NAME = os.getenv("DB_NAME", "database.db")

# News API Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "701ccf219640483db2e95e3d0cf08c31")  # Use env variable or fallback key
BASE_URL = "https://newsapi.org/v2/everything"

# News Categories
CATEGORIES = {
    "USA": ["United States", "U.S."],
    "Europe": ["Europe", "Spain", "Poland", "Italy", "European Union"],
    "LATAM": ["Mexico", "Chile", "Brazil"],
    "Central America": ["Guatemala", "Costa Rica", "Panama", "El Salvador", "Honduras", "Nicaragua", "Belize"]
}
