import logging
from Agents.BusinessAnalystAgent.businessAnalystAgent import BusinessIdeaAnalyzer
from Agents.MarketTrendAgent.googleTrendsAnalyzer import GoogleTrendsAnalyzer
from app.config import Config

openai_key = Config.OPENAI_API_KEY
serp_key = Config.SERP_API_KEY

# Setup logging
logger = logging.getLogger(__name__)

# Initialize agents
analyzer = BusinessIdeaAnalyzer(openai_api_key=openai_key)
trends_analyzer = GoogleTrendsAnalyzer(serpapi_key=serp_key, openai_key=openai_key)

def analyze_idea(request_data):
    """Analyze a business idea using the BusinessIdeaAnalyzer agent"""
    logger.info(f"Analyzing business idea: {request_data.get('businessIdea', {}).get('shortName', 'Unnamed')}")
    return analyzer.analyze_business_idea(request_data)

def analyze_google_trends(trends_data):
    """Fetch Google Trends data and analyze using OpenAI"""
    return trends_analyzer.analyze_market_trends(trends_data)  
