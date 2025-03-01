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
        except Exception as e:
            return None
    
    def extract_monthly_data(self, trend_data):
        if not trend_data or "interest_over_time" not in trend_data:
            return []
        
        timeline_data = trend_data["interest_over_time"].get("timeline_data", [])
        monthly_data = {}
        start_date = self.current_date - timedelta(days=365)
        
        for point in timeline_data:
            date_str = point.get("date", "")
            if "–" in date_str:
                date_str = date_str.split("–")[0].strip()
            
            try:
                for fmt in ["%b %d, %Y", "%b %d %Y", "%Y-%m-%d", "%b %d"]:
                    try:
                        if fmt == "%b %d":
                            parsed_date = datetime.strptime(date_str, fmt)
                            if parsed_date.month > self.current_date.month:
                                parsed_date = parsed_date.replace(year=self.current_date.year - 1)
                            else:
                                parsed_date = parsed_date.replace(year=self.current_date.year)
                            break
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
                if not values:
                    continue
                
                if isinstance(values[0], dict) and "extracted_value" in values[0]:
                    value = values[0]["extracted_value"]
                elif isinstance(values, list) and len(values) > 0:
                    value = values[0].get("extracted_value", 0)
                else:
                    value = 0
                
                if year_month not in monthly_data:
                    monthly_data[year_month] = []
                
                monthly_data[year_month].append(value)
                
            except Exception as e:
                continue
        
        monthly_averages = [
            {
                "month": month,
                "average_value": sum(values) / len(values) if values else 0
            }
            for month, values in monthly_data.items()
        ]
        
        monthly_averages.sort(key=lambda x: x["month"])
        
        return monthly_averages
    
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
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in market trends analysis and business strategy."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return "Unable to generate insights due to an API error."
    
    def analyze_market_trends(self, request_data):
        if "keywords" not in request_data or "regions" not in request_data:
            return {"error": "Missing required fields: keywords and regions"}
        
        keywords = request_data["keywords"]
        regions = request_data["regions"]
        
        if not keywords or not regions:
            return {"error": "Empty keywords or regions list"}
        
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
            "detailed_trends": trends_data,
            "trends_summary": trends_summary,
            "ai_analysis": ai_analysis
        }
