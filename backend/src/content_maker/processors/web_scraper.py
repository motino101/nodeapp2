#!/usr/bin/env python3
"""
Web Scraping RAG Layer for processing webpage URLs
"""

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, timeout=10, max_retries=3, delay=1):
        """
        Initialize web scraper with configuration
        
        Args:
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retry attempts
            delay (float): Delay between requests in seconds
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.delay = delay
        self.session = requests.Session()
        
        # Set user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def is_valid_url(self, url):
        """Check if URL is valid and accessible"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and parsed.scheme in ['http', 'https']
        except:
            return False
    
    def extract_webpage_urls(self, text):
        """Extract webpage URLs from text content"""
        # Pattern to match URLs (excluding Google Docs)
        url_pattern = r'https?://(?!docs\.google\.com)[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        
        # Filter and validate URLs
        valid_urls = []
        for url in urls:
            # Clean up URL (remove trailing punctuation)
            url = re.sub(r'[.,;:!?]+$', '', url)
            if self.is_valid_url(url):
                valid_urls.append(url)
        
        return list(set(valid_urls))  # Remove duplicates
    
    def scrape_webpage(self, url):
        """
        Scrape content from a webpage
        
        Args:
            url (str): URL to scrape
            
        Returns:
            dict: Scraped content with metadata
        """
        print(f"🌐 Scraping webpage: {url}")
        
        for attempt in range(self.max_retries):
            try:
                print(f"🔗 Attempt {attempt + 1}/{self.max_retries}")
                
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # Parse HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract metadata
                title = self._extract_title(soup)
                description = self._extract_description(soup)
                
                # Extract main content
                content = self._extract_main_content(soup)
                
                # Clean and process content
                cleaned_content = self._clean_content(content)
                
                print(f"✅ Successfully scraped: {title}")
                print(f"📝 Content length: {len(cleaned_content)} characters")
                
                return {
                    'url': url,
                    'title': title,
                    'description': description,
                    'content': cleaned_content,
                    'status': 'success'
                }
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))  # Exponential backoff
                else:
                    return {
                        'url': url,
                        'title': 'Scraping Failed',
                        'description': f'Failed to scrape: {str(e)}',
                        'content': f'[Webpage scraping failed: {url}]',
                        'status': 'error',
                        'error': str(e)
                    }
            
            except Exception as e:
                print(f"❌ Unexpected error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))
                else:
                    return {
                        'url': url,
                        'title': 'Scraping Failed',
                        'description': f'Unexpected error: {str(e)}',
                        'content': f'[Webpage scraping failed: {url}]',
                        'status': 'error',
                        'error': str(e)
                    }
    
    def _extract_title(self, soup):
        """Extract page title"""
        # Try different title selectors
        title_selectors = [
            'title',
            'h1',
            'meta[property="og:title"]',
            'meta[name="twitter:title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    title = element.get('content', '').strip()
                else:
                    title = element.get_text().strip()
                
                if title and len(title) > 0:
                    return title[:200]  # Limit title length
        
        return "Untitled Webpage"
    
    def _extract_description(self, soup):
        """Extract page description"""
        description_selectors = [
            'meta[name="description"]',
            'meta[property="og:description"]',
            'meta[name="twitter:description"]'
        ]
        
        for selector in description_selectors:
            element = soup.select_one(selector)
            if element:
                description = element.get('content', '').strip()
                if description:
                    return description[:300]  # Limit description length
        
        return ""
    
    def _extract_main_content(self, soup):
        """Extract main content from webpage"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
            element.decompose()
        
        # Try to find main content areas
        content_selectors = [
            'main',
            'article',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-content',
            '#content',
            '#main',
            '.main-content'
        ]
        
        main_content = None
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                main_content = element
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body')
        
        if main_content:
            return main_content.get_text()
        else:
            return soup.get_text()
    
    def _clean_content(self, content):
        """Clean and process scraped content"""
        if not content:
            return ""
        
        # Split into lines and clean
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Strip whitespace
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip very short lines (likely navigation/ads)
            if len(line) < 10:
                continue
            
            # Skip lines that look like navigation or ads
            if any(skip_word in line.lower() for skip_word in [
                'cookie', 'privacy', 'terms', 'subscribe', 'newsletter',
                'follow us', 'share', 'like', 'comment', 'advertisement',
                'sponsored', 'click here', 'read more', 'continue reading'
            ]):
                continue
            
            cleaned_lines.append(line)
        
        # Join lines and clean up
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Remove excessive whitespace
        cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)
        
        # Limit content length (keep first 5000 characters)
        if len(cleaned_content) > 5000:
            cleaned_content = cleaned_content[:5000] + "\n\n[Content truncated...]"
        
        return cleaned_content
    
    def process_webpage_urls(self, text_content):
        """
        Process all webpage URLs found in text content
        
        Args:
            text_content (str): Text content that may contain URLs
            
        Returns:
            list: List of scraped webpage content
        """
        urls = self.extract_webpage_urls(text_content)
        
        if not urls:
            return []
        
        print(f"🔍 Found {len(urls)} webpage URL(s) to scrape")
        
        scraped_content = []
        for url in urls:
            result = self.scrape_webpage(url)
            scraped_content.append(result)
            
            # Add delay between requests to be respectful
            time.sleep(self.delay)
        
        return scraped_content

# Example usage and testing
if __name__ == "__main__":
    scraper = WebScraper()
    
    # Test with sample text containing URLs
    test_text = """
    Check out this interesting article about digital gardening: https://example.com/digital-gardening-guide
    Also, here's a useful resource: https://github.com/maggieappleton/digital-gardeners
    And this blog post: https://www.technologyreview.com/2020/09/03/1007716/digital-gardens-let-you-cultivate-your-own-little-bit-of-the-internet/
    """
    
    print("🧪 Testing web scraping functionality")
    print("=" * 50)
    
    # Extract URLs
    urls = scraper.extract_webpage_urls(test_text)
    print(f"📋 Found URLs: {urls}")
    
    # Test scraping (this will fail for example.com but shows the process)
    for url in urls[:1]:  # Just test first URL
        print(f"\n🔍 Testing scrape of: {url}")
        result = scraper.scrape_webpage(url)
        print(f"Result: {result['status']}")
        if result['status'] == 'success':
            print(f"Title: {result['title']}")
            print(f"Content preview: {result['content'][:200]}...")
