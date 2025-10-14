import json
import google.generativeai as genai
import streamlit as st

def parse_expense_with_gemini(transcribed_text):
    """
    Use Gemini to parse natural language expense description into structured data.
    
    Args:
        transcribed_text: The text transcribed from voice input
        
    Returns:
        Dictionary with parsed expense data or None if parsing failed
    """
    try:
        # Configure Gemini if API key is available
        if 'GEMINI_API_KEY' not in st.secrets:
            return None
            
        genai.configure(api_key=st.secrets.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create prompt for Gemini
        prompt = f"""
        Parse this expense description into structured data:
        "{transcribed_text}"
        
        Extract the following information:
        1. Item name (what was purchased)
        2. Amount (in euros, as a number)
        3. Category (choose from: Groceries, Restaurants, Cafeteria, Transportation, Entertainment, Shopping, Bills, Donations, Other)
        
        Return ONLY a JSON object with this exact format:
        {{
            "item": "extracted item name",
            "amount": extracted_amount_as_number,
            "category": "selected_category"
        }}
        
        If you cannot determine any field, use "Unknown" for item, 0 for amount, and "Other" for category.
        Be precise with the amount - extract only the numerical value.
        """
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        try:
            # Clean the response text (remove markdown formatting if present)
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            parsed_data = json.loads(response_text)
            
            # Validate the parsed data
            if all(key in parsed_data for key in ['item', 'amount', 'category']):
                return {
                    'item': str(parsed_data['item']),
                    'amount': float(parsed_data['amount']),
                    'category': str(parsed_data['category'])
                }
            else:
                return None
                
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract information manually
            return extract_fallback_data(transcribed_text)
            
    except Exception as e:
        st.error(f"Error parsing with Gemini: {str(e)}")
        return None

def extract_fallback_data(text):
    """
    Fallback method to extract basic information if Gemini parsing fails.
    """
    import re
    
    # Try to extract amount (look for numbers with euro symbols or currency)
    amount_match = re.search(r'(\d+(?:\.\d{2})?)', text)
    amount = float(amount_match.group(1)) if amount_match else 0.0
    
    # Simple category detection based on keywords
    text_lower = text.lower()
    if any(word in text_lower for word in ['grocery', 'supermarket', 'food', 'shopping']):
        category = 'Groceries'
    elif any(word in text_lower for word in ['restaurant', 'lunch', 'dinner', 'eat']):
        category = 'Restaurants'
    elif any(word in text_lower for word in ['cafeteria', 'cafe', 'coffee']):
        category = 'Cafeteria'
    elif any(word in text_lower for word in ['bus', 'train', 'transport', 'taxi', 'uber']):
        category = 'Transportation'
    elif any(word in text_lower for word in ['movie', 'entertainment', 'game', 'fun']):
        category = 'Entertainment'
    elif any(word in text_lower for word in ['bill', 'payment', 'subscription']):
        category = 'Bills'
    elif any(word in text_lower for word in ['donation', 'charity', 'give']):
        category = 'Donations'
    else:
        category = 'Other'
    
    return {
        'item': text.strip(),
        'amount': amount,
        'category': category
    }

def get_voice_input_examples():
    """
    Return examples of natural language expense descriptions.
    """
    return [
        "I spent 15 euros on lunch at the cafeteria",
        "Bought groceries for 45.50 at the supermarket",
        "Paid 12 euros for bus tickets",
        "Coffee at Starbucks, 4.80 euros",
        "Movie tickets cost 18 euros",
        "Donated 25 euros to charity",
        "Restaurant dinner for 35.75 euros",
        "Uber ride cost 8.50 euros"
    ]
