import os
import random
import pandas as pd
from datetime import datetime
import quopri
import html
import re
import glob

def find_file(filename, directory='.'):
    """Find a file case-insensitively in the specified directory."""
    pattern = os.path.join(directory, filename.lower())
    matches = glob.glob(pattern, recursive=False)
    if not matches:
        pattern = os.path.join(directory, filename.upper())
        matches = glob.glob(pattern, recursive=False)
    if not matches:
        pattern = os.path.join(directory, filename.capitalize())
        matches = glob.glob(pattern, recursive=False)
    if not matches:
        # Try common variations (e.g., CEAS_08.csv)
        pattern = os.path.join(directory, filename.lower().replace('.csv', '_08.csv'))
        matches = glob.glob(pattern, recursive=False)
    return matches[0] if matches else None

def load_dataset(csv_path, label_filter=None):
    """Load email data from CSV, filter by label if specified."""
    csv_file = find_file(os.path.basename(csv_path))
    if not csv_file:
        print(f"Error: {csv_path} (or case variant) not found. Using fallback templates.")
        return None, csv_file
    try:
        df = pd.read_csv(csv_file)
        if label_filter is not None:
            df = df[df['label'] == label_filter] if isinstance(label_filter, int) else df[df['label'].str.contains(label_filter, case=False, na=False)]
        if len(df) > 250:
            df = df.sample(n=250, random_state=42)
        elif len(df) < 250:
            print(f"Warning: Only {len(df)} emails found in {csv_file}. Padding with fallback templates.")
        return df.to_dict('records'), csv_file
    except Exception as e:
        print(f"Error loading {csv_file}: {str(e)}. Using fallback templates.")
        return None, csv_file

def load_phishing_data():
    """Load and merge phishing emails from nazario.csv and CEAS_08.csv."""
    nazario_data, nazario_file = load_dataset('nazario.csv', label_filter='Phishing')
    ceas_data, ceas_file = load_dataset('CEAS_08.csv', label_filter=1)
    phishing_data = []
    if nazario_data:
        for data in nazario_data:
            data['source_file'] = nazario_file
        phishing_data.extend(nazario_data)
    if ceas_data:
        for data in ceas_data:
            data['source_file'] = ceas_file
        phishing_data.extend([d for d in ceas_data if d['label'] == 1])
    if len(phishing_data) > 250:
        phishing_data = random.sample(phishing_data, 250)
    elif len(phishing_data) < 250:
        print(f"Warning: Only {len(phishing_data)} phishing emails found. Padding with fallback templates.")
    return phishing_data

