import os
import json
import requests
from app.config import Config


class GoogleTrendsAnalyzer:
    def __init__(self, serpapi_key=None):
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_KEY")
        if not self.serpapi_key:
            raise ValueError("SerpAPI key is required. Provide it as an argument or set SERPAPI_KEY environment variable.")
        
        self.base_url = "https://serpapi.com/search"
    
    def analyze_trend(self, query, geo="US", period="now 1-d", data_type="TIMESERIES"):
        params = {
            "engine": "google_trends",
            "q": query,
            "geo": geo,
            "date": period,
            "data_type": data_type,
            "api_key": self.serpapi_key
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def compare_trends(self, queries, geo="US", period="now 1-d"):
        if isinstance(queries, list):
            query_string = ",".join(queries)
        else:
            query_string = queries
            
        params = {
            "engine": "google_trends",
            "q": query_string,
            "geo": geo,
            "date": period,
            "data_type": "TIMESERIES",
            "api_key": self.serpapi_key
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_related_queries(self, query, geo="US"):
        params = {
            "engine": "google_trends",
            "q": query,
            "geo": geo,
            "data_type": "RELATED_QUERIES",
            "api_key": self.serpapi_key
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_interest_by_region(self, query, geo="US"):
        params = {
            "engine": "google_trends",
            "q": query,
            "geo": geo,
            "data_type": "GEO_MAP_0",
            "api_key": self.serpapi_key
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        return response.json()

def test_trends_analyzer():
    try:
        analyzer = GoogleTrendsAnalyzer()
        
        print("1. Testing single trend analysis...")
        result = analyzer.analyze_trend("artificial intelligence", period="now 7-d")
        if "interest_over_time" in result:
            print("✅ Single trend analysis successful")
            with open("trend_result.json", "w") as f:
                json.dump(result, f, indent=2)
            print("   Results saved to trend_result.json")
        else:
            print("❌ Single trend analysis failed")
            print(result)
        
        print("\n2. Testing trend comparison...")
        result = analyzer.compare_trends(["AI", "machine learning", "data science"], period="now 7-d")
        if "interest_over_time" in result:
            print("✅ Trend comparison successful")
            with open("comparison_result.json", "w") as f:
                json.dump(result, f, indent=2)
            print("   Results saved to comparison_result.json")
        else:
            print("❌ Trend comparison failed")
            print(result)
        
        print("\n3. Testing related queries...")
        result = analyzer.get_related_queries("artificial intelligence")
        if "related_queries" in result:
            print("✅ Related queries successful")
            with open("related_queries_result.json", "w") as f:
                json.dump(result, f, indent=2)
            print("   Results saved to related_queries_result.json")
        else:
            print("❌ Related queries failed")
            print(result)
        
        print("\n4. Testing interest by region...")
        result = analyzer.get_interest_by_region("artificial intelligence")
        if "interest_by_region" in result:
            print("✅ Interest by region successful")
            with open("region_interest_result.json", "w") as f:
                json.dump(result, f, indent=2)
            print("   Results saved to region_interest_result.json")
        else:
            print("❌ Interest by region failed")
            print(result)
        
        print("\nAll tests completed!")
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Starting Google Trends Analyzer tests using SerpAPI...\n")
    test_trends_analyzer()