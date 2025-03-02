import json
from openai import OpenAI
from typing import Dict, List, Any, Optional
import re

class CompetitorAgentResearch:
    def __init__(self, api_key: str, perplexity_api: str, business_data: Dict[str, Any]):
        """
        Initialize the CompetitorAgentResearch with API keys and business data.
        
        Args:
            api_key (str): OpenAI API key for GPT model access
            perplexity_api (str): Perplexity API key for search functionality
            business_data (Dict[str, Any]): Dictionary containing business context information
        """
        self.api_key = api_key
        self.openai_api_key = api_key
        self.client = OpenAI(api_key=self.openai_api_key)
        self.business_data = business_data
        self.industry_analysis = business_data.get("industryAnalysis", {})
        self.original_request = business_data.get("originalRequest", {})
        self.perplexity_client = OpenAI(api_key=perplexity_api, base_url="https://api.perplexity.ai")
        
    def _build_prompt(self) -> str:
        """Build the prompt for generating search queries based on business data."""
        business_idea = self.original_request.get("businessIdea", {})
        basic_context = self.original_request.get("basicContext", {})
        
        return f"""Generate one detailed search query to research competitors in the mobile payment processing industry for small businesses.

Important instructions:
1. Do NOT include ANY specific competitor company names in the query
2. Do NOT include specific years (like 2023, 2024, etc.) in the query
3. Your search query MUST focus on finding information about:
   - Major competitors in the mobile payment processing industry
   - Market share of leading companies
   - Strengths and weaknesses of top players
   - Business models and pricing structures
   - Competitive analysis and comparisons
4. The query should be something that can be directly pasted into a search engine
5. Format as a plain text query without any explanations

Business context (for your reference only):
- Business: {business_idea.get("shortName", "")} - {business_idea.get("description", "")}
- Industry: {self.industry_analysis.get("primaryIndustry", "")}
- Target: {basic_context.get("targetCustomers", "")}
- Context: {self.original_request.get("additionalContext", "")}"""
    
    def generate_search_queries(self) -> List[str]:
        """
        Generate search queries for competitor research.
        
        Returns:
            List[str]: List of search queries
        """
        try:
            prompt = self._build_prompt()
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a market research expert creating search queries. Your task is to create one detailed search query that finds information about competitors, their market share, strengths, and weaknesses without naming ANY specific companies or years. Return ONLY the query text without explanations or formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            query = response.choices[0].message.content.strip()
            
            # Remove any quotes or formatting that might be in the response
            query = query.strip('"\'').replace('```', '').strip()
            
            # Filter out years (2020-2029)
            query = re.sub(r'\b20[0-9]{2}\b', '', query)
            
            # Ensure the query has key terms for competitor analysis
            key_terms = ["competitors", "market share", "strengths", "weaknesses"]
            missing_terms = [term for term in key_terms if term not in query.lower()]
            
            if missing_terms:
                # Add missing key terms to the query
                query += " " + " ".join(missing_terms)
            
            # Add site:*.com if not present to improve search quality
            if "site:" not in query:
                query += " site:*.com"
                
            # Clean up any double spaces from removals
            query = re.sub(r'\s+', ' ', query).strip()
                
            if not query or len(query) < 10:
                # Fallback if we get an empty or very short query
                query = "mobile payment processing industry competitors market share strengths weaknesses competitive analysis small businesses site:*.com"
                
            return [query]  # Return as list for compatibility with rest of code
            
        except Exception as e:
            # For API use, re-raise the exception to be handled by the API framework
            # or return a fallback query with error metadata
            return ["mobile payment processing industry competitors market share strengths weaknesses competitive analysis small businesses site:*.com"]
    
    def execute_searches(self, queries: List[str]) -> Dict[str, Any]:
        """
        Execute the search queries using Perplexity API.
        
        Args:
            queries (List[str]): List of search queries to execute
            
        Returns:
            Dict[str, Any]: Dictionary containing search results
        """
        try:
            search_results = {}
            for i, query in enumerate(queries):
                # Use the Perplexity client to search for the query
                response = self.perplexity_client.chat.completions.create(
                    model="sonar-pro",
                    messages=[
                        {"role": "system", "content": "You are a search engine that returns detailed results for market research queries. Search for information about competitors in the mobile payment processing industry, including their market share, strengths, and weaknesses."},
                        {"role": "user", "content": f"Perform a detailed search for: {query}"}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
                
                search_results[f"query_{i+1}"] = {
                    "query": query,
                    "results": response.choices[0].message.content
                }
                
            return {"queries": queries, "results": search_results}
            
        except Exception as e:
            # Return a structured error result for API consumption
            error_message = str(e)
            return {
                "error": error_message,
                "queries": queries, 
                "results": {
                    "query_1": {
                        "query": queries[0] if queries else "",
                        "results": f"Error: {error_message}"
                    }
                }
            }
    
    def analyze_competitors(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the search results to extract competitor information in the requested format.
        
        Args:
            search_results (Dict[str, Any]): Dictionary containing search results
            
        Returns:
            Dict[str, Any]: Dictionary containing competitor analysis
        """
        prompt = f"""Analyze the following search results about competitors in the mobile payment processing industry:
        
{json.dumps(search_results, indent=2)}

Extract information about the major competitors. For each competitor, provide:
1. Name of the competitor
2. A brief description of their business and positioning in the market
3. A list of their strengths
4. A list of their weaknesses

Format the response as structured JSON with the following schema:
{{
  "competitors": {{
    "[competitor_name]": {{
      "description": "Brief description of the competitor",
      "strengths": ["Strength 1", "Strength 2", ...],
      "weaknesses": ["Weakness 1", "Weakness 2", ...]
    }},
    // More competitors
  }}
}}

Include at least 5 major competitors in your analysis.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a market research expert analyzing competitive data. Always respond with valid JSON structured according to the requested schema."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            analysis = json.loads(content)
            return analysis
            
        except Exception as e:
            # Return a structured error for API consumption
            return {"error": str(e), "competitors": {}}
    
    def get_competitor_analysis(self) -> Dict[str, Any]:
        """
        Run the complete analysis pipeline and return competitor data.
        This is the main method to be called from the API endpoint.
        
        Returns:
            Dict[str, Any]: Dictionary containing competitor analysis
        """
        try:
            # Step 1: Generate search queries
            queries = self.generate_search_queries()
            
            # Step 2: Execute searches
            search_results = self.execute_searches(queries)
            
            # Check if there was an error in search execution
            if "error" in search_results:
                return {"status": "error", "message": search_results["error"], "competitors": {}}
            
            # Step 3: Analyze competitors
            analysis = self.analyze_competitors(search_results)
            
            # Check if there was an error in analysis
            if "error" in analysis:
                return {"status": "error", "message": analysis["error"], "competitors": {}}
            
            # Return successful result
            return {"status": "success", "data": analysis}
        
        except Exception as e:
            # Handle any unexpected errors
            return {"status": "error", "message": str(e), "competitors": {}}