def generate_mock_email(email_id, email_type, genuine_data=None, phishing_data=None):
    """Generate a production-ready .eml file (genuine or spam/phishing)."""
    receiver = random.choice([
        'femi.ade@example.com', 'femi.ola@university.edu', 'femi@startup.ng',
        'femi.adewale@gmail.com', 'femi@techhub.ng'
    ])
    date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0100')

    if email_type == 'good':
        senders = [
            'hr@techcorp.com', 'support@bankoflagos.com', 'no-reply@ecommerce.ng',
            'prof.ade@university.edu', 'orders@shoponline.com', 'info@ngtech.com',
            'events@lagostechweek.com', 'billing@fintech.ng'
        ]
        fallback_subjects = [
            'Q3 Performance Review Meeting',
            'Your Transaction Receipt',
            'Welcome to Our Platform!',
            'Lecture Schedule Update',
            'Order Confirmation #ORD12345',
            'Invitation to Tech Webinar'
        ]
        fallback_bodies = [
            """Dear Femi,\nPlease join us for your Q3 performance review on Friday at 10 AM.\nBest regards,\nJane Doe, HR Manager""",
            """Dear Femi,\nYour transaction of NGN 5,000 was successful.\nRef: TXN789012\nThank you,\nBank of Lagos""",
            """Welcome to ShopOnline, Femi!\nExplore our products at http://shoponline.ng.\nCheers,\nThe ShopOnline Team""",
            """Dear Students,\nThe lecture schedule for CS101 has been updated.\nCheck http://university.edu/schedule.\nProf. Ade""",
            """Dear Femi,\nYour order #ORD12345 has been shipped.\nTrack at http://shoponline.ng/track.\nThank you,\nShopOnline"""
        ]
        content_type = 'text/plain'
        sender = random.choice(senders)
        subject = random.choice(fallback_subjects)
        body = random.choice(fallback_bodies)
        source = 'fallback_template'

        if genuine_data and email_id <= len(genuine_data):
            email_data = genuine_data[email_id - 1]
            subject = email_data.get('subject', subject)
            body = email_data.get('body', body)
            body = re.sub(r'\( see attached file.*?\)', '', body).strip()
            source = f'enron_row_{email_id}'
        encoded_body = body

    else:  # spam/phishing
        fallback_senders = [
            'alert@paypa1.com', 'security@amaz0n.com', 'verify@bank0fnigeria.com',
            'support@g00gle.com', 'promo@lotteryng.com', 'admin@secure-login.xyz'
        ]
        fallback_subjects = [
            'Urgent: Verify Your Account Now!',
            'Your PayPal Account is Suspended!',
            'Security Alert: Unusual Activity Detected',
            'Claim Your $1000 Amazon Gift Card!',
            'Your Bank Account Needs Immediate Action!'
        ]
        fallback_bodies = [
            """<html><body><p>Dear Customer,</p><p>Your PayPal account has been locked. Click <a href="http://secure-login.xyz/verify">here</a> to verify your identity.</p><p>PayPal Security</p></body></html>""",
            """<html><body><p>Urgent! Unusual activity detected. Secure your Amazon account at <a href="http://amaz0n-security.com/login">here</a>.</p><p>Amazon Team</p></body></html>""",
            """<html><body><p>Your bank account is at risk! Verify your details at <a href="http://bank0fnigeria.com/secure">this link</a> within 24 hours.</p><p>Bank of Nigeria</p></body></html>"""
        ]
        content_type = 'text/html'
        sender = random.choice(fallback_senders)
        subject = random.choice(fallback_subjects)
        body = random.choice(fallback_bodies)
        source = 'fallback_template'

        if phishing_data and email_id <= len(phishing_data):
            email_data = phishing_data[email_id - 1]
            sender = email_data.get('sender', sender) or sender
            subject = email_data.get('subject', subject) or subject
            body = email_data.get('body', body)
            urls = email_data.get('urls', None)
            if not urls or urls == '1':
                url_matches = re.findall(r'(https?://[^\s<>"]+)', body)
                urls = url_matches[0] if url_matches else 'http://phish.example.com'
            if not body.startswith('<html'):
                escaped_body = html.escape(body)
                body = f"""<html><body><p>{escaped_body}</p><p>Click <a href="{urls}">here</a> to proceed.</p><p>Security Team</p></body></html>"""
            source = f"{'nazario' if 'nazario' in email_data.get('source_file', '').lower() else 'ceas'}_row_{email_id}"
        encoded_body = quopri.encodestring(body.encode('utf-8')).decode('utf-8')

    eml_content = f"""From: {sender}
To: {receiver}
Subject: {subject}
Date: {date}
Content-Type: {content_type}
Content-Transfer-Encoding: quoted-printable
X-Source: {source}

{encoded_body}"""

    directory = f'emails/{email_type}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    safe_source = source.replace(':', '_').replace(' ', '_')
    filename = f'{directory}/email_{email_id}_{safe_source}.eml'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(eml_content)
    print(f"Generated {filename}")

def main():
    """Generate 250 genuine and 250 spam/phishing emails."""
    genuine_csv = 'enron.csv'
    genuine_data, _ = load_dataset(genuine_csv, label_filter=0)
    phishing_data = load_phishing_data()

    for i in range(1, 251):
        generate_mock_email(i, 'good', genuine_data=genuine_data)
        generate_mock_email(i, 'spam', phishing_data=phishing_data)

if __name__ == '__main__':
    main()
