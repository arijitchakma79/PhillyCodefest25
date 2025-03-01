import os
import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BusinessIdeaAnalyzer:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required.")

        # Create OpenAI client
        self.client = OpenAI(api_key=self.openai_api_key)

        logger.info("BusinessIdeaAnalyzer initialized successfully")

    def analyze_business_idea(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis method to process a business idea request.
        
        Args:
            request: The incoming business idea request JSON
            
        Returns:
            Enhanced request with additional analysis
        """
        logger.info(f"Analyzing business idea: {request.get('businessIdea', {}).get('shortName', 'Unnamed')}")
        
        # Create a deep copy of the request to avoid modifying the original
        enhanced_request = json.loads(json.dumps(request))
        
        # Perform comprehensive analysis using LLM
        analysis_results = self.perform_llm_analysis(request)

        enhanced_request["enhancedContext"] = {
            "industryAnalysis": analysis_results["industryAnalysis"],
            "businessModelAnalysis": analysis_results["businessModelAnalysis"],
            "competitiveParameters": analysis_results["competitiveParameters"],
            "marketParameters": analysis_results["marketParameters"],
            "technicalRequirements": analysis_results["technicalRequirements"],
            "regulatoryConsiderations": analysis_results["regulatoryConsiderations"],
            "swotAnalysis": analysis_results["swotAnalysis"]
        }
        
        enhanced_request["agentRouting"] = analysis_results["agentRouting"]
        
        enhanced_request["confidenceScores"] = analysis_results["confidenceScores"]
        
        enhanced_request["dataGaps"] = analysis_results.get("dataGaps", [])
        
        logger.info("Business idea analysis completed successfully")
        
        return enhanced_request
    
    def perform_llm_analysis(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use OpenAI to analyze the business idea comprehensively.
        
        Args:
            request: The business idea request data
            
        Returns:
            Structured analysis from the LLM
        """
        # Construct a comprehensive prompt for the LLM
        prompt = self.construct_analysis_prompt(request)
        
        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert business analyst specializing in market research and business strategy. 
                    Your task is to analyze a business idea comprehensively and return a structured analysis in JSON format.
                    
                    Be creative and thorough in your analysis. You should:
                    1. Identify the most appropriate industry classification
                    2. Determine likely competitors and market dynamics
                    3. Assess the business model and revenue streams
                    4. Identify technical requirements and regulatory considerations
                    5. Conduct a preliminary SWOT analysis
                    
                    Be specific and detailed in your analysis, making reasonable inferences when information is limited.
                    Think beyond obvious categories and provide insightful observations that would be valuable to an entrepreneur.
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.3 
        )
        
        # Parse the response
        analysis_results = json.loads(response.choices[0].message.content)
        
        logger.info("LLM analysis successful")
        return analysis_results
    
    def construct_analysis_prompt(self, request: Dict[str, Any]) -> str:
        """
        Construct a detailed prompt for the LLM to analyze the business idea.
        
        Args:
            request: The business idea request
            
        Returns:
            A structured prompt for the LLM
        """
        idea_description = request.get("businessIdea", {}).get("description", "")
        short_name = request.get("businessIdea", {}).get("shortName", "")
        industry = request.get("basicContext", {}).get("industry", "")
        business_type = request.get("basicContext", {}).get("businessType", "")
        target_customers = request.get("basicContext", {}).get("targetCustomers", "")
        geographic_interest = request.get("geographicInterest", [])
        additional_context = request.get("additionalContext", "")
        
        return f"""
        Analyze the following business idea in detail and provide a structured analysis in JSON format.
        
        BUSINESS IDEA SUMMARY:
        - Description: {idea_description}
        - Name: {short_name if short_name else 'Not provided'}
        - Industry: {industry if industry else 'Not explicitly stated'}
        - Business Type: {business_type if business_type else 'Not explicitly stated'}
        - Target Customers: {target_customers if target_customers else 'Not explicitly stated'}
        - Geographic Interest: {', '.join(geographic_interest) if geographic_interest else 'Not explicitly stated'}
        - Additional Context: {additional_context if additional_context else 'None provided'}
        
        Please analyze and return a JSON object with the following structure:
        
        {json.dumps(self._get_response_schema(), indent=2)}
        
        Based on the provided business idea, conduct a comprehensive analysis. If some information is not provided, 
        make reasonable inferences based on the idea description. Be specific, insightful, and provide detailed 
        analysis for each section. Think like an experienced business strategist and industry analyst.
        """
    
    def _get_response_schema(self) -> Dict[str, Any]:
        """
        Returns the expected schema for LLM response.
        
        Returns:
            Dictionary representing the schema with example values
        """
        return {
            "industryAnalysis": {
                "primaryIndustry": "string",
                "subIndustries": ["string"],
                "keywords": ["string"],
                "relatedIndustries": ["string"]
            },
            "businessModelAnalysis": {
                "primaryModel": "string",
                "revenueStreams": ["string"],
                "b2bVsB2c": "string",
                "customerAcquisitionChannels": ["string"],
                "valueProposition": ["string"],
                "scalabilityAssessment": "string"
            },
            "competitiveParameters": {
                "likelyCompetitors": [
                    {
                        "name": "string",
                        "type": "direct|indirect",
                        "strengths": ["string"],
                        "weaknesses": ["string"]
                    }
                ],
                "competitiveDimensions": ["string"],
                "marketSaturation": "low|medium|high",
                "barrierToEntry": "low|medium|high"
            },
            "marketParameters": {
                "targetSegments": ["string"],
                "geographicScope": ["string"],
                "businessSize": "string",
                "industryFocus": ["string"],
                "customerNeeds": ["string"],
                "marketSize": {
                    "estimate": "number",
                    "unit": "string",
                    "growthRate": "number"
                },
                "adoptionChallenges": ["string"]
            },
            "technicalRequirements": {
                "platforms": ["string"],
                "integrationNeeds": ["string"],
                "techStack": ["string"],
                "developmentComplexity": "low|medium|high",
                "timeToMarket": "string"
            },
            "regulatoryConsiderations": {
                "regulations": ["string"],
                "certifications": ["string"],
                "dataPrivacyRequirements": ["string"],
                "complianceComplexity": "low|medium|high"
            },
            "swotAnalysis": {
                "strengths": ["string"],
                "weaknesses": ["string"],
                "opportunities": ["string"],
                "threats": ["string"]
            },
            "agentRouting": [
                {
                    "agentType": "string",
                    "priority": "low|medium|high",
                    "specificFocus": ["string"]
                }
            ],
            "confidenceScores": {
                "industryClassification": "number between 0-1",
                "competitorIdentification": "number between 0-1",
                "marketSizing": "number between 0-1",
                "regulatoryAssessment": "number between 0-1",
                "overallConfidence": "number between 0-1"
            },
            "dataGaps": ["string"]
        }