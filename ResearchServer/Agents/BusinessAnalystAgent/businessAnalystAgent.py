import os
import json
import logging
from typing import Dict, Any, Optional
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
        return {
            "originalRequest": request,
            "industryAnalysis": industry_analysis
            }

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
