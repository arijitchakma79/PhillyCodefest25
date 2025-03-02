from flask import Blueprint, request, jsonify
from app.services import analyze_idea, analyze_google_trends, analyze_competitors  

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

@business_routes.route("/trends/analyze", methods=["POST"])
def analyze_trends():
    """API endpoint to analyze market trends"""
    try:
        trends_data = request.get_json()
        if not trends_data:
            return jsonify({"error": "Invalid JSON input"}), 400

        insights = analyze_google_trends(trends_data)  
        return jsonify({"insights": insights}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@business_routes.route("/competitors/analyze", methods=["POST"])
def analyze_market_competitors():
    """API endpoint to analyze market competitors"""
    try:
        business_data = request.get_json()
        if not business_data:
            return jsonify({"error": "Invalid JSON input"}), 400

        competitor_analysis = analyze_competitors(business_data)
        return jsonify(competitor_analysis), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500