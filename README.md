## Dataset
- Generated 500 production-ready `.eml` files (250 genuine, 250 spam/phishing).
- **Genuine Emails**: Use `Enron.csv` from the [Kaggle Phishing Email Dataset](https://www.kaggle.com/datasets/subhajit3798/phishing-site-prediction) for subjects and bodies, with generated senders (e.g., `hr@techcorp.com`) and receivers (e.g., `femi.ade@example.com`). Plain-text, professional content.
- **Spam/Phishing Emails**: Use `Nazario.csv` and `CEAS_08.csv` for senders (e.g., `Amazon.com <amazon@croydonpodiatrygroup.com.au>`), subjects, bodies, and URLs. HTML with quoted-printable encoding.
- Fallback templates used for missing dataset entries.
- Sample emails in `emails/sample/`.

## Scripts
- `generate_emails.py`: Generates 500 `.eml` files, handles case-insensitive CSV loading and CEAS_08.csv.
- `url_extractor.py`: Extracts URLs from a single `.eml` file, handles quoted-printable encoding.
- `batch_process.py`: Processes all `.eml` files in parallel, generates `url_extraction_results.json` and `url_extraction_summary.json`, with case-insensitive directory handling.

## Results
- Processed 500 emails.
- Extracted 1078 URLs, with 204 unique URLs.
- Robust against quoted-printable, multipart emails, and case-sensitive filenames.