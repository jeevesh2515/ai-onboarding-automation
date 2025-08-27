# src/analyzer/business_analyzer.py
import openai
import json
import logging
import os
from typing import Dict, List

class BusinessAnalyzerError(Exception):
    pass

class BusinessInsights:
    def __init__(self):
        self.target_audience = ["Startups", "SMBs"]
        self.pain_points = ["Scaling", "Security"]
        self.opportunities = ["Cloud Migration", "AI Integration"]
        self.project_recommendations = ["Build scalable web app", "Implement AI chatbot"]

class BusinessAnalyzer:
    def __init__(self, api_key):
        # 👉 Pass your OpenAI API key here
        self.api_key = api_key
        openai.api_key = api_key  # <-- Your OpenAI API key is set here
    
    def analyze_business_needs(self, company_data: Dict) -> BusinessInsights:
        """Generate comprehensive business analysis using AI"""
        
        analysis_prompt = f"""
        Analyze this company data and provide detailed business insights:
        
        Company: {company_data.get('company_name', 'Unknown')}
        Industry: {company_data.get('industry', 'Unknown')}
        Description: {company_data.get('description', '')}
        Services: {', '.join(company_data.get('services', []))}
        Tech Stack: {', '.join(company_data.get('tech_stack', []))}
        Team Size: {company_data.get('team_size', 'Unknown')}
        
        Please provide analysis in this JSON format:
        {{
            "industry_analysis": "Deep analysis of their industry position",
            "target_audience": ["audience segment 1", "audience segment 2"],
            "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
            "opportunities": ["opportunity 1", "opportunity 2"],
            "project_recommendations": ["recommendation 1", "recommendation 2"],
            "budget_estimate": {{
                "small_project": 5000,
                "medium_project": 15000,
                "large_project": 35000
            }},
            "timeline_estimate": "X-Y weeks"
        }}
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a senior business analyst specializing in digital transformation and web development projects."},
                {"role": "user", "content": analysis_prompt}
            ]
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            analysis_json = json.loads(response.choices[0].message.content)
            return BusinessInsights(**analysis_json)
        except Exception as e:
            # Log and handle errors
            print(f"OpenAI error: {e}")
            # Fallback with default values
            return BusinessInsights()
