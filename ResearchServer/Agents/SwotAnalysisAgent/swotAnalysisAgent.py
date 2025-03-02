import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SWOTAnalysisAgent:
    def __init__(self, api_key: str, business_data: Dict[str, Any], competitor_data: Dict[str, Any], trends_data: Optional[Dict[str, Any]] = None):
        """
        Initialize the SWOT Analysis Agent with API key and analysis data.
        
        Args:
            api_key (str): OpenAI API key for GPT model access
            business_data (Dict[str, Any]): Dictionary containing business analysis
            competitor_data (Dict[str, Any]): Dictionary containing competitor analysis
            trends_data (Optional[Dict[str, Any]]): Dictionary containing market trends analysis
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.business_data = business_data
        self.competitor_data = competitor_data
        self.trends_data = trends_data or {}
        
        # Extract key business information for easier access
        self.industry_analysis = business_data.get("industryAnalysis", {})
        self.original_request = business_data.get("originalRequest", {})
        self.competitors = competitor_data.get("data", {}).get("competitors", {})
        
    def _extract_business_details(self) -> Dict[str, Any]:
        """Extract key business details from input data"""
        business_idea = self.original_request.get("businessIdea", {})
        basic_context = self.original_request.get("basicContext", {})
        additional_context = self.original_request.get("additionalContext", "")
        
        # Extract business unique value propositions from the description and context
        unique_value_props = []
        
        # Look for specific differentiators in the additional context
        if "lower transaction fees" in additional_context.lower():
            unique_value_props.append("Lower transaction fees than competitors")
        
        if "actionable business insights" in additional_context.lower() or "analytics" in additional_context.lower():
            unique_value_props.append("Advanced analytics and business insights")
            
        # Extract from the business description
        description = business_idea.get("description", "")
        if "analytics" in description.lower():
            if "Advanced analytics and business insights" not in unique_value_props:
                unique_value_props.append("Integrated analytics capabilities")
                
        # Add any other specific features mentioned
        for feature in ["AI", "machine learning", "blockchain", "subscription", "real-time", "cloud-based"]:
            if feature.lower() in description.lower() or feature.lower() in additional_context.lower():
                unique_value_props.append(f"{feature.title()} technology integration")
        
        return {
            "name": business_idea.get("shortName", ""),
            "description": description,
            "industry": self.industry_analysis.get("primaryIndustry", ""),
            "sub_industries": self.industry_analysis.get("subIndustries", []),
            "target_markets": self.industry_analysis.get("potentialGeographicMarkets", []),
            "target_customers": basic_context.get("targetCustomers", ""),
            "business_type": basic_context.get("businessType", ""),
            "additional_context": additional_context,
            "unique_value_propositions": unique_value_props
        }
        
    def _extract_competitor_insights(self) -> Dict[str, Any]:
        """Extract detailed competitor insights for strategic analysis"""
        
        # Collect all strengths and weaknesses by competitor
        competitor_strengths = {}
        competitor_weaknesses = {}
        market_presence = []
        business_models = []
        pricing_models = []
        
        # Track common strength and weakness patterns
        common_strengths = {}
        common_weaknesses = {}
        
        # Analyze each competitor
        for name, details in self.competitors.items():
            # Record strengths by competitor
            strengths = details.get("strengths", [])
            competitor_strengths[name] = strengths
            
            # Count frequency of each type of strength
            for strength in strengths:
                # Normalize the strength text for better matching
                normalized = strength.lower()
                if normalized not in common_strengths:
                    common_strengths[normalized] = {"count": 0, "examples": []}
                common_strengths[normalized]["count"] += 1
                common_strengths[normalized]["examples"].append(f"{name}: {strength}")
            
            # Record weaknesses by competitor
            weaknesses = details.get("weaknesses", [])
            competitor_weaknesses[name] = weaknesses
            
            # Count frequency of each type of weakness
            for weakness in weaknesses:
                # Normalize the weakness text for better matching
                normalized = weakness.lower()
                if normalized not in common_weaknesses:
                    common_weaknesses[normalized] = {"count": 0, "examples": []}
                common_weaknesses[normalized]["count"] += 1
                common_weaknesses[normalized]["examples"].append(f"{name}: {weakness}")
            
            # Extract geography information
            geography = details.get("geography", "")
            if geography:
                market_presence.append(f"{name}: {geography}")
            
            # Extract business description for potential business models
            description = details.get("description", "")
            if description:
                business_models.append(f"{name}: {description}")
                
                # Look for pricing information in the description
                if "pricing" in description.lower() or "fee" in description.lower() or "cost" in description.lower():
                    pricing_models.append(f"{name}: {description}")
        
        # Sort common strengths and weaknesses by frequency
        sorted_strengths = sorted(common_strengths.items(), key=lambda x: x[1]["count"], reverse=True)
        sorted_weaknesses = sorted(common_weaknesses.items(), key=lambda x: x[1]["count"], reverse=True)
        
        # Extract the most common patterns
        top_strengths = [{"pattern": k, "count": v["count"], "examples": v["examples"][:3]} 
                        for k, v in sorted_strengths[:5]]
        top_weaknesses = [{"pattern": k, "count": v["count"], "examples": v["examples"][:3]} 
                         for k, v in sorted_weaknesses[:5]]
        
        return {
            "competitor_strengths": competitor_strengths,
            "competitor_weaknesses": competitor_weaknesses,
            "common_strength_patterns": top_strengths,
            "common_weakness_patterns": top_weaknesses,
            "market_presence": market_presence,
            "business_models": business_models,
            "pricing_models": pricing_models,
            "competitor_count": len(self.competitors)
        }
    
    def _extract_market_trends(self) -> Dict[str, Any]:
        """Extract market trend insights from trends data"""
        if not self.trends_data:
            return {"available": False}
            
        trends_insights = {}
        
        # Extract AI analysis from trends data
        ai_analysis = self.trends_data.get("insights", {}).get("ai_analysis", "")
        if ai_analysis:
            trends_insights["ai_analysis"] = ai_analysis
            
        # Extract any specific trend patterns 
        detailed_trends = self.trends_data.get("insights", {}).get("detailed_trends", {})
        trends_by_region = {}
        forecasts = {}
        
        for keyword, regions in detailed_trends.items():
            for region, data in regions.items():
                if "forecast" in data:
                    if region not in forecasts:
                        forecasts[region] = {}
                    forecasts[region][keyword] = data["forecast"]
                
                if "monthly_data" in data:
                    if region not in trends_by_region:
                        trends_by_region[region] = {}
                    trends_by_region[region][keyword] = data["monthly_data"]
        
        trends_insights["forecasts"] = forecasts
        trends_insights["historical_trends"] = trends_by_region
        trends_insights["available"] = bool(ai_analysis or forecasts or trends_by_region)
        
        return trends_insights
    
    def _generate_swot_prompt(self, business_details: Dict[str, Any], 
                             competitor_insights: Dict[str, Any],
                             market_trends: Dict[str, Any]) -> str:
        """Generate prompt for SWOT analysis based on business, competitor and trend data"""
        
        # Format competitor strengths and weaknesses information
        competitor_strengths_str = ""
        for competitor, strengths in competitor_insights["competitor_strengths"].items():
            competitor_strengths_str += f"{competitor} Strengths:\n"
            for strength in strengths:
                competitor_strengths_str += f"- {strength}\n"
            competitor_strengths_str += "\n"
            
        competitor_weaknesses_str = ""
        for competitor, weaknesses in competitor_insights["competitor_weaknesses"].items():
            competitor_weaknesses_str += f"{competitor} Weaknesses:\n"
            for weakness in weaknesses:
                competitor_weaknesses_str += f"- {weakness}\n"
            competitor_weaknesses_str += "\n"
            
        # Format common patterns
        common_strength_patterns = "Common competitor strengths:\n"
        for strength in competitor_insights["common_strength_patterns"]:
            common_strength_patterns += f"- Pattern: {strength['pattern']} (found in {strength['count']} competitors)\n"
            common_strength_patterns += f"  Examples: {'; '.join(strength['examples'])}\n\n"
            
        common_weakness_patterns = "Common competitor weaknesses:\n"
        for weakness in competitor_insights["common_weakness_patterns"]:
            common_weakness_patterns += f"- Pattern: {weakness['pattern']} (found in {weakness['count']} competitors)\n"
            common_weakness_patterns += f"  Examples: {'; '.join(weakness['examples'])}\n\n"
        
        # Add market trends if available
        trends_section = ""
        if market_trends["available"]:
            trends_section = "MARKET TRENDS INSIGHTS:\n"
            
            if "ai_analysis" in market_trends:
                trends_section += f"AI Market Analysis:\n{market_trends['ai_analysis']}\n\n"
                
            if "forecasts" in market_trends and market_trends["forecasts"]:
                trends_section += "Market Forecasts:\n"
                for region, keywords in market_trends["forecasts"].items():
                    trends_section += f"Region: {region}\n"
                    for keyword, forecast in keywords.items():
                        trends_section += f"- {keyword}: Growth trend over next 6 months: "
                        try:
                            first_val = forecast[0]["predicted_value"]
                            last_val = forecast[-1]["predicted_value"]
                            percent_change = ((last_val - first_val) / first_val) * 100
                            trends_section += f"{percent_change:.1f}% change\n"
                        except (IndexError, KeyError, ZeroDivisionError):
                            trends_section += "Data incomplete\n"
        
        # Assemble the prompt
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
- Potential unique value propositions: {', '.join(business_details['unique_value_propositions'])}

COMPETITOR INSIGHTS:
The business would be competing against {competitor_insights['competitor_count']} established competitors with the following characteristics:

{competitor_strengths_str}

{competitor_weaknesses_str}

{common_strength_patterns}

{common_weakness_patterns}

Geographic presence of competitors:
{json.dumps(competitor_insights['market_presence'], indent=2)}

Competitor business models and positioning:
{json.dumps(competitor_insights['business_models'], indent=2)}

{trends_section}

Based on this information, provide a detailed SWOT analysis with the following structure:

1. STRENGTHS: Internal factors that give the business an advantage over competitors.
   - Focus on how the business can capitalize on competitor weaknesses
   - Highlight any unique value propositions that address gaps in the market
   - Identify resources or capabilities that competitors don't have

2. WEAKNESSES: Internal factors that place the business at a disadvantage.
   - Identify areas where competitors have established strengths that may be hard to overcome
   - Consider potential resource, experience, or technology gaps compared to competitors
   - Highlight challenges in differentiation or market penetration

3. OPPORTUNITIES: External factors that the business could exploit to its advantage.
   - Look for patterns in competitor weaknesses that reveal market gaps
   - Identify trends showing growth potential or emerging customer needs
   - Consider geographic or demographic segments underserved by competitors
   - Suggest specific strategies to capitalize on market trends and competitor limitations

4. THREATS: External factors that could cause trouble for the business.
   - Analyze how competitors might respond to a new market entrant
   - Identify market saturation, pricing pressures, or regulatory challenges
   - Consider technological developments that might impact the business model
   - Highlight potential barriers to entry created by established competitors

For each category, provide at least 5-7 specific points with brief explanations of why they matter and how they relate to the competitor landscape. Focus on actionable insights that can guide business strategy.
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
            
            # Extract market trends
            market_trends = self._extract_market_trends()
            
            # Generate prompt for SWOT analysis
            prompt = self._generate_swot_prompt(business_details, competitor_insights, market_trends)
            
            # Generate SWOT analysis using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategy expert specializing in SWOT analysis. Your expertise is in analyzing competitor data to identify strategic advantages, weaknesses, opportunities and threats. Provide balanced, insightful, and actionable SWOT analyses with specific references to how the business compares to competitors and how it can capitalize on market trends."},
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
                    "competitors_analyzed": competitor_insights["competitor_count"],
                    "trends_data_used": market_trends["available"]
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
            structure_prompt = f"""
            Convert the following SWOT analysis into a structured JSON object. 
            
            The JSON should have four main categories:
            1. "strengths" - internal advantages
            2. "weaknesses" - internal disadvantages
            3. "opportunities" - external factors that could be exploited
            4. "threats" - external factors that could cause problems
            
            For each category, create an array of objects where each object has:
            - "title": A short, descriptive title for the point (1-5 words)
            - "description": A detailed explanation of the point
            - "competitorContext": How this relates to competitors (if mentioned)
            - "actionItem": A suggested action based on this point (if applicable)
            
            Here's the SWOT analysis to structure:
            
            {swot_text}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a data structuring specialist. Your task is to convert text-based SWOT analyses into structured JSON format while preserving all key insights and strategic details."},
                    {"role": "user", "content": structure_prompt}
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

# Function to use in your services.py
def analyze_swot(business_data: Dict[str, Any], competitor_data: Dict[str, Any], trends_data: Optional[Dict[str, Any]] = None, openai_key: Optional[str] = None) -> Dict[str, Any]:
    """Analyze business and competitor data to generate a SWOT analysis"""
    from app.config import Config
    
    openai_key = openai_key or Config.OPENAI_API_KEY
    
    try:
        swot_agent = SWOTAnalysisAgent(
            api_key=openai_key,
            business_data=business_data,
            competitor_data=competitor_data,
            trends_data=trends_data
        )
        
        return swot_agent.generate_swot_analysis()
    except Exception as e:
        logger.error(f"Error in SWOT analysis: {str(e)}")
        return {"status": "error", "message": str(e), "swot_analysis": {}}