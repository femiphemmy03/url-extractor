 
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

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate