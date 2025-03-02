import os
import json
import logging
import pycountry
from typing import Dict, Any, Optional, List
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BusinessIdeaAnalyzer:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = OpenAI(api_key=self.openai_api_key)
        logger.info("BusinessIdeaAnalyzer initialized successfully")
    
    def analyze_business_idea(self, request: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Analyzing business idea: {request.get('businessIdea', {}).get('shortName', 'Unnamed')}")
        industry_analysis = self.perform_llm_analysis(request)
        
        # Convert country names to ISO codes
        if "potentialGeographicMarkets" in industry_analysis:
            industry_analysis["potentialGeographicMarkets"] = self.convert_to_country_codes(
                industry_analysis["potentialGeographicMarkets"]
            )
        
        return {
            "originalRequest": request,
            "industryAnalysis": industry_analysis
        }
    
    def convert_to_country_codes(self, country_names: List[str]) -> List[str]:
        """Convert country names to their ISO 3166-1 alpha-2 codes."""
        country_codes = []
        for country_name in country_names:
            try:
                # Try to find the country by name
                country = pycountry.countries.search_fuzzy(country_name)
                if country and country[0].alpha_2:
                    country_codes.append(country[0].alpha_2)
                else:
                    # If no match found, keep the original name
                    country_codes.append(country_name)
            except LookupError:
                # If lookup fails, keep the original name
                country_codes.append(country_name)
        return country_codes
    
    def perform_llm_analysis(self, request: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self.construct_analysis_prompt(request)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are an expert in industry classification. Analyze the business idea and return structured industry analysis as JSON."""},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)
    
    def construct_analysis_prompt(self, request: Dict[str, Any]) -> str:
        idea_description = request.get("businessIdea", {}).get("description", "")
        short_name = request.get("businessIdea", {}).get("shortName", "")
        industry = request.get("basicContext", {}).get("industry", "")
        geographic_interest = request.get("geographicInterest", [])
        
        return f"""
        Classify the business idea into industries and identify relevant geographic markets.
        
        BUSINESS IDEA:
        - Description: {idea_description}
        - Name: {short_name if short_name else 'Not provided'}
        - Industry: {industry if industry else 'Not explicitly stated'}
        - Target Markets: {', '.join(geographic_interest) if geographic_interest else 'Not explicitly stated'}
        
        Return JSON with this format:
        
        {json.dumps(self._get_response_schema(), indent=2)}
        """
    
    def _get_response_schema(self) -> Dict[str, Any]:
        return {
            "primaryIndustry": "string",
            "subIndustries": ["string"],
            "keywords": ["string"],
            "relatedIndustries": ["string"],
            "potentialGeographicMarkets": ["string"]
        }