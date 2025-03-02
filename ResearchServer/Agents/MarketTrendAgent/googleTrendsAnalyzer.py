import os
import json
import requests
from datetime import datetime, timedelta
import numpy as np
from openai import OpenAI

class GoogleTrendsAnalyzer:
    def __init__(self, serpapi_key, openai_key):
        self.serpapi_key = serpapi_key
        self.openai_client = OpenAI(api_key=openai_key)
        self.base_url = "https://serpapi.com/search"
        self.current_date = datetime.now()
    
    def fetch_yearly_trend(self, query, geo="US"):
        params = {
            "engine": "google_trends",
            "q": query,
            "geo": geo,
            "date": "today 12-m",
            "data_type": "TIMESERIES",
            "api_key": self.serpapi_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                return None
            return response.json()
        except Exception:
            return None
    
    def extract_monthly_data(self, trend_data):
        if not trend_data or "interest_over_time" not in trend_data:
            return []
        
        timeline_data = trend_data["interest_over_time"].get("timeline_data", [])
        monthly_data = {}
        start_date = self.current_date - timedelta(days=365)
        
        for point in timeline_data:
            date_str = point.get("date", "").split("–")[0].strip()
            
            try:
                for fmt in ["%b %d, %Y", "%b %d %Y", "%Y-%m-%d", "%b %d"]:
                    try:
                        if fmt == "%b %d":
                            parsed_date = datetime.strptime(date_str, fmt)
                            parsed_date = parsed_date.replace(
                                year=self.current_date.year - 1 if parsed_date.month > self.current_date.month else self.current_date.year
                            )
                        else:
                            parsed_date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    continue
                
                if parsed_date < start_date or parsed_date > self.current_date:
                    continue
                
                year_month = f"{parsed_date.year}-{parsed_date.month:02d}"
                
                values = point.get("values", [])
                value = values[0].get("extracted_value", 0) if isinstance(values, list) and values else 0
                
                if year_month not in monthly_data:
                    monthly_data[year_month] = []
                
                monthly_data[year_month].append(value)
                
            except Exception:
                continue
        
        return [
            {"month": month, "average_value": sum(values) / len(values) if values else 0}
            for month, values in sorted(monthly_data.items())
        ]
    
    def forecast_next_6_months(self, monthly_data):
        if not monthly_data or len(monthly_data) < 3:
            return []
        
        values = [item["average_value"] for item in monthly_data][-3:]
        
        if len(values) < 3:
            return []
        
        trend = (values[-1] - values[0]) / 2
        recent_avg = sum(values) / len(values)
        
        forecasts = []
        current_year = self.current_date.year
        current_month = self.current_date.month
        
        for i in range(6):
            forecast_month = (current_month + i - 1) % 12 + 1
            forecast_year = current_year + ((current_month + i - 1) // 12)
            
            variation = recent_avg * 0.05 * (np.random.random() - 0.5)
            predicted_value = max(0, recent_avg + (trend * i) + variation)
            
            forecasts.append({
                "month": f"{forecast_year}-{forecast_month:02d}",
                "predicted_value": round(predicted_value, 1)
            })
        
        return forecasts
    
    def analyze_trends_with_openai(self, trends_summary):
        if not trends_summary["keywords"]:
            return "No significant trends identified."
        
        prompt = f"""
        Analyze the market trends based on the following insights:
        
        {json.dumps(trends_summary, indent=2)}
        
        Provide:
        1. Overall market trend analysis
        2. Key opportunities by region
        3. Seasonal patterns observed
        4. Recommended timing for product launches
        5. Strategic prioritization of markets
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in market trends analysis and business strategy."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception:
            return "Unable to generate insights due to an API error."
    
    def extract_business_analytics_data(self, business_analytics_data):
        try:
            keywords = []
            regions = []
            
            if "industryAnalysis" in business_analytics_data:
                industry_analysis = business_analytics_data["industryAnalysis"]
                
                if "primaryIndustry" in industry_analysis:
                    keywords.append(industry_analysis["primaryIndustry"])
                
                if "subIndustries" in industry_analysis:
                    keywords.extend(industry_analysis["subIndustries"])
                
                if "keywords" in industry_analysis:
                    keywords.extend(industry_analysis["keywords"])
                
                if "potentialGeographicMarkets" in industry_analysis:
                    regions = industry_analysis["potentialGeographicMarkets"]
            
            if not keywords and "originalRequest" in business_analytics_data:
                request = business_analytics_data["originalRequest"]
                
                if "businessIdea" in request and "shortName" in request["businessIdea"]:
                    keywords.append(request["businessIdea"]["shortName"])
                
                if "basicContext" in request and "industry" in request["basicContext"]:
                    keywords.append(request["basicContext"]["industry"])
                
                if not regions and "geographicInterest" in request:
                    regions = request["geographicInterest"]
            
            keywords = list(set(filter(None, keywords)))
            regions = list(set(filter(None, regions)))
            
            if len(keywords) > 3:
                keywords = keywords[:3]
            
            return {
                "keywords": keywords,
                "regions": regions
            }
        except Exception as e:
            return {
                "keywords": [],
                "regions": [],
                "error": str(e)
            }
    
    def analyze_market_trends(self, request_data):
        if isinstance(request_data, dict) and ("industryAnalysis" in request_data or "originalRequest" in request_data):
            extracted_data = self.extract_business_analytics_data(request_data)
            keywords = extracted_data.get("keywords", [])
            regions = extracted_data.get("regions", [])
            
            if "error" in extracted_data:
                return {"error": f"Failed to extract data: {extracted_data['error']}"}
        else:
            if "keywords" not in request_data or "regions" not in request_data:
                return {"error": "Missing required fields: keywords and regions"}
            
            keywords = request_data["keywords"]
            regions = request_data["regions"]
        
        if not keywords or not regions:
            return {"error": "Empty keywords or regions list"}
        
        # Temporary
        if isinstance(keywords, list):
            keywords = keywords[0]

        if isinstance(regions, list):
            regions = regions[0]

        trends_data = {}
        for keyword in keywords:
            trends_data[keyword] = {}
            for region in regions:
                try:
                    trend_result = self.fetch_yearly_trend(keyword, geo=region)
                    if trend_result:
                        monthly_data = self.extract_monthly_data(trend_result)
                        forecast = self.forecast_next_6_months(monthly_data)
                        trends_data[keyword][region] = {
                            "monthly_data": monthly_data,
                            "forecast": forecast
                        }
                except Exception as e:
                    trends_data[keyword][region] = {"error": str(e)}
        
        trends_summary = {"keywords": trends_data}
        ai_analysis = self.analyze_trends_with_openai(trends_summary)
        
        return {
            "insights": {
                "detailed_trends": trends_data,
                "trends_summary": trends_summary,
                "ai_analysis": ai_analysis
            }
        }
