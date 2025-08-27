# src/scraper/company_scraper.py
import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import logging

class CompanyScraperError(Exception):
    pass

class CompanyDataScraper:
    def __init__(self, delay: int = 2):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_company_basics(self, url: str) -> Dict:
        """Extract basic company information from website"""
        try:
            if not url or not url.startswith("http"):
                raise CompanyScraperError("Invalid URL provided.")
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Dummy data for scaffolding
            return {
                "company_name": "Example Corp",
                "industry": "Technology",
                "tech_stack": ["Python", "React", "AWS"],
                "services": ["Web Development", "Cloud Solutions"]
            }
        except CompanyScraperError as e:
            logging.error(f"CompanyDataScraper error: {e}")
            return {"error": str(e)}
        except Exception as e:
            logging.error(f"Unexpected error in CompanyDataScraper: {e}")
            return {"error": "Failed to scrape company data."}
    
    def _extract_company_name(self, soup: BeautifulSoup) -> str:
        # Try multiple strategies to find company name
        selectors = [
            'title',
            'h1',
            '.company-name',
            '[data-testid="company-name"]',
            'meta[property="og:site_name"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get('content') if element.name == 'meta' else element.get_text()
                if text and len(text.strip()) > 0:
                    return text.strip().split('|')[0].split('-')[0].strip()
        return "Unknown Company"
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        # Extract company description from meta tags or content
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')
        
        # Fallback to first paragraph or hero section
        hero_text = soup.select_one('.hero p, .intro p, main p, .about p')
        return hero_text.get_text().strip() if hero_text else ""
    
    def _extract_services(self, soup: BeautifulSoup) -> List[str]:
        # Look for services sections
        services = []
        service_sections = soup.find_all(['div', 'section'], 
                                       class_=lambda x: x and any(word in x.lower() 
                                                                for word in ['service', 'offering', 'solution']))
        
        for section in service_sections:
            items = section.find_all(['h3', 'h4', 'li'])
            services.extend([item.get_text().strip() for item in items if item.get_text().strip()])
        
        return services[:10]  # Limit to top 10
    
    def _detect_tech_stack(self, response, soup: BeautifulSoup) -> List[str]:
        tech_stack = []
        
        # Check response headers
        server = response.headers.get('server', '')
        if server:
            tech_stack.append(server)
        
        # Check for common frameworks/tools in HTML
        html_content = str(soup).lower()
        
        tech_indicators = {
            'react': ['react', '_next', '__next'],
            'vue': ['vue.js', 'nuxt'],
            'angular': ['angular', 'ng-'],
            'wordpress': ['wp-content', 'wordpress'],
            'shopify': ['shopify', 'myshopify'],
            'webflow': ['webflow'],
            'squarespace': ['squarespace']
        }
        
        for tech, indicators in tech_indicators.items():
            if any(indicator in html_content for indicator in indicators):
                tech_stack.append(tech.title())
        
        return tech_stack
