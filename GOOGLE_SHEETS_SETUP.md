# Google Sheets Integration Setup

This guide will help you set up Google Sheets integration for your expenses app.

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click on it and press "Enable"

## Step 2: Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application" as the application type
4. Give it a name (e.g., "Expenses App")
5. Download the credentials file and rename it to `credentials.json`
6. Place the `credentials.json` file in your project folder

## Step 3: Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Copy the spreadsheet ID from the URL (the long string between `/d/` and `/edit`)
4. Example URL: `https://docs.google.com/spreadsheets/d/1ABC123...XYZ/edit`
   - The ID is: `1ABC123...XYZ`

## Step 4: Configure Streamlit Secrets

Create a `.streamlit/secrets.toml` file in your project folder with:

```toml
GOOGLE_SHEET_ID = "your-actual-spreadsheet-id-here"
```

Replace `your-actual-spreadsheet-id-here` with your actual Google Sheet ID.

## Step 5: Install Dependencies

Run this command in your terminal:

```bash
install-req
```

## Step 6: First Run Setup

1. Run your app: `streamlit run expenses_list.py`
2. The first time you add an expense, your browser will open for Google authentication
3. Sign in with your Google account and grant permissions
4. A `token.pickle` file will be created (this stores your authentication)

## How It Works

- Every time you add an expense, it gets saved both locally and to your Google Sheet
- The Google Sheet will automatically have headers: Date, Item, Amount, Category
- If Google Sheets is unavailable, the app still works locally
- Your data is safely stored in both places

## Troubleshooting

- **"credentials.json not found"**: Make sure you downloaded and placed the credentials file correctly
- **"Permission denied"**: Make sure you shared the Google Sheet with the same Google account you authenticated with
- **"Invalid spreadsheet ID"**: Double-check that you copied the correct ID from the URL

## Security Note

- Never share your `credentials.json` or `token.pickle` files
- Add them to your `.gitignore` file if using version control
- The app will work without Google Sheets if these files are missing
