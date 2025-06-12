import os
import json
import logging
from multiprocessing import Pool
from url_extractor import URLExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(name)s: %(message)s'
)
logger = logging.getLogger('batch')

def process_single_email(eml_path):
    """Process a single .eml file and return results."""
    extractor = URLExtractor()
    extractor.process_eml_file(eml_path)
    return {
        'file': eml_path,
        'urls': list(extractor.get_unique_urls()),
        'url_count': len(extractor.get_unique_urls())
    }

def batch_process_emails(spam_dir, good_dir):
    """Process all .eml files in directories using parallel processing."""
    email_files = []
    for directory in [spam_dir, good_dir]:
        for filename in os.listdir(directory):
            if filename.endswith('.eml'):
                email_files.append(os.path.join(directory, filename))
    
    logger.info(f"Processing {len(email_files)} emails")
    
    # Parallel processing
    with Pool() as pool:
        results = pool.map(process_single_email, email_files)
    
    # Save results to JSON
    with open('url_extraction_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate summary
    total_emails = len(results)
    total_urls = sum(r['url_count'] for r in results)
    unique_urls = set()
    for r in results:
        unique_urls.update(r['urls'])
    
    summary = {
        'total_emails_processed': total_emails,
        'total_urls_extracted': total_urls,
        'unique_urls_count': len(unique_urls)
    }
    
    with open('url_extraction_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Processed {total_emails} emails, extracted {total_urls} URLs, {len(unique_urls)} unique")
    return results

if __name__ == '__main__':
    spam_dir = 'emails/spam'
    good_dir = 'emails/good'
    batch_process_emails(spam_dir, good_dir)
