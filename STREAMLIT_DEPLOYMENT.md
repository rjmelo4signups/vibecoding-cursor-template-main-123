# Streamlit Cloud Deployment Guide

This guide will help you deploy your expenses app to Streamlit Cloud with Google Sheets integration.

## Step 1: Prepare Your GitHub Repository

### 1.1 Push Your Code to GitHub
1. Make sure all your files are committed and pushed to your GitHub repository
2. Your repository should include:
   - `expenses_list.py` (main app)
   - `google_sheets_helper.py` (Google Sheets integration)
   - `requirements.txt` (dependencies)
   - `GOOGLE_SHEETS_SETUP.md` (setup instructions)

### 1.2 Repository Structure
Your repository should look like this:
```
your-repo/
├── expenses_list.py
├── google_sheets_helper.py
├── requirements.txt
├── GOOGLE_SHEETS_SETUP.md
└── .gitignore
```

## Step 2: Deploy to Streamlit Cloud

### 2.1 Go to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"

### 2.2 Configure Your App
1. **Repository**: Select your GitHub repository
2. **Branch**: Choose `main` (or your default branch)
3. **Main file path**: Enter `expenses_list.py`
4. **App URL**: Choose a custom URL (e.g., `your-name-expenses-app`)

### 2.3 Set Up Secrets in Streamlit Cloud
1. In your Streamlit Cloud dashboard, go to your app
2. Click "Settings" (gear icon)
3. Go to "Secrets" tab
4. Add your Google Sheet ID:

```toml
GOOGLE_SHEET_ID = "your-actual-spreadsheet-id-here"
```

## Step 3: Configure Google Sheets for Cloud Deployment

### 3.1 Update Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to "APIs & Services" > "Credentials"
4. Edit your OAuth client
5. **Add authorized redirect URIs**:
   - `https://your-app-name.streamlit.app/`
   - `https://your-app-name.streamlit.app/_stcore/oauth/callback`

### 3.2 Download New Credentials
1. Download the updated `credentials.json`
2. **Important**: You need to upload this to Streamlit Cloud

## Step 4: Upload Credentials to Streamlit Cloud

### 4.1 Create a Secrets File
Create a file called `.streamlit/secrets.toml` in your repository:

```toml
GOOGLE_SHEET_ID = "your-actual-spreadsheet-id-here"

# Google Sheets API Credentials (base64 encoded)
GOOGLE_CREDENTIALS = """
# Paste your credentials.json content here (base64 encoded)
# You'll need to encode your credentials.json file
"""
```

### 4.2 Encode Your Credentials
Run this command to encode your credentials:

```bash
# On Mac/Linux
base64 -i credentials.json

# On Windows (PowerShell)
[Convert]::ToBase64String([IO.File]::ReadAllBytes("credentials.json"))
```

### 4.3 Update Your Code for Cloud Deployment
Modify `google_sheets_helper.py` to handle cloud credentials:

```python
import os
import base64
import json
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_service():
    """Get authenticated Google Sheets service."""
    creds = None
    
    # Check if we're in Streamlit Cloud
    if 'GOOGLE_CREDENTIALS' in st.secrets:
        # Decode credentials from secrets
        credentials_json = base64.b64decode(st.secrets.GOOGLE_CREDENTIALS).decode('utf-8')
        credentials_info = json.loads(credentials_json)
        
        # Use credentials from secrets
        flow = InstalledAppFlow.from_client_config(credentials_info, SCOPES)
        creds = flow.run_local_server(port=0)
    else:
        # Local development
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service
```

## Step 5: Deploy and Test

### 5.1 Deploy Your App
1. Push all changes to your GitHub repository
2. Streamlit Cloud will automatically redeploy your app
3. Check the deployment logs for any errors

### 5.2 Test Your App
1. Visit your deployed app URL
2. Try adding a new expense
3. Check your Google Sheet to verify data is being saved
4. Refresh the app to see if it loads existing data

## Troubleshooting

### Common Issues:
1. **"Credentials not found"**: Make sure you've uploaded credentials to Streamlit secrets
2. **"Permission denied"**: Check that your Google Sheet is shared with the correct account
3. **"Invalid redirect URI"**: Update your Google Cloud Console with the correct Streamlit URL
4. **"App won't load"**: Check the deployment logs in Streamlit Cloud

### Getting Help:
- Check Streamlit Cloud logs in your app dashboard
- Verify your Google Cloud Console settings
- Test locally first to ensure everything works

## Security Notes

- Never commit `credentials.json` or `token.pickle` to your repository
- Use Streamlit secrets for sensitive configuration
- Regularly rotate your Google API credentials
- Monitor your Google Cloud Console for unusual activity

## Cost Information

- **Streamlit Cloud**: Free for public repositories
- **Google Sheets API**: Free for reasonable usage
- **Google Cloud**: Free tier available

Your app will be accessible at: `https://your-app-name.streamlit.app`
