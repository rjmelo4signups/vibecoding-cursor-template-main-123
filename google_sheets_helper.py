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
    
    # Check if we're in Streamlit Cloud (has GOOGLE_CREDENTIALS in secrets)
    if 'GOOGLE_CREDENTIALS' in st.secrets:
        try:
            # Decode credentials from Streamlit secrets
            credentials_json = base64.b64decode(st.secrets.GOOGLE_CREDENTIALS).decode('utf-8')
            credentials_info = json.loads(credentials_json)
            
            # For cloud deployment, we need to use service account or stored tokens
            # Check if we have stored tokens in secrets
            if 'GOOGLE_TOKENS' in st.secrets:
                # Use stored tokens
                tokens_json = base64.b64decode(st.secrets.GOOGLE_TOKENS).decode('utf-8')
                tokens_info = json.loads(tokens_json)
                creds = Credentials.from_authorized_user_info(tokens_info, SCOPES)
            else:
                # For cloud deployment, we need to use a different approach
                # This requires setting up a service account or manual token generation
                st.error("Google Sheets authentication not configured for cloud deployment. Please set up GOOGLE_TOKENS in your Streamlit secrets.")
                return None
                
        except Exception as e:
            st.error(f"Error with cloud credentials: {str(e)}")
            return None
    else:
        # Local development - use files
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    st.error("credentials.json not found. Please set up Google Sheets integration.")
                    return None
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
                expense_data['Category'],
                # Use Timestamp if provided; else leave blank for backward compatibility
                expense_data.get('Timestamp', '')
            ]
        ]
        
        # Append the data to the sheet
        body = {
            'values': values
        }
        
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A:E',  # Include Timestamp column
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
            range='Sheet1!A1:E1'
        ).execute()
        
        values = result.get('values', [])
        
        # If no headers exist, add them (now including Timestamp)
        if not values:
            header_values = [['Date', 'Item', 'Amount', 'Category', 'Timestamp']]
            body = {
                'values': header_values
            }
            
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A1:E1',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
        else:
            # If headers exist but Timestamp column is missing, extend headers to include it
            existing_headers = values[0]
            if 'Timestamp' not in existing_headers:
                # Append Timestamp header in column E
                service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range='Sheet1!E1',
                    valueInputOption='USER_ENTERED',
                    body={'values': [['Timestamp']]}
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
            range='Sheet1!A2:E'  # Skip header row, include Timestamp
        ).execute()
        
        values = result.get('values', [])
        
        # Convert to list of dictionaries
        expenses = []
        for row in values:
            if len(row) >= 4:  # Make sure we have base 4 columns
                expense = {
                    "Date": row[0],
                    "Item": row[1],
                    "Amount": float(row[2]) if row[2] else 0.0,
                    "Category": row[3]
                }
                # Optionally include Timestamp if present (column E)
                if len(row) >= 5 and row[4]:
                    expense["Timestamp"] = row[4]
                expenses.append(expense)
        
        return True, expenses
        
    except HttpError as error:
        return False, f"Google Sheets error: {error}"
    except Exception as error:
        return False, f"Error loading expenses: {error}"

def clear_all_expenses_from_sheet(spreadsheet_id):
    """
    Clear all expense data from Google Sheet (keep headers).
    
    Args:
        spreadsheet_id: The ID of the Google Sheet
        
    Returns:
        Tuple of (success, message)
    """
    try:
        service = get_google_sheets_service()
        
        # Clear all data except headers (rows 2 onwards)
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A2:E'
        ).execute()
        
        return True, "All expenses cleared from Google Sheet successfully!"
        
    except HttpError as error:
        return False, f"Google Sheets error: {error}"
    except Exception as error:
        return False, f"Error clearing expenses: {error}"

def delete_expense_from_sheet(spreadsheet_id, expense_data, debug: bool = False):
    """
    Delete a specific expense from Google Sheet by finding and removing the row.
    
    Args:
        spreadsheet_id: The ID of the Google Sheet
        expense_data: Dictionary with expense information to delete
        
    Returns:
        Tuple of (success, message)
    """
    try:
        service = get_google_sheets_service()

        if service is None:
            return False, "Failed to initialize Google Sheets service."

        # Get all data from the sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A:E'
        ).execute()
        
        values = result.get('values', [])
        if debug:
            try:
                st.write("[DEBUG] Loaded rows:", len(values))
                st.write("[DEBUG] Sample rows:", values[:5])
            except Exception:
                pass
        
        # Find the row to delete (search through all rows including headers)
        row_to_delete = None
        has_ts = 'Timestamp' in expense_data and str(expense_data.get('Timestamp', '')).strip() != ''
        for i, row in enumerate(values):
            if len(row) >= 4:
                if i == 0:
                    continue  # Skip header row
                # Prefer exact match on Timestamp if both payload and row include it
                if has_ts and len(row) >= 5 and str(row[4]).strip() == str(expense_data['Timestamp']).strip():
                    row_to_delete = i + 1
                    break
                # Fallback legacy match if no Timestamp or not found
                # Normalize amount for robust comparison
                amt_row = None
                try:
                    amt_row = float(str(row[2]).replace(',', '.'))
                except Exception:
                    pass
                amt_payload = None
                try:
                    amt_payload = float(str(expense_data['Amount']).replace(',', '.'))
                except Exception:
                    pass
                amount_matches = False
                if amt_row is not None and amt_payload is not None:
                    amount_matches = abs(amt_row - amt_payload) < 0.005
                else:
                    amount_matches = str(row[2]) == str(expense_data['Amount'])

                if (row[0] == expense_data['Date'] and 
                    row[1] == expense_data['Item'] and 
                    amount_matches and 
                    row[3] == expense_data['Category']):
                    row_to_delete = i + 1  # +1 because Google Sheets uses 1-based indexing
                    break
        
        if row_to_delete is None:
            if debug:
                try:
                    st.write("[DEBUG] No matching row found for:", expense_data)
                except Exception:
                    pass
            return False, "Expense not found in Google Sheet"
        
        # Use a simpler approach - clear the specific row and shift up
        # First, get the sheet info to get the correct sheet ID
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        # Prefer the sheet titled 'Sheet1', else fallback to the first sheet
        sheet_id = None
        for s in sheet_metadata.get('sheets', []):
            props = s.get('properties', {})
            if props.get('title') == 'Sheet1':
                sheet_id = props.get('sheetId')
                break
        if sheet_id is None and sheet_metadata.get('sheets'):
            sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']
        if debug:
            try:
                st.write("[DEBUG] Using sheet_id:", sheet_id, "for deletion at row", row_to_delete)
            except Exception:
                pass
        
        # Delete the row
        request_body = {
            'requests': [{
                'deleteDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': row_to_delete - 1,  # Convert to 0-based index
                        'endIndex': row_to_delete
                    }
                }
            }]
        }

        service.spreadsheets().batch_update(
            spreadsheetId=spreadsheet_id,
            body=request_body
        ).execute()
        
        return True, "Expense deleted from Google Sheet successfully!"
        
    except HttpError as error:
        return False, f"Google Sheets error: {error}"
    except Exception as error:
        return False, f"Error deleting expense: {error}"

