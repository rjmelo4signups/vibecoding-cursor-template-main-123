import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_service():
    """Get authenticated Google Sheets service."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def append_expense_to_sheet(spreadsheet_id, expense_data):
    """
    Append expense data to Google Sheet.
    
    Args:
        spreadsheet_id: The ID of the Google Sheet
        expense_data: Dictionary with expense information
    """
    try:
        service = get_google_sheets_service()
        
        # Prepare the data to append
        values = [
            [
                expense_data['Date'],
                expense_data['Item'],
                expense_data['Amount'],
                expense_data['Category']
            ]
        ]
        
        # Append the data to the sheet
        body = {
            'values': values
        }
        
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A:D',  # Adjust range as needed
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        return True, "Expense added to Google Sheet successfully!"
        
    except HttpError as error:
        return False, f"An error occurred: {error}"
    except Exception as error:
        return False, f"An unexpected error occurred: {error}"

def setup_sheet_headers(spreadsheet_id):
    """
    Set up headers in the Google Sheet if they don't exist.
    """
    try:
        service = get_google_sheets_service()
        
        # Check if the sheet has headers
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1:D1'
        ).execute()
        
        values = result.get('values', [])
        
        # If no headers exist, add them
        if not values:
            header_values = [['Date', 'Item', 'Amount', 'Category']]
            body = {
                'values': header_values
            }
            
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A1:D1',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
        return True, "Sheet headers set up successfully!"
        
    except Exception as error:
        return False, f"Error setting up sheet headers: {error}"

def load_expenses_from_sheet(spreadsheet_id):
    """
    Load all expenses from Google Sheet.
    
    Args:
        spreadsheet_id: The ID of the Google Sheet
        
    Returns:
        Tuple of (success, data_or_error_message)
    """
    try:
        service = get_google_sheets_service()
        
        # Get all data from the sheet (starting from row 2 to skip headers)
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A2:D'  # Skip header row
        ).execute()
        
        values = result.get('values', [])
        
        # Convert to list of dictionaries
        expenses = []
        for row in values:
            if len(row) >= 4:  # Make sure we have all 4 columns
                expense = {
                    "Date": row[0],
                    "Item": row[1],
                    "Amount": float(row[2]) if row[2] else 0.0,
                    "Category": row[3]
                }
                expenses.append(expense)
        
        return True, expenses
        
    except HttpError as error:
        return False, f"Google Sheets error: {error}"
    except Exception as error:
        return False, f"Error loading expenses: {error}"
