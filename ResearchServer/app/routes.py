from flask import Blueprint, request, jsonify
from app.services import analyze_idea

business_routes = Blueprint("business_routes", __name__)

@business_routes.route("/analyze", methods=["POST"])
def analyze_business():
    """API endpoint to analyze a business idea"""
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Invalid JSON input"}), 400

        result = analyze_idea(request_data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
