import logging
from Agents.BusinessAnalystAgent.businessAnalystAgent import BusinessIdeaAnalyzer
from app.config import Config

openai_key = Config.OPENAI_API_KEY


logger = logging.getLogger(__name__)

analyzer = BusinessIdeaAnalyzer(openai_api_key=openai_key)

def analyze_idea(request_data):
    """Processes business idea using the BusinessIdeaAnalyzer"""
    logger.info(f"Analyzing business idea: {request_data.get('businessIdea', {}).get('shortName', 'Unnamed')}")
    return analyzer.analyze_business_idea(request_data)
