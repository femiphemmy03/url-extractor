import os
import random
from datetime import datetime
import base64
import quopri  # For quoted-printable encoding

def generate_mock_email(email_id, email_type):
    """Generate a production-ready .eml file (genuine or spam/phishing)."""
    # Common headers
    receiver = random.choice([
        'femi.ade@example.com', 'femi.ola@university.edu', 'femi@startup.ng'
    ])
    date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0100')
    
    if email_type == 'good':
        # Genuine email: Professional or transactional
        senders = [
            'hr@techcorp.com', 'support@bankoflagos.com', 'no-reply@ecommerce.ng',
            'prof.ade@university.edu', 'orders@shoponline.com'
        ]
        subjects = [
            'Q3 Performance Review Meeting',
            'Your Transaction Receipt',
            'Welcome to Our Platform!',
            'Lecture Schedule Update',
            'Order Confirmation #ORD12345'
        ]
        bodies = [
            """Dear Femi,\nPlease join us for your Q3 performance review on Friday at 10 AM.\nBest regards,\nJane Doe, HR Manager""",
            """Dear Femi,\nYour transaction of NGN 5,000 was successful.\nRef: TXN789012\nThank you,\nBank of Lagos""",
            """Welcome to ShopOnline, Femi!\nExplore our products at http://shoponline.ng.\nCheers,\nThe ShopOnline Team""",
            """Dear Students,\nThe lecture schedule for CS101 has been updated.\nCheck http://university.edu/schedule.\nProf. Ade""",
            """Dear Femi,\nYour order #ORD12345 has been shipped.\nTrack at http://shoponline.ng/track.\nThank you,\nShopOnline"""
        ]
        # Plain text for simplicity
        content_type = 'text/plain'
        body = random.choice(bodies)
        # Encode body (plain text, no special encoding needed)
        encoded_body = body
    
    else:  # spam/phishing
        # Spam/phishing email: Kaggle-inspired phishing structure
        senders = [
            'alert@paypa1.com', 'security@amaz0n.com', 'verify@bank0fnigeria.com',
            'support@g00gle.com', 'promo@lotteryng.com'
        ]
        subjects = [
            'Urgent: Verify Your Account Now!',
            'Your PayPal Account is Suspended!',
            'Security Alert: Unusual Activity Detected',
            'Claim Your $1000 Amazon Gift Card!',
            'Your Bank Account Needs Immediate Action!'
        ]
        # HTML bodies with malicious URLs and phishing traits
        bodies = [
            """<html><body><p>Dear Customer,</p><p>Your PayPal account has been locked. Click <a href="http://secure-login.xyz/verify">here</a> to verify your identity.</p><p>Thank you,<br>PayPal Security</p></body></html>""",
            """<html><body><p>Urgent! Unusual activity detected on your Amazon account. Secure it now at <a href="http://amaz0n-security.com/login">http://amaz0n-security.com/login</a>.</p><p>Amazon Team</p></body></html>""",
            """<html><body><p>Your bank account is at risk! Verify your details at <a href="http://bank0fnigeria.com/secure">this link</a> within 24 hours.</p><p>Bank of Nigeria</p></body></html>""",
            """<html><body><p>Congratulations! You’ve won a $1000 gift card. Claim it at <a href="http://lotteryng-promo.com/claim">http://lotteryng-promo.com/claim</a>.</p><p>Lottery NG</p></body></html>""",
            """<html><body><p>Your Google account needs verification. Click <a href="http://g00gle-verify.com">here</a> to avoid suspension.</p><p>Google Support</p></body></html>"""
        ]
        content_type = 'text/html'
        body = random.choice(bodies)
        # Encode body as quoted-printable (common in phishing emails)
        encoded_body = quopri.encodestring(body.encode('utf-8')).decode('utf-8')
    
    # Construct .eml content with headers
    sender = random.choice(senders)
    eml_content = f"""From: {sender}
To: {receiver}
Subject: {random.choice(subjects)}
Date: {date}
Content-Type: {content_type}
Content-Transfer-Encoding: quoted-printable

{encoded_body}"""
    
    # Save to appropriate directory
    directory = f'emails/{email_type}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(f'{directory}/email_{email_id}.eml', 'w', encoding='utf-8') as f:
        f.write(eml_content)
    print(f"Generated {email_type}/email_{email_id}.eml")

def main():
    """Generate 250 genuine and 250 spam/phishing emails."""
    for i in range(1, 251):
        generate_mock_email(i, 'good')
        generate_mock_email(i, 'spam')

if __name__ == '__main__':
    main()
