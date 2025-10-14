#!/usr/bin/env python3
"""
Script to generate tokens for Streamlit Cloud deployment.
Run this locally to create the tokens needed for cloud deployment.
"""

import os
import base64
import json
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def generate_tokens():
    """Generate tokens for cloud deployment."""
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please download your credentials.json file from Google Cloud Console first.")
        return
    
    print("🔐 Generating tokens for Streamlit Cloud deployment...")
    
    # Load credentials
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save tokens for cloud deployment
    tokens_info = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
    
    # Encode tokens for Streamlit secrets
    tokens_json = json.dumps(tokens_info)
    tokens_b64 = base64.b64encode(tokens_json.encode()).decode()
    
    print("✅ Tokens generated successfully!")
    print("\n📋 Add this to your Streamlit Cloud secrets:")
    print("=" * 50)
    print(f"GOOGLE_TOKENS = \"\"\"{tokens_b64}\"\"\"")
    print("=" * 50)
    
    # Also encode credentials for reference
    with open('credentials.json', 'r') as f:
        credentials_json = f.read()
    credentials_b64 = base64.b64encode(credentials_json.encode()).decode()
    
    print("\n📋 Also add this to your Streamlit Cloud secrets:")
    print("=" * 50)
    print(f"GOOGLE_CREDENTIALS = \"\"\"{credentials_b64}\"\"\"")
    print("=" * 50)
    
    print("\n🔧 Instructions:")
    print("1. Copy both GOOGLE_TOKENS and GOOGLE_CREDENTIALS to your Streamlit Cloud secrets")
    print("2. Make sure your Google Sheet ID is also in the secrets")
    print("3. Redeploy your app")
    
    # Save tokens locally for reference
    with open('cloud_tokens.txt', 'w') as f:
        f.write(f"GOOGLE_TOKENS = \"\"\"{tokens_b64}\"\"\"\n")
        f.write(f"GOOGLE_CREDENTIALS = \"\"\"{credentials_b64}\"\"\"\n")
    
    print("\n💾 Tokens saved to cloud_tokens.txt for reference")

if __name__ == "__main__":
    generate_tokens()
