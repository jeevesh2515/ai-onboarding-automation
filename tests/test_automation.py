# tests/test_automation.py
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper.company_scraper import CompanyDataScraper
from src.analyzer.business_analyzer import BusinessAnalyzer

class TestAutomationSystem:
    def test_scraper_initialization(self):
        scraper = CompanyDataScraper()
        assert scraper.delay == 2
        assert scraper.session is not None
    
    def test_company_name_extraction(self):
        scraper = CompanyDataScraper()
        # Test with mock HTML
        from bs4 import BeautifulSoup
        html = "<html><head><title>Test Company | Homepage</title></head></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        name = scraper._extract_company_name(soup)
        assert name == "Test Company"
    
    def test_business_analyzer_initialization(self):
        analyzer = BusinessAnalyzer("test-api-key")
        assert analyzer.client is not None

# Run tests
if __name__ == "__main__":
    pytest.main([__file__])
