# Gemini Voice Input Setup Guide

This guide will help you set up the Gemini-powered voice input feature for your expenses app.

## Step 1: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## Step 2: Configure Streamlit Secrets

### For Local Development
Create or update `.streamlit/secrets.toml`:

```toml
# Google Sheets (existing)
GOOGLE_SHEET_ID = "your-spreadsheet-id-here"

# Gemini API Key (new)
GEMINI_API_KEY = "your-gemini-api-key-here"
```

### For Streamlit Cloud Deployment
1. Go to your Streamlit Cloud app dashboard
2. Click "Settings" (gear icon)
3. Go to "Secrets" tab
4. Add your Gemini API key:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

## Step 3: Install Dependencies

Run this command to install the new dependencies:

```bash
install-req
```

## Step 4: Test the Feature

### Text-Based Voice Input (Works Immediately)
1. Open your expenses app
2. In the sidebar, find the "🎤 Voice Input" section
3. Type a natural expense description like: "I spent 15 euros on lunch at the cafeteria"
4. Click "🤖 Parse with Gemini"
5. Watch as Gemini automatically fills in the form fields!

### Audio Recording (Future Enhancement)
The microphone button is ready for when you implement speech-to-text. Currently it shows a placeholder message.

## How It Works

### Natural Language Examples
You can type or say things like:
- "I spent 15 euros on lunch at the cafeteria"
- "Bought groceries for 45.50 at the supermarket"
- "Paid 12 euros for bus tickets"
- "Coffee at Starbucks, 4.80 euros"
- "Movie tickets cost 18 euros"
- "Donated 25 euros to charity"

### What Gemini Extracts
- **Item**: "lunch at the cafeteria"
- **Amount**: 15.00
- **Category**: "Cafeteria"

### Supported Categories
- Groceries
- Restaurants
- Cafeteria
- Transportation
- Entertainment
- Shopping
- Bills
- Donations
- Other

## Features

### ✅ What Works Now
- **Text-based voice input**: Type natural descriptions
- **Gemini parsing**: AI extracts structured data
- **Auto-fill forms**: Automatically populates expense fields
- **Smart categorization**: AI chooses appropriate category
- **Amount extraction**: Finds numerical values in text

### 🔄 Future Enhancements
- **Real voice recording**: Microphone input with speech-to-text
- **Mobile optimization**: Better mobile voice experience
- **Multi-language support**: Parse expenses in different languages
- **Voice commands**: "Add expense" voice triggers

## Troubleshooting

### Common Issues
1. **"GEMINI_API_KEY not found"**: Make sure you've added the API key to secrets
2. **"Error parsing with Gemini"**: Check your internet connection and API key
3. **"Could not parse the expense"**: Try rephrasing your description

### Tips for Better Results
- Be specific about amounts: "15 euros" instead of "fifteen"
- Mention the category: "lunch at the cafeteria" vs "lunch"
- Include the item: "coffee at Starbucks" vs just "coffee"

## Cost Information

- **Gemini API**: Free tier available (generous limits)
- **Google AI Studio**: Free for reasonable usage
- **Streamlit Cloud**: Free for public repositories

## Security Notes

- Never commit your Gemini API key to version control
- Use Streamlit secrets for secure storage
- Monitor your API usage in Google AI Studio
- Rotate API keys regularly for security

Your expenses app now has AI-powered natural language processing! 🎉
