import logging
from Agents.BusinessAnalystAgent.businessAnalystAgent import BusinessIdeaAnalyzer
from Agents.MarketTrendAgent.googleTrendsAnalyzer import GoogleTrendsAnalyzer
from Agents.CompetitorAgent.competitorAgent import CompetitorAgentResearch
from app.config import Config

openai_key = Config.OPENAI_API_KEY
serp_key = Config.SERP_API_KEY
perplexity_key = Config.PERPLEXITY_API_KEY

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

def analyze_competitors(business_data):
    """Analyze market competitors for a business idea"""
    logger.info(f"Analyzing competitors for: {business_data.get('originalRequest', {}).get('businessIdea', {}).get('shortName', 'Unnamed')}")
    
    try:
        # Initialize the CompetitorAgentResearch with the necessary keys and business data
        competitor_agent = CompetitorAgentResearch(
            api_key=openai_key,
            perplexity_api=perplexity_key,
            business_data=business_data
        )
        
        # Get competitor analysis
        competitor_analysis = competitor_agent.get_competitor_analysis()
        return competitor_analysis
        
    except Exception as e:
        logger.error(f"Error in competitor analysis: {str(e)}")
        return {"status": "error", "message": str(e), "competitors": {}}