import logging
import threading
import time
import concurrent.futures
from typing import Dict, Any, List

from Agents.BusinessAnalystAgent.businessAnalystAgent import BusinessIdeaAnalyzer
from Agents.MarketTrendAgent.googleTrendsAnalyzer import GoogleTrendsAnalyzer
from Agents.CompetitorAgent.competitorAgent import CompetitorAgentResearch
from Agents.SwotAnalysisAgent.swotAnalysisAgent import SWOTAnalysisAgent
from app.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BusinessAnalysisPipeline:
    def __init__(self):
        """Initialize the pipeline with all required agents"""
        self.openai_key = Config.OPENAI_API_KEY
        self.serp_key = Config.SERP_API_KEY
        self.perplexity_key = Config.PERPLEXITY_API_KEY
        
        # Initialize the agents
        self.business_analyzer = BusinessIdeaAnalyzer(openai_api_key=self.openai_key)
        self.trends_analyzer = GoogleTrendsAnalyzer(serpapi_key=self.serp_key, openai_key=self.openai_key)
        
        # CompetitorAgentResearch and SWOTAnalysisAgent are initialized with business data, so we create them later
        
    def _run_business_analysis(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the business analysis using BusinessIdeaAnalyzer"""
        logger.info(f"Starting business analysis for: {request_data.get('businessIdea', {}).get('shortName', 'Unnamed')}")
        return self.business_analyzer.analyze_business_idea(request_data)
    
    def _run_trends_analysis(self, business_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run the trends analysis using GoogleTrendsAnalyzer"""
        logger.info(f"Starting trends analysis for: {business_analysis.get('originalRequest', {}).get('businessIdea', {}).get('shortName', 'Unnamed')}")
        try:
            return self.trends_analyzer.analyze_market_trends(business_analysis)
        except Exception as e:
            logger.error(f"Error in trends analysis: {str(e)}")
            return {"error": str(e)}
    
    def _run_competitor_analysis(self, business_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run the competitor analysis using CompetitorAgentResearch"""
        logger.info(f"Starting competitor analysis for: {business_analysis.get('originalRequest', {}).get('businessIdea', {}).get('shortName', 'Unnamed')}")
        try:
            competitor_agent = CompetitorAgentResearch(
                api_key=self.openai_key,
                perplexity_api=self.perplexity_key,
                business_data=business_analysis
            )
            return competitor_agent.get_competitor_analysis()
        except Exception as e:
            logger.error(f"Error in competitor analysis: {str(e)}")
            return {"status": "error", "message": str(e), "competitors": {}}
    
    def _run_swot_analysis(self, business_analysis: Dict[str, Any], competitor_analysis: Dict[str, Any], trends_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Run the SWOT analysis using SWOTAnalysisAgent with trends data"""
        logger.info(f"Starting SWOT analysis for: {business_analysis.get('originalRequest', {}).get('businessIdea', {}).get('shortName', 'Unnamed')}")
        try:
            swot_agent = SWOTAnalysisAgent(
                api_key=self.openai_key,
                business_data=business_analysis,
                competitor_data=competitor_analysis,
                trends_data=trends_analysis
            )
            return swot_agent.generate_swot_analysis()
        except Exception as e:
            logger.error(f"Error in SWOT analysis: {str(e)}")
            return {"status": "error", "message": str(e), "swot_analysis": {}}
    
    def run_pipeline(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the complete business analysis pipeline with parallel processing
        
        Args:
            request_data (Dict[str, Any]): The initial business idea request
            
        Returns:
            Dict[str, Any]: Comprehensive analysis including business, trends, competitor, and SWOT data
        """
        start_time = time.time()
        
        # Step 1: Run the business analysis (this must be done first)
        business_analysis = self._run_business_analysis(request_data)
        
        # Track individual analysis results
        results = {
            "businessAnalysis": business_analysis
        }
        
        # Step 2: Run trends and competitor analysis in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit the analysis tasks
            trends_future = executor.submit(self._run_trends_analysis, business_analysis)
            competitor_future = executor.submit(self._run_competitor_analysis, business_analysis)
            
            # Get the results
            trends_analysis = trends_future.result()
            competitor_analysis = competitor_future.result()
            
            # Add results to the output
            results["trendsAnalysis"] = trends_analysis
            results["competitorAnalysis"] = competitor_analysis
        
        # Step 3: Run SWOT analysis using competitor and trends analysis results
        swot_analysis = self._run_swot_analysis(business_analysis, competitor_analysis, trends_analysis)
        results["swotAnalysis"] = swot_analysis
        
        # Calculate execution time
        execution_time = time.time() - start_time
        logger.info(f"Total pipeline execution time: {execution_time:.2f} seconds")
        
        # Add metadata to the results
        results["metadata"] = {
            "executionTime": f"{execution_time:.2f} seconds",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "businessName": business_analysis.get("originalRequest", {}).get("businessIdea", {}).get("shortName", "Unnamed")
        }
        
        return results

# Modified service functions to use the pipeline
def analyze_business_pipeline(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full business analysis pipeline that distributes data to all agents
    and returns a comprehensive analysis
    
    Args:
        request_data (Dict[str, Any]): The initial business idea request
        
    Returns:
        Dict[str, Any]: Comprehensive analysis from all agents
    """
    pipeline = BusinessAnalysisPipeline()
    return pipeline.run_pipeline(request_data)

# Add standalone SWOT analysis function for individual use
def analyze_swot(business_data: Dict[str, Any], competitor_data: Dict[str, Any], trends_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze business, competitor, and trends data to generate a SWOT analysis
    
    Args:
        business_data (Dict[str, Any]): Business analysis data
        competitor_data (Dict[str, Any]): Competitor analysis data
        trends_data (Dict[str, Any], optional): Market trends analysis data
        
    Returns:
        Dict[str, Any]: SWOT analysis results with strengths, weaknesses, opportunities, and threats
    """
    from app.config import Config
    
    try:
        swot_agent = SWOTAnalysisAgent(
            api_key=Config.OPENAI_API_KEY,
            business_data=business_data,
            competitor_data=competitor_data,
            trends_data=trends_data
        )
        
        return swot_agent.generate_swot_analysis()
    except Exception as e:
        logger.error(f"Error in SWOT analysis: {str(e)}")
        return {"status": "error", "message": str(e), "swot_analysis": {}}

# Backwards compatibility functions for existing routes
def analyze_idea(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for business idea analysis only"""
    analyzer = BusinessIdeaAnalyzer(openai_api_key=Config.OPENAI_API_KEY)
    return analyzer.analyze_business_idea(request_data)

def analyze_google_trends(trends_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for trends analysis only"""
    trends_analyzer = GoogleTrendsAnalyzer(serpapi_key=Config.SERP_API_KEY, openai_key=Config.OPENAI_API_KEY)
    return trends_analyzer.analyze_market_trends(trends_data)

def analyze_competitors(business_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for competitor analysis only"""
    try:
        competitor_agent = CompetitorAgentResearch(
            api_key=Config.OPENAI_API_KEY,
            perplexity_api=Config.PERPLEXITY_API_KEY,
            business_data=business_data
        )
        return competitor_agent.get_competitor_analysis()
    except Exception as e:
        logger.error(f"Error in competitor analysis: {str(e)}")
        return {"status": "error", "message": str(e), "competitors": {}}