#!/usr/bin/env python3
"""
Simple script to test Resend API email sending
Usage: python test_email_simple.py YOUR_API_KEY your@email.com
"""

import sys
import requests
import json


def send_test_email(api_key, to_email):
    """Send a simple test email via Resend API"""
    
    # Simple test email content
    subject = "BiteDrop Test Email - Resend API"
    html_content = """
    <html>
        <body>
            <h2>🎉 BiteDrop Test Email</h2>
            <p>Hello!</p>
            <p>This is a test email sent via Resend API.</p>
            <p><strong>Details:</strong></p>
            <ul>
                <li>Service: BiteDrop</li>
                <li>API: Resend</li>
                <li>Status: Working! ✅</li>
            </ul>
            <p>If you received this email, the integration is working correctly!</p>
        </body>
    </html>
    """
    
    text_content = """
    BiteDrop Test Email
    
    Hello!
    
    This is a test email sent via Resend API.
    
    Details:
    - Service: BiteDrop
    - API: Resend
    - Status: Working! ✅
    
    If you received this email, the integration is working correctly!
    """
    
    print(f"📧 Sending test email to: {to_email}")
    print(f"🔑 Using API key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "from": "BiteDrop <noreply@resend.dev>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
                "text": text_content
            },
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Email sent successfully!")
            print(f"📧 Email ID: {result.get('id', 'Unknown')}")
            return True
        else:
            print("❌ FAILED! Email sending failed.")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_email_simple.py YOUR_API_KEY your@email.com")
        print("Example: python test_email_simple.py re_123abc... test@example.com")
        sys.exit(1)
    
    api_key = sys.argv[1]
    email = sys.argv[2]
    
    success = send_test_email(api_key, email)
    sys.exit(0 if success else 1)
