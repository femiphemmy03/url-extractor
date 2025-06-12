import sys
import logging
import email
from email import policy
import re
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(name)s: %(message)s'
)
logger = logging.getLogger('main')

class URLExtractor:
    """Class to extract URLs from .eml files."""
    
    def __init__(self):
        """Initialize URLExtractor."""
        self.urls = set()  # Store unique URLs
    
    def extract_html_content(self, eml_path):
        """Parse .eml file and extract HTML or text content."""
        try:
            logger.info(f"Reading email file: {eml_path}")
            with open(eml_path, 'r', encoding='utf-8', errors='ignore') as f:
                msg = email.message_from_file(f, policy=policy.default)
            
            content = ''
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type in ['text/plain', 'text/html']:
                        payload = part.get_payload(decode=True)
                        if payload:
                            content += payload.decode('utf-8', errors='ignore')
            else:
                content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            if not content:
                logger.warning("No content found in email")
                return None
            
            logger.info("Email content extracted successfully")
            
            # Parse HTML if present
            if 'text/html' in msg.get_content_type() or '<html' in content.lower():
                soup = BeautifulSoup(content, 'html.parser')
                content = soup.get_text()
                logger.info("HTML body extracted successfully")
            
            return content
        
        except FileNotFoundError:
            logger.error(f"File not found: {eml_path}")
            return None
        except Exception as e:
            logger.error(f"Error processing {eml_path}: {str(e)}")
            return None
    
    def extract_urls(self, content):
        """Extract and validate URLs from content."""
        if not content:
            logger.warning("No content to extract URLs from")
            return
        
        # Regex for HTTP/HTTPS URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, content)
        
        if not urls:
            logger.info("No URLs found in content")
            return
        
        self.urls.update(urls)
        logger.info(f"Extracted {len(urls)} URLs")
    
    def get_unique_urls(self):
        """Return unique URLs."""
        return self.urls
    
    def process_eml_file(self, eml_path):
        """Process a single .eml file."""
        content = self.extract_html_content(eml_path)
        if content:
            self.extract_urls(content)
            if self.urls:
                logger.info("Unique URLs found:")
                for url in self.urls:
                    print(url)
                print(f"Total unique URLs: {len(self.urls)}")
            else:
                logger.info("No URLs found in email")

def main():
    """Main function to process command-line argument."""
    if len(sys.argv) != 2:
        logger.error("Usage: python url_extractor.py path/to/email.eml")
        sys.exit(1)
    
    eml_path = sys.argv[1]
    extractor = URLExtractor()
    extractor.process_eml_file(eml_path)

if __name__ == '__main__':
    main()
