from flask import Blueprint, request, jsonify
from app.services import (
    analyze_idea, 
    analyze_google_trends, 
    analyze_competitors, 
    analyze_business_pipeline,
    analyze_swot
)

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
        return jsonify(insights), 200

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

@business_routes.route("/swot/analyze", methods=["POST"])
def analyze_business_swot():
    """
    API endpoint to create a SWOT analysis based on business and competitor data
    
    Expected JSON input format:
    {
        "businessData": {business analysis output},
        "competitorData": {competitor analysis output}
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON input"}), 400
        
        if "businessData" not in data or "competitorData" not in data:
            return jsonify({"error": "Missing required fields: businessData and competitorData"}), 400
            
        swot_analysis = analyze_swot(data["businessData"], data["competitorData"])
        return jsonify(swot_analysis), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@business_routes.route("/pipeline/analyze", methods=["POST"])
def run_full_analysis_pipeline():
    """
    API endpoint to run the complete business analysis pipeline
    This runs all agents in parallel and provides a comprehensive analysis
    """
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Invalid JSON input"}), 400

        # Run the full pipeline with parallel processing
        pipeline_results = analyze_business_pipeline(request_data)
        return jsonify(pipeline_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500