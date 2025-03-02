import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SWOTAnalysisAgent:
    def __init__(self, api_key: str, business_data: Dict[str, Any], competitor_data: Dict[str, Any]):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.business_data = business_data
        self.competitor_data = competitor_data
        
        # Extract key business information for easier access
        self.industry_analysis = business_data.get("industryAnalysis", {})
        self.original_request = business_data.get("originalRequest", {})
        self.competitors = competitor_data.get("data", {}).get("competitors", {})

    def _extract_business_details(self) -> Dict[str, Any]:
        business_idea = self.original_request.get("businessIdea", {})
        basic_context = self.original_request.get("basicContext", {})
        
        return {
            "name": business_idea.get("shortName", ""),
            "description": business_idea.get("description", ""),
            "industry": self.industry_analysis.get("primaryIndustry", ""),
            "sub_industries": self.industry_analysis.get("subIndustries", []),
            "target_markets": self.industry_analysis.get("potentialGeographicMarkets", []),
            "target_customers": basic_context.get("targetCustomers", ""),
            "business_type": basic_context.get("businessType", ""),
            "additional_context": self.original_request.get("additionalContext", "")
        }
    
    def _extract_competitor_insights(self) -> Dict[str, Any]:
        """Extract key competitor insights"""
        
        strengths_list = []
        weaknesses_list = []
        market_presence = []
        business_models = []
        
        # Analyze each competitor
        for name, details in self.competitors.items():
            # Add key strengths to the list
            strengths_list.extend(details.get("strengths", []))
            
            # Add key weaknesses to the list
            weaknesses_list.extend(details.get("weaknesses", []))
            
            # Extract geography information
            geography = details.get("geography", "")
            if geography:
                market_presence.append(f"{name}: {geography}")
            
            # Extract business description for potential business models
            description = details.get("description", "")
            if description:
                business_models.append(f"{name}: {description}")
        
        # Remove duplicates and keep only unique insights
        strengths_list = list(set(strengths_list))
        weaknesses_list = list(set(weaknesses_list))
        
        return {
            "market_strengths": strengths_list,
            "market_weaknesses": weaknesses_list,
            "market_presence": market_presence,
            "business_models": business_models,
            "competitor_count": len(self.competitors)
        }
    
    def _generate_swot_prompt(self, business_details: Dict[str, Any], competitor_insights: Dict[str, Any]) -> str:
        """Generate prompt for SWOT analysis based on business and competitor data"""
        
        prompt = f"""Generate a comprehensive SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis for a business with the following details:

        BUSINESS INFORMATION:
        - Name: {business_details['name']}
        - Description: {business_details['description']}
        - Industry: {business_details['industry']}
        - Sub-industries: {', '.join(business_details['sub_industries'])}
        - Target markets: {', '.join(business_details['target_markets'])}
        - Target customers: {business_details['target_customers']}
        - Business type: {business_details['business_type']}
        - Additional context: {business_details['additional_context']}

        COMPETITOR INSIGHTS:
        The business would be competing against {competitor_insights['competitor_count']} established competitors with the following characteristics:

        Common strengths in the market:
        {json.dumps(competitor_insights['market_strengths'], indent=2)}

        Common weaknesses in the market:
        {json.dumps(competitor_insights['market_weaknesses'], indent=2)}

        Geographic presence of competitors:
        {json.dumps(competitor_insights['market_presence'], indent=2)}

        Competitor business models and positioning:
        {json.dumps(competitor_insights['business_models'], indent=2)}

        Based on this information, please provide a detailed SWOT analysis with the following structure:

        1. STRENGTHS: Internal factors that give the business an advantage over competitors
        2. WEAKNESSES: Internal factors that place the business at a disadvantage
        3. OPPORTUNITIES: External factors that the business could exploit to its advantage
        4. THREATS: External factors that could cause trouble for the business

        For each category, provide at least 5 specific points with brief explanations of why they matter.
        """
        return prompt
    
    def generate_swot_analysis(self) -> Dict[str, Any]:
        """
        Generate a complete SWOT analysis for the business
        
        Returns:
            Dict[str, Any]: SWOT analysis with strengths, weaknesses, opportunities, and threats
        """
        try:
            # Extract business details
            business_details = self._extract_business_details()
            
            # Extract competitor insights
            competitor_insights = self._extract_competitor_insights()
            
            # Generate prompt for SWOT analysis
            prompt = self._generate_swot_prompt(business_details, competitor_insights)
            
            # Generate SWOT analysis using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategy expert specializing in SWOT analysis. Provide balanced, insightful, and actionable SWOT analyses based on business and competitor data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            swot_text = response.choices[0].message.content
            
            # Now parse the SWOT text into a structured format
            structured_swot = self._structure_swot_analysis(swot_text)
            
            # Add metadata
            return {
                "status": "success",
                "swot_analysis": structured_swot,
                "metadata": {
                    "business_name": business_details["name"],
                    "industry": business_details["industry"],
                    "competitors_analyzed": competitor_insights["competitor_count"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating SWOT analysis: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "swot_analysis": {}
            }
    
    def _structure_swot_analysis(self, swot_text: str) -> Dict[str, Any]:
        """Parse SWOT text into a structured format"""
        try:
            # Use OpenAI to structure the SWOT analysis
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a data structuring assistant. Convert a SWOT analysis in text format into a structured JSON object with four main keys: 'strengths', 'weaknesses', 'opportunities', and 'threats'. Each key should contain an array of objects with 'title' and 'description' fields."},
                    {"role": "user", "content": f"Convert this SWOT analysis into structured JSON:\n\n{swot_text}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            structured_swot = json.loads(response.choices[0].message.content)
            return structured_swot
            
        except Exception as e:
            logger.error(f"Error structuring SWOT analysis: {str(e)}")
            # Fallback with basic structure if parsing fails
            return {
                "strengths": [{"title": "Error parsing strengths", "description": "Could not parse SWOT text"}],
                "weaknesses": [{"title": "Error parsing weaknesses", "description": "Could not parse SWOT text"}],
                "opportunities": [{"title": "Error parsing opportunities", "description": "Could not parse SWOT text"}],
                "threats": [{"title": "Error parsing threats", "description": "Could not parse SWOT text"}]
            }