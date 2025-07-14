import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse
import json

class ManimDocsScraper:
    def __init__(self, base_url="https://docs.manim.community/en/stable/reference/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.downloaded_urls = set()
        self.output_dir = "manim_docs"
        
    def create_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def get_page_content(self, url):
        """Fetch page content with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
            
    def extract_links(self, html_content, base_url):
        """Extract all documentation links from a page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        # Find all links that are within the reference section
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include links that are part of the reference documentation
            if '/reference/' in full_url and full_url.startswith('https://docs.manim.community'):
                # Remove fragment identifiers
                full_url = full_url.split('#')[0]
                links.add(full_url)
                
        return links
        
    def save_page(self, url, content):
        """Save page content to file, starting from the first <h1> onward."""
        soup = BeautifulSoup(content, 'html.parser')

        # Find the first <h1> tag
        h1 = soup.find('h1')
        if h1:
            # Collect all elements from the first <h1> to the end of its parent section/article
            elements = []
            # Find the closest parent <section> or <article> (or fallback to body)
            parent = h1.find_parent(['section', 'article', 'main', 'body'])
            found_h1 = False
            for elem in parent.descendants:
                if getattr(elem, 'name', None) == 'h1':
                    found_h1 = True
                if found_h1 and getattr(elem, 'name', None):
                    elements.append(elem)
            # Join the text from all collected elements
            text_content = '\n'.join(e.get_text(separator='\n', strip=True) for e in elements if hasattr(e, 'get_text'))
        else:
            # Fallback: extract main content as before
            main_content = soup.find('div', class_='document') or soup.find('main') or soup.body
            text_content = main_content.get_text(separator='\n', strip=True) if main_content else None

        if text_content:
            # Create filename from URL
            parsed_url = urlparse(url)
            filename = parsed_url.path.replace('/', '_').replace('.html', '') + '.txt'
            filename = filename.strip('_') or 'index'

            filepath = os.path.join(self.output_dir, filename)

            # Save both text and metadata
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"{'='*50}\n\n")
                f.write(text_content)

            # No longer save raw HTML for reference

            print(f"Saved: {filename}")
            return True
        return False
        
    def crawl_documentation(self):
        """Main crawling function"""
        self.create_output_dir()
        
        urls_to_visit = ['https://docs.manim.community/en/stable/reference.html']
        visited_urls = set()
        
        while urls_to_visit:
            current_url = urls_to_visit.pop(0)
            
            if current_url in visited_urls:
                continue
                
            print(f"Crawling: {current_url}")
            visited_urls.add(current_url)
            
            # Get page content
            content = self.get_page_content(current_url)
            if not content:
                continue
                
            # Save the page
            self.save_page(current_url, content)
            
            # Extract links and add to queue
            links = self.extract_links(content, current_url)
            for link in links:
                if link not in visited_urls:
                    urls_to_visit.append(link)
                    
            # Be respectful - small delay between requests
            time.sleep(0.5)
            
        # Save metadata
        metadata = {
            'total_pages': len(visited_urls),
            'urls_crawled': list(visited_urls),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(os.path.join(self.output_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
            
        print(f"\nCrawling complete! Downloaded {len(visited_urls)} pages to '{self.output_dir}' directory")
        
def main():
    scraper = ManimDocsScraper()
    # scraper.crawl_documentation()
    quickstart_url = 'https://docs.manim.community/en/stable/tutorials/quickstart.html'
    scraper.save_page(quickstart_url, scraper.get_page_content(quickstart_url))

if __name__ == "__main__":
    main()