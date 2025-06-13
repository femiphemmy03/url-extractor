 
# URLExtractor Tool
Python Developer Intern Project for Datakerra Technologies

## Overview
This project implements a command-line `URLExtractor` tool that parses `.eml` email files, extracts HTML or text content, and identifies unique HTTP/HTTPS URLs. It processes a single `.eml` file via command-line argument and supports batch processing of 500 emails (250 genuine, 250 spam) with parallel processing and JSON output.

## Files
- `generate_emails.py`: Generates 500 mock `.eml` files (250 genuine, 250 spam).
- `url_extractor.py`: Main script with `URLExtractor` class for single-file URL extraction.
- `batch_process.py`: Batch processes 500 emails with parallel processing and JSON output.
- `url_extraction_results.json`: Detailed results for 500 emails.
- `url_extraction_summary.json`: Summary statistics.
- `requirements.txt`: Dependencies.
- `emails/`: Generated emails (samples in `emails/sample/`; full set available on request).

## Dataset
- Generated 500 production-ready `.eml` files (250 genuine, 250 spam/phishing) due to insufficient data in the provided Google Drive.
- **Genuine Emails**: Mimic professional, transactional, or personal communication with realistic senders (e.g., `hr@techcorp.com`), subjects (e.g., “Order Confirmation”), and content (e.g., meeting invites, receipts).
- **Spam/Phishing Emails**: Modeled after Kaggle phishing datasets with authentic phishing structures, including spoofed senders (e.g., `alert@paypa1.com`), urgent subjects, HTML bodies, and malicious URLs (e.g., `http://secure-login.xyz/verify`).
- Sample emails in `emails/sample/` (full set available on request).
- Public datasets (e.g., SpamAssassin) were not used; phishing structures were emulated based on Kaggle-inspired characteristics.

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate