from flask import Blueprint, jsonify
from services.newsletter_service import get_newsletter

newsletter_routes = Blueprint("newsletter_routes", __name__)

@newsletter_routes.route("/generate-newsletter", methods=["GET"])
def generate_newsletter():
    return jsonify({"newsletter": get_newsletter()})
