import re
from bs4 import BeautifulSoup
import requests

def extract_text_from_url( url):
    """Extract text content from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find main content areas
        content_selectors = [
            'article', '.article', '#article',
            '.post', '.content', '.entry-content',
            'main', '.main', '#main',
            '.story', '.text', 'p'
        ]
        
        text = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                text = ' '.join([elem.get_text() for elem in elements])
                break
        
        if not text:
            text = soup.get_text()
        
        # Clean the text
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from URL: {str(e)}")

print (extract_text_from_url(r"https://en.wikipedia.org/wiki/Elon_Musk"